"""Command-line entry points for the TraceForge toolkit."""

import argparse
import json
from collections.abc import Sequence

from traceforge.config import DB, REPORT
from traceforge.evaluation import gate, run_demo
from traceforge.storage.sqlite import SQLiteTraceStore
from traceforge.web import serve


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser and its supported commands."""
    parser = argparse.ArgumentParser(prog="traceforge")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("demo", help="record the deterministic sample evaluation")
    gate_parser = commands.add_parser("gate", help="evaluate the latest report")
    gate_parser.add_argument("--max-task-drop", type=float)
    gate_parser.add_argument("--max-groundedness-drop", type=float)
    serve_parser = commands.add_parser("serve", help="serve the dashboard on loopback")
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8000)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run one CLI command and return its process exit status."""
    args = build_parser().parse_args(argv)
    if args.command == "serve":
        serve(args.host, args.port)
        return 0
    if args.command == "demo":
        with SQLiteTraceStore(DB) as repository:
            report = run_demo(repository)
        print(json.dumps(report, indent=2))
        return 0
    if not REPORT.exists():
        print("Run `traceforge demo` first.")
        return 2
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    result = gate(report, args.max_task_drop, args.max_groundedness_drop)
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1
