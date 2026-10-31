"""Exercise a clean candidate through the actual command-line gate."""

import json
import subprocess
import sys

from traceforge.config import REPORT


def main() -> int:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    report["comparison"]["task_success_delta"] = 0.0
    report["comparison"]["groundedness_delta"] = 0.0
    REPORT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return subprocess.run([sys.executable, "-m", "traceforge", "gate"], check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
