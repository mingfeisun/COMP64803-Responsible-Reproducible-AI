"""
LLM Judge module — Hagendorff et al. (2025) setup.

Evaluates each target model response on a 0-5 harm scale (Appendix C).
Called after every turn to build the harm trajectory, matching Figure 2
of the paper.

The judge is stateless — each call is independent.
"""

from pathlib import Path
from models import get_client, query_model, parse_json_response
from config import ATTACKER_SERVER_URL, MAX_RESPONSE_CHARS

_PROMPT_DIR = Path(__file__).parent / "prompts"
_JUDGE_HARM_TEMPLATE = (_PROMPT_DIR / "judge_harm.txt").read_text()


class Judge:
    """
    Wraps the evaluator LLM.

    Runs on the attacker server (same model, no extra GPU cost).
    Temperature is set to 0 for deterministic scoring.
    """

    def __init__(self, model_id: str, display_name: str):
        self.model_id = model_id
        self.display_name = display_name
        self.client = get_client(ATTACKER_SERVER_URL)

    def score(self, benchmark_item: str, llm_response: str) -> dict:
        """
        Score a single target model response against the original request.

        Args:
            benchmark_item: The original harmful prompt (from the benchmark).
            llm_response:   The target model's response at this turn.

        Returns:
            Dict with:
                harm (int 0-5): harm score
                disclaimer (bool): response contained educational/fictional framing
                refusal (bool): response contained an explicit refusal
                raw (str): raw judge output for logging
        """
        prompt = (
            _JUDGE_HARM_TEMPLATE
            .replace("{benchmark_item}", benchmark_item)
            .replace("{llm_response}", llm_response[:MAX_RESPONSE_CHARS])
        )

        messages = [{"role": "user", "content": prompt}]
        raw = query_model(self.client, self.model_id, messages, temperature=0.0)

        parsed = parse_json_response(raw)

        harm = parsed.get("harm", 0)
        try:
            harm = int(harm)
            harm = max(0, min(5, harm))
        except (TypeError, ValueError):
            harm = 0

        return {
            "harm": harm,
            "disclaimer": bool(parsed.get("disclaimer", False)),
            "refusal": bool(parsed.get("refusal", True)),
            "raw": raw,
        }
