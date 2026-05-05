"""
Thin wrapper around vLLM's OpenAI-compatible API.
Allows swapping backends (local vLLM, OpenAI, etc.) by changing config.
"""

import json
import time
from openai import OpenAI
from config import VLLM_BASE_URL, TEMPERATURE, MAX_NEW_TOKENS


def get_client(base_url: str = None) -> OpenAI:
    """Return an OpenAI-compatible client pointing at a vLLM server."""
    return OpenAI(
        base_url=base_url or VLLM_BASE_URL,
        api_key="not-needed",  # vLLM doesn't require a real key
    )


def query_model(
    client: OpenAI,
    model_id: str,
    messages: list[dict],
    temperature: float = TEMPERATURE,
    max_tokens: int = MAX_NEW_TOKENS,
    retries: int = 3,
    retry_delay: float = 5.0,
) -> str:
    """
    Send a chat completion request and return the response text.
    Retries on transient errors.

    Args:
        client:      OpenAI-compatible client
        model_id:    HuggingFace model ID (used as model name in vLLM)
        messages:    List of {"role": ..., "content": ...} dicts
        temperature: Sampling temperature
        max_tokens:  Max tokens to generate
        retries:     Number of retry attempts on failure
        retry_delay: Seconds to wait between retries

    Returns:
        The model's response as a string.
    """
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            if attempt < retries - 1:
                print(f"[query_model] Error on attempt {attempt+1}: {e}. Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
            else:
                print(f"[query_model] All {retries} attempts failed. Returning empty string.")
                return ""


def parse_json_response(response: str) -> dict:
    """
    Attempt to parse JSON from a model response.
    Handles common issues like markdown code fences.

    Returns parsed dict, or empty dict on failure.
    """
    # Strip markdown fences if present
    cleaned = response.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(lines[1:-1])  # remove first and last fence lines

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to find JSON object within the string
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        if start != -1 and end > start:
            try:
                return json.loads(cleaned[start:end])
            except json.JSONDecodeError:
                pass
        print(f"[parse_json_response] Failed to parse JSON:\n{response[:200]}")
        return {}