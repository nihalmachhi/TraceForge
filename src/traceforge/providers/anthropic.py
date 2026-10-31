"""Anthropic Messages API adapter using standard-library HTTP."""

import json
import os
from urllib.request import Request, urlopen

from traceforge.providers.base import Completion


class AnthropicProvider:
    """Call Anthropic's Messages endpoint with an environment API key."""

    def __init__(self, model: str, api_key: str | None = None, timeout: float = 30) -> None:
        self.model = model
        self.api_key = api_key or os.environ["ANTHROPIC_API_KEY"]
        self.timeout = timeout

    def complete(self, prompt: str) -> Completion:
        """Send one user message and normalize token usage metadata."""
        body = json.dumps(
            {
                "model": self.model,
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}],
            }
        ).encode()
        request = Request(
            "https://api.anthropic.com/v1/messages",
            data=body,
            headers={
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
        )
        with urlopen(request, timeout=self.timeout) as response:
            data = json.load(response)
        usage = data.get("usage", {})
        text = "".join(
            str(item.get("text", ""))
            for item in data.get("content", [])
            if item.get("type") == "text"
        )
        return {
            "text": text,
            "model": str(data.get("model", self.model)),
            "input_tokens": int(usage.get("input_tokens", 0)),
            "output_tokens": int(usage.get("output_tokens", 0)),
        }
