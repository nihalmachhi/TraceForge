# Local walkthrough

1. Install Python 3.11+ and Node.js 22+.
2. Run `python -m pip install -e ".[dev]"`.
3. Build the UI with `cd site && npm ci && npm run build`.
4. From the repository root, run `python -m traceforge demo`.
5. Run `python -m traceforge serve` and open `http://127.0.0.1:8000`.
6. Run `python -m traceforge gate` to inspect the intentional candidate
   regression (exit status 1 is expected for this sample).
