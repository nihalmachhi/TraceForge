"""Ollama's local HTTP chat adapter using only the standard library."""

import json
from urllib.request import Request, urlopen

from traceforge.providers.base import Completion


class OllamaProvider:
    """Call a local Ollama server without third-party runtime packages."""

    def __init__(self, model: str = "llama3.2", base_url: str = "http://127.0.0.1:11434") -> None:
        self.model = model
        self.base_url = base_url.rstrip("/")

    def complete(self, prompt: str) -> Completion:
        """Generate a response; network errors propagate to the caller."""
        payload = json.dumps(
            {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            }
        ).encode()
        request = Request(
            f"{self.base_url}/api/chat", data=payload, headers={"Content-Type": "application/json"}
        )
        with urlopen(request, timeout=60) as response:
            data = json.load(response)
        return {
            "text": str(data["message"]["content"]),
            "model": str(data.get("model", self.model)),
            "input_tokens": int(data.get("prompt_eval_count", 0)),
            "output_tokens": int(data.get("eval_count", 0)),
        }
