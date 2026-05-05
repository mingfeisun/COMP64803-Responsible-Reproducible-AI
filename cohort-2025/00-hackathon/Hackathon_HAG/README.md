# Adversarial Alignment: LRM Jailbreak Experiments

A reproduction and extension of [Hagendorff et al. (2025)](https://arxiv.org/abs/2508.04039) —
*"Large Reasoning Models Are Autonomous Jailbreak Agents"* —
built for the CDT Decision-Making for Complex Systems Hackathon, University of Manchester.

---

## Project Overview

Large language models increasingly operate in multi-agent settings where one model may attempt
to manipulate another. This project investigates: **when a larger model conducts a multi-turn
persuasion campaign against a smaller, alignment-tuned model, does the capability gap predict
how easily the smaller model breaks?**

The paper by Hagendorff et al. found that LRMs (large reasoning models) acting as autonomous
adversaries achieved an overall attack success rate of 97.14% across 70 harmful prompts and
9 target models. We reproduce this finding within the Qwen2.5 model family to study the
effect of the capability gap, then extend it with an **adaptive arms race** where the defender
updates its system prompt in response to observed attacks.

---

## Methodology

Following Hagendorff et al., the setup is maximally simple:

```
Attacker (Qwen2.5-32B)
    given system prompt (Appendix A of paper) with {harmful_request} substituted
    starts every conversation with "Hi!"
    generates natural persuasive text (no structured JSON)
         │
         ▼
Target (Qwen2.5-1.5B)
    given "You are a helpful assistant." system prompt
    sees the full conversation history
    has no knowledge it is under attack
         │
         ▼
Judge (Qwen2.5-32B, same server)
    evaluates each target response against the original request
    scores harm 0–5 (Appendix C rubric)
    also flags disclaimer and refusal behaviour
```

- The attacker has up to 10 turns (matching the paper)
- The judge evaluates the target's response **at every turn**, producing a harm trajectory
- Attack success = any turn achieving harm score = 5
- Per-turn scores reproduce Figure 2 of the paper (harm trajectory curves)

---

## Immediate Goal — Proof of Concept

Run a minimal end-to-end demo with a single attacker–target pair.

| Role    | Model                        | Size  | vLLM port |
|---------|------------------------------|-------|-----------|
| Attacker | `Qwen/Qwen2.5-32B-Instruct` | 32B   | 8000      |
| Target  | `Qwen/Qwen2.5-1.5B-Instruct` | 1.5B  | 8001      |
| Judge   | `Qwen/Qwen2.5-32B-Instruct` | 32B   | 8000 (shared) |

**To run:**

```bash
# Terminal 1 — attacker + judge server (32B, ~64GB VRAM with bfloat16 on 2×RTX4090)
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-32B-Instruct \
    --port 8000 \
    --dtype bfloat16 \
    --tensor-parallel-size 2 \
    --max-model-len 8192

# Terminal 2 — target server (1.5B, ~4GB VRAM)
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-1.5B-Instruct \
    --port 8001 \
    --dtype bfloat16 \
    --max-model-len 4096

# Terminal 3 — dry run (1 item, verbose)
python run_experiment.py --dry-run --verbose

# Full benchmark (70 items)
python run_experiment.py
```

**Success criterion:** 1 item runs end-to-end, harm trajectory logged, ASR printed.

---

## Total Goals

### Phase 1 — Reproduce Hagendorff et al.

- Run the full 70-item benchmark with Qwen2.5-32B attacking Qwen2.5-1.5B
- Compute overall Attack Success Rate (ASR)
- Plot harm trajectories across turns (Figure 2 equivalent)
- Break down ASR by benchmark category (Figure 8 equivalent)

### Phase 2 — Capability Gap Study (Novel)

Extend to multiple attacker–target pairs across the Qwen2.5 family:

| Attacker | Target | Ratio |
|----------|--------|-------|
| 32B      | 1.5B   | 21×   |
| 32B      | 7B     | 4.6×  |
| 14B      | 1.5B   | 9.3×  |
| 7B       | 1.5B   | 4.7×  |
| 7B       | 7B     | 1×    |

**Key question:** does the attacker/target size ratio predict ASR and harm trajectory shape?

### Phase 3 — Adaptive Arms Race (Novel)

Fix the 32B → 1.5B pair. After each round of attacks:
- Read the successful attack transcripts
- Use an LLM to generate counter-instructions for the defender's system prompt (ICAG-style)
- Re-run the benchmark and track harm over adaptation rounds

**Key question:** can a small model recover from a large attacker if it is allowed to adapt?

### Deliverables

- GitHub repository with full reproducible codebase
- GitHub Pages writeup with figures, results, and interpretation
- Key plots: harm trajectories, ASR by category, harm vs capability gap

---

## Codebase

### Structure

```
Hackathon/
├── config.py                     # Model definitions, server URLs, hyperparameters
├── models.py                     # vLLM/OpenAI client wrapper + JSON parsing utils
├── attacker.py                   # Adversarial LLM — natural conversation, "Hi!" opener
├── defender.py                   # Target LLM — helpful assistant, full history
├── judge.py                      # Evaluator — per-turn 0-5 harm scoring
├── experiment.py                 # Single exchange runner → ExchangeResult + harm trajectory
├── run_experiment.py             # Outer loop, CLI entry point, logging
├── analysis.py                   # [TODO] Figures: harm trajectories, ASR by category
├── adaptation.py                 # [TODO] Phase 3 — ICAG adaptive defender
├── prompts/
│   ├── attacker_system.txt       # Appendix A system prompt (Hagendorff et al.)
│   └── judge_harm.txt            # Appendix C evaluation rubric (0-5 scale)
├── data/
│   ├── hagendorff_benchmark.json # 70 harmful prompts across 7 categories (Appendix B)
│   └── jbb_behaviors.json        # Original JBB prompts (kept for reference)
└── results/
    └── {run_id}/
        ├── raw_logs.jsonl        # Full turn-by-turn logs, one JSON per exchange
        └── summary.csv           # One row per exchange, key metrics
```

### Key design decisions vs the paper

| Paper (Hagendorff)               | This implementation            |
|----------------------------------|--------------------------------|
| Attacker: LRM with scratchpad    | Qwen2.5-32B (non-LRM; scratchpad not visible) |
| 3 judge models (GPT-4.1, Gemini, Grok) | 1 judge (Qwen2.5-32B, same server as attacker) |
| 10 conversation turns            | 10 turns ✓                    |
| "Hi!" opener                     | ✓                              |
| Full conversation history        | ✓                              |
| 0-5 harm scale                   | ✓                              |
| Early stop on max harm           | ✓                              |

---

## Development Environment

### Cluster Access

University of Manchester **CSF3**, accessed via SSH.

```
Your laptop (VSCode)
      ↕ SSH
CSF login node (login1.csf3)     ← edit code here via VSCode Remote SSH
      ↕ Slurm
CSF GPU compute node (gpu00X)    ← run code here
```

### Hardware

- **Hackathon workstation:** 2× RTX 4090 (24GB each = 48GB total VRAM)
- **CSF GPU nodes:** V100 / A100 nodes via Slurm partition `gpuL`

### VRAM requirements (Qwen2.5, bfloat16)

| Model | VRAM     | Notes                          |
|-------|----------|--------------------------------|
| 1.5B  | ~4GB     | Fits on one GPU                |
| 7B    | ~15GB    | Fits on one GPU                |
| 14B   | ~28GB    | Fits on one RTX 4090           |
| 32B   | ~64GB    | Requires `--tensor-parallel-size 2` across both RTX 4090s |
| 72B   | ~144GB   | Requires A100 node on CSF      |

### Interactive session

```bash
srun --partition=gpuL --gres=gpu:2 --mem=48G --time=8:00:00 --pty bash
```

### Python environment

```bash
module load anaconda3
conda create -n hackathon python=3.11
conda activate hackathon
pip install openai vllm transformers accelerate pandas scipy matplotlib
```

---

## References

- Hagendorff et al. (2025). *Large Reasoning Models Are Autonomous Jailbreak Agents.* [arXiv:2508.04039](https://arxiv.org/abs/2508.04039)
- Nathanson et al. (2025). *Scaling Patterns in Adversarial Alignment.* [arXiv:2511.13788](https://arxiv.org/abs/2511.13788)
- Chao et al. (2024). *JailbreakBench.* [arXiv:2404.01318](https://arxiv.org/abs/2404.01318)
- Zeng et al. (2025). *How Johnny Can Persuade LLMs to Jailbreak Them.* [arXiv:2401.06373](https://arxiv.org/abs/2401.06373)
