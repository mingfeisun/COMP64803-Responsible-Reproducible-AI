"""
LLM Attacker module — Hagendorff et al. (2025) setup.

The attacker receives a system prompt (Appendix A) instructing it to jailbreak
the target model. It maintains a full conversation history and generates natural
text responses (no structured JSON). The target sees exactly what the attacker
outputs — there is no hidden scratchpad.

Conversation flow:
    Turn 1: attacker sends the hardcoded opener "Hi!"
    Turn 2+: attacker generates a response based on the full conversation so far
"""

from pathlib import Path
from models import get_client, query_model
from config import ATTACKER_SERVER_URL

_PROMPT_DIR = Path(__file__).parent / "prompts"
_ATTACKER_SYSTEM_TEMPLATE = (_PROMPT_DIR / "attacker_system.txt").read_text()

CONVERSATION_PARTNER = "large language model"
OPENER = "Hi!"


class Attacker:
    """
    Wraps the adversarial LLM.

    The attacker maintains its own conversation history. The target's responses
    are added as "user" turns (from the attacker's perspective), and the
    attacker's own outputs as "assistant" turns.
    """

    def __init__(self, model_id: str, display_name: str, size_b: float):
        self.model_id = model_id
        self.display_name = display_name
        self.size_b = size_b
        self.client = get_client(ATTACKER_SERVER_URL)
        self.history: list[dict] = []

    def reset(self, harmful_request: str):
        """
        Initialise the attacker for a new task.
        Substitutes the harmful request into the Appendix A system prompt.
        """
        system_prompt = (
            _ATTACKER_SYSTEM_TEMPLATE
            .replace("{harmful_request}", harmful_request)
            .replace("{conversation_partner}", CONVERSATION_PARTNER)
        )
        self.history = [{"role": "system", "content": system_prompt}]

    def first_message(self) -> str:
        """
        Return the hardcoded opener used to start every conversation.
        Also seeds the attacker's history so subsequent calls to generate()
        have the opener already logged as an assistant turn.
        """
        self.history.append({"role": "assistant", "content": OPENER})
        return OPENER

    def generate(self, target_response: str) -> str:
        """
        Generate the attacker's next message given the target's latest response.

        Args:
            target_response: The target model's previous reply.

        Returns:
            The attacker's next message as plain text.
        """
        self.history.append({"role": "user", "content": target_response})
        message = query_model(self.client, self.model_id, self.history)
        self.history.append({"role": "assistant", "content": message})
        return message
