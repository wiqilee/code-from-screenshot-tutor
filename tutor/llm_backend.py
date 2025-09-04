# tutor/llm_backend.py
from __future__ import annotations

import os
from typing import Optional

try:
    # Load variables from .env if present (no-op if the file doesn't exist)
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()
except Exception:
    # If python-dotenv isn't installed, we just skip silently
    pass


class LLMBackend:
    """
    Simple backend switcher for:
      - OpenAI Chat Completions API
      - Local HuggingFace model via transformers.pipeline (CPU by default)

    Env vars (optional, with defaults):
      LLM_BACKEND=openai | local
      OPENAI_API_KEY=sk- # API key
      OPENAI_MODEL=gpt-4o-mini
      LLM_MODEL_ID=TinyLlama/TinyLlama-1.1B-Chat-v1.0
      LLM_TEMPERATURE=0.2
      LLM_MAX_TOKENS=256
    """

    def __init__(self) -> None:
        self.backend = os.getenv("LLM_BACKEND", "openai").lower()
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.model_id = os.getenv("LLM_MODEL_ID", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.2"))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "256"))

        if self.backend not in {"openai", "local"}:
            raise ValueError("LLM_BACKEND must be either 'openai' or 'local'")

        if self.backend == "openai" and not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError(
                "OPENAI_API_KEY is not set. "
                "Set it in your shell (export OPENAI_API_KEY=...) or in a .env file."
            )

    # Public API --------------------------------------------------------------

    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        if self.backend == "openai":
            return self._generate_openai(prompt, system)
        return self._generate_local(prompt)

    # Private helpers ---------------------------------------------------------

    def _generate_openai(self, prompt: str, system: Optional[str]) -> str:
        from openai import OpenAI  # lazy import so local mode works without it

        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        # Chat Completions API
        resp = client.chat.completions.create(
            model=self.openai_model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        # Defensive extraction (handles SDK variations safely)
        choice = getattr(resp, "choices", [None])[0]
        if not choice or not getattr(choice, "message", None):
            raise RuntimeError("OpenAI returned an unexpected response format.")
        return choice.message.content or ""

    def _generate_local(self, prompt: str) -> str:
        # CPU by default so it runs everywhere
        from transformers import pipeline  # lazy import

        pipe = pipeline(
            task="text-generation",
            model=self.model_id,
            device=-1,  # CPU
        )
        out = pipe(
            prompt,
            max_new_tokens=self.max_tokens,
            do_sample=(self.temperature > 0),
            temperature=self.temperature,
            truncation=True,
            return_full_text=False,
        )
        # pipeline returns a list of dicts like [{"generated_text": "..."}]
        text = (out[0].get("generated_text") if out and isinstance(out, list) else "") or ""
        return text.strip()
