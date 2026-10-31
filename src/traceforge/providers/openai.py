"""OpenAI-compatible chat completion adapter using standard-library HTTP."""

import json
import os
from urllib.request import Request, urlopen

from traceforge.providers.base import Completion


class OpenAIProvider:
    """Call OpenAI's Chat Completions endpoint with an environment API key."""

    def __init__(self, model: str, api_key: str | None = None, timeout: float = 30) -> None:
        self.model = model
        self.api_key = api_key or os.environ["OPENAI_API_KEY"]
        self.timeout = timeout

    def complete(self, prompt: str) -> Completion:
        """Send a single prompt and normalize response usage metadata."""
        body = json.dumps(
            {"model": self.model, "messages": [{"role": "user", "content": prompt}]}
        ).encode()
        request = Request(
            "https://api.openai.com/v1/chat/completions",
            data=body,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
        )
        with urlopen(request, timeout=self.timeout) as response:
            data = json.load(response)
        usage = data.get("usage", {})
        return {
            "text": str(data["choices"][0]["message"]["content"]),
            "model": str(data.get("model", self.model)),
            "input_tokens": int(usage.get("prompt_tokens", 0)),
            "output_tokens": int(usage.get("completion_tokens", 0)),
        }
