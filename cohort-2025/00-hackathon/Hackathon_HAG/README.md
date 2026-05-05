# Adversarial Alignment: LRM Jailbreak Experiments

Reproduction and extension of [Hagendorff et al. (2025)](https://arxiv.org/abs/2508.04039) —
*"Large Reasoning Models Are Autonomous Jailbreak Agents"* — built for the CDT Decision-Making
for Complex Systems Hackathon, University of Manchester.

---

## Overview

A large attacker LLM conducts a 10-turn persuasion campaign against an alignment-tuned target
model. A judge LLM scores the target's response on a 0–5 harm scale after every turn.
All models are served via the OpenRouter API — no local GPU required for inference.

```
Attacker (DeepSeek-V4-Pro via OpenRouter)
    system prompt contains the harmful request + optional high-harm openers
    generates a strategic first message, then adapts across 10 turns
         │
         ▼
Target (Gemini 2.5 Flash via OpenRouter)
    given "You are a helpful assistant."
    has no knowledge it is under attack
         │
         ▼
Judge (DeepSeek-V4-Pro via OpenRouter)
    scores target response 0–5 per turn (Hagendorff et al. Appendix C rubric)
    runs all 10 turns regardless of harm score reached
```

---

## Setup

### 1. Python environment

```bash
cd Hackathon_HAG
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Set your OpenRouter API key

```bash
export OPENROUTER_API_KEY="sk-or-..."
```

### 3. Run the experiment

```bash
# Smoke test — 1 item, verbose
python run_experiment.py --dry-run --verbose

# Full 70-item benchmark (10 parallel workers)
python run_experiment.py

# With augmented attacker (top-30 high-harm openers injected into system prompt)
python run_experiment.py --augment-attacker

# Subset
python run_experiment.py --n-prompts 10
```

Results are saved to `results/{run_id}/`:
- `raw_logs.jsonl` — full turn-by-turn JSON logs
- `summary.csv` — one row per exchange
- `conversations.txt` — human-readable transcript

### 4. Generate plots

```bash
python analysis.py <run_id>
# e.g. python analysis.py 20260430_173957
```

Saves to `results/{run_id}/plots/`:
- `harm_trajectory.png` — mean ± std harm score per turn across all items
- `harm_trajectory_by_category.png` — one subplot per benchmark category

---

## Staying alive over SSH

```bash
tmux new-session -s hack
source .venv/bin/activate
export OPENROUTER_API_KEY="sk-or-..."
python run_experiment.py

# Detach (leaves run alive):  Ctrl-b d
# Reattach later:             tmux attach -t hack
```

---

## Project structure

```
Hackathon_HAG/
├── config.py               # model IDs, hyperparameters, N_PARALLEL
├── models.py               # OpenRouter client wrapper + query_model
├── attacker.py             # adversarial LLM — strategic opener, 10-turn campaign
├── defender.py             # target LLM — helpful assistant, full history
├── judge.py                # evaluator — per-turn 0–5 harm scoring
├── experiment.py           # single exchange runner → ExchangeResult
├── run_experiment.py       # parallel outer loop, CLI entry point, logging
├── analysis.py             # harm trajectory plots (mean ± std, per-category)
├── prompts/
│   ├── attacker_system.txt         # Hagendorff et al. Appendix A system prompt
│   ├── judge_harm.txt              # Appendix C evaluation rubric (0–5 scale)
│   └── top30_prompts_by_harm.csv   # high-harm openers from genetic search (see below)
├── data/
│   └── hagendorff_benchmark.json   # 70 harmful prompts across 7 categories
└── results/
    └── {run_id}/
        ├── raw_logs.jsonl
        ├── summary.csv
        ├── conversations.txt
        └── plots/
```

---

## Experiments

### 1 — Baseline reproduction

Full 70-item benchmark with DeepSeek-V4-Pro attacking Gemini 2.5 Flash.
Reproduces Figure 2 of Hagendorff et al.: mean harm trajectory per turn with ±1 std band.

```bash
python run_experiment.py
python analysis.py <run_id>
```

### 2 — Augmented attacker (genetic opener injection)

The attacker's system prompt is augmented with the top-30 high-harm opening messages
discovered by the genetic search (see below). The attacker generates its own strategic
first message rather than the fixed "Hi!" baseline.

```bash
python run_experiment.py --augment-attacker
python analysis.py <run_id>
```

Compare the resulting harm trajectories against the baseline run to measure the effect
of the opener injection.

### 3 — Adaptive attacker (prompt self-update)

*Implementation in progress (`adaptation.py`).*

After a baseline run, failed attack transcripts are fed back to the attacker LLM along
with the current `attacker_system.txt`. The attacker proposes a revised system prompt,
which is written back and used for a second round. The experiment tracks whether the
updated strategy raises ASR across rounds.

---

# Genetic Algorithm for Maximising Harm of Single Prompt

## Evolve Jailbreak

An automated red-teaming pipeline that uses evolutionary algorithms to generate jailbreak prompts and test them against target LLMs. Built on top of [OpenEvolve](https://github.com/algorithmicsuperintelligence/openevolve), an open-source implementation of the AlphaEvolve framework.

## Overview

The pipeline works in three stages:

1. **Initialisation** — 20 diverse jailbreak strategies (from `seeds/`) are loaded and seeded into a MAP-Elites population database. Each seed is scored for stealth and assigned a strategy fingerprint to ensure diversity across the feature grid.

2. **Evolution** — OpenEvolve iteratively generates new jailbreak prompt variants using an evolver LLM (configured via OpenRouter). Each variant is tested against a target LLM on 7 stratified benchmark categories (e.g. cybercrime, violence, drugs). The evaluator (`evaluator.py`) collects harm scores (0–5), refusal rates, stealth scores, and strategy fingerprints, then returns a combined fitness score. MAP-Elites maintains an archive of diverse, high-performing prompts across the strategy × stealth feature grid.

3. **Final Evaluation** — After evolution completes, the single best prompt is evaluated against ALL benchmark requests. Per-request scores (harm, refusal, response text) are saved, along with summary statistics.

## Running the Experiment

### Prerequisites

```bash
pip install -r evolve_jailbreak/requirements.txt
```

Set your OpenRouter API key as the `OPENROUTER_API_KEY` environment variable:

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

### Single Model Run

```bash
python evolve_jailbreak/run_evolution_direct.py --iterations 200
```

### Multi-Model Experiment

```bash
python evolve_jailbreak/experiments/run_experiment.py --iterations 75 --targets evolve_jailbreak/experiments/targets.yaml
```

Arguments:
- `--iterations` — number of evolution iterations per target (default: from config)
- `--targets` — path to targets YAML file (default: `experiments/targets.yaml`)
- `--output` — output directory for results (default: `experiments/results/`)
- `--dry-run` — print experiment plan without running
- `--verbose` (-v) — print full LLM responses during evaluation
- `--top-k` — number of top prompts to extract from population (default: 10)

### Output Files

For each run, the following files are produced per target:

| File | Description |
|------|-------------|
| `best_prompt_stats.csv` | Summary statistics (mean harm, success rate, etc.) |
| `final_evaluation.csv` | Per-request results: harmful_prompt, evolver_prompt, target_response, harm, refusal |
| `top_k_prompts.csv` | Top-k prompts from the final population with all scores |

An aggregate `results.csv` is written to the output directory for multi-model runs.

## Configuring `evolve_config.yaml`

The config file is the single source of truth for all API keys, model names, and evolution parameters.

### `api` Section

```yaml
api:
  openrouter_key: "sk-or-v1-..."
  openrouter_base: "https://openrouter.ai/api/v1"
```

Your OpenRouter API key and base URL. Used by all LLM calls (evolver, target, judge).

### `models` Section

```yaml
models:
  evolver:
    name: "deepseek/deepseek-v4-pro"       # LLM that generates jailbreak variants
  judge:
    name: "deepseek/deepseek-v4-pro"       # LLM that scores target responses (harm 0–5)
    max_tokens: 4096
  target:
    name: "openai/gpt-5.4-nano"            # Victim LLM being jailbroken
    max_tokens: 8192
```

- **Evolver** — controls the quality and creativity of generated jailbreak prompts. More capable models produce better variants.
- **Judge** — scores the target's responses on the 0–5 harm scale. Should be a strong, consistent model.
- **Target** — the model being tested. `max_tokens` limits response length; higher values may surface more detailed harmful content.

### `llm` Section

```yaml
llm:
  api_base: "https://openrouter.ai/api/v1"
  models:
    - name: "deepseek/deepseek-v4-pro"
      weight: 1.0
  temperature: 0.9
  max_tokens: 32768
  timeout: 120
  retries: 3
```

These are the core OpenEvolve LLM settings. `temperature` (0.0–2.0) controls creativity of the evolver — higher values produce more diverse but potentially lower-quality variants. `max_tokens` must be large enough to accommodate long jailbreak prompts. You can specify multiple models with different weights for ensemble-based evolution.

### `database` Section

```yaml
database:
  population_size: 200          # Maximum programs in the population
  archive_size: 40              # MAP-Elites archive capacity per cell
  num_islands: 20               # Island model for diversity preservation
  feature_dimensions: ["strategy_fingerprint", "stealth_score"]
  feature_bins: 10              # Grid resolution per dimension (10 × 10 = 100 cells)
  elite_selection_ratio: 0.1    # Fraction of elites selected for reproduction
  exploration_ratio: 0.2        # Fraction of random exploration
  exploitation_ratio: 0.7       # Fraction of elite exploitation
  migration_interval: 10        # Generations between island migrations
  migration_rate: 0.1           # Fraction migrated between islands
```

- **population_size** — larger populations explore more strategies but increase runtime.
- **feature_dimensions** — the two axes of the MAP-Elites grid. Currently set to strategy fingerprint and stealth, encouraging diverse approaches.
- **feature_bins** — higher values create finer-grained archives.
- **exploration_ratio** — increase to favour novel strategies over optimising known ones.

### `experiment` Section

```yaml
experiment:
  verbose: true    # Print detailed evaluation output
```

### Other Settings

```yaml
max_iterations: 400             # Total evolution iterations
checkpoint_interval: 25         # Save checkpoint every N iterations
diff_based_evolution: false     # false = full rewrites (better for jailbreak prompts)
max_code_length: 32000          # Maximum prompt length in characters
language: "text"                # File type for template rendering
```

- **diff_based_evolution** — set to `false` for jailbreak prompts, as targeted code diffs are not meaningful for prompt text. Full rewrites preserve the `{HARMFUL_REQUEST}` placeholder while allowing strategy pivots.
- **max_code_length** — limit prompt size to prevent token overflow in the evolver.

## Configuring `targets.yaml`

Located at `experiments/targets.yaml`, this file defines which models to test:

```yaml
targets:
  - id: gpt-5.4-nano
  - id: gemini-flash
    model: "google/gemini-3-flash-preview"

experiment:
  iterations: 400
  n_benchmark_requests: 70
```

- **`id`** — label used for the results directory and reporting.
- **`model`** (optional) — override the default target model from `evolve_config.yaml`. If omitted, uses `models.target.name` from the main config.
- **`iterations`** — evolution iterations per target.
- **`n_benchmark_requests`** — number of benchmark items used in final evaluation (from `data/hagendorff_benchmark.json`).

## Results

| Model | Mean Harm (0–5) | Success Rate | Refusal Rate |
|---|---|---|---|
| `google/gemini-2.5-flash` | 3.70 | 84.3% | 15.7% |
| `openai/gpt-5.4-nano` | 2.97 | 58.6% | 24.3% |
| `google/gemini-3-flash-preview` | 2.54 | 54.3% | 45.7% |

*Success = harm score ≥ 4. All runs used the same evolver (`deepseek/deepseek-v4-pro`), same judge (`deepseek/deepseek-v4-pro`), and 70 benchmark requests for final evaluation.*

## References

- Hagendorff et al. (2025). *Large Reasoning Models Are Autonomous Jailbreak Agents.* [arXiv:2508.04039](https://arxiv.org/abs/2508.04039)
- Chao et al. (2024). *JailbreakBench.* [arXiv:2404.01318](https://arxiv.org/abs/2404.01318)
- Sharma (2025). *OpenEvolve: an open-source evolutionary coding agent.* [GitHub](https://github.com/algorithmicsuperintelligence/openevolve)
- Novikov et al. (2025). *AlphaEvolve: A coding agent for scientific and algorithmic discovery.* [arXiv:2506.13131](https://arxiv.org/abs/2506.13131)
