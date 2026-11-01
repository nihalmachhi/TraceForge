# Contributing to TraceForge

Thanks for taking a look. TraceForge is a small, dependency-free tracing and evaluation toolkit,
so the bar is simple: keep the core standard-library only, keep changes typed and tested, and keep
claims honest.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

For the dashboard:

```bash
cd site
npm ci
npm run build
```

## Before opening a pull request

Run all three checks locally:

```bash
make lint
make types
make test
```

Equivalent commands:

```bash
python -m ruff check src tests scripts
python -m ruff format --check src tests scripts
python -m mypy --strict src
python -m pytest --cov --cov-fail-under=85
```

CI runs the same checks on Ubuntu, Windows, and macOS across Python 3.11, 3.12, and 3.13.

## Conventions

- Python 3.11+, type hints everywhere, docstrings on public APIs.
- Lines are limited to 100 characters.
- The core package must not gain runtime dependencies. Put optional integrations behind extras in
  `pyproject.toml`.
- Every behavior change needs a regression test.
- Never commit secrets, `.env` files, generated SQLite databases, or `data/generated/` artifacts.
- Use Conventional Commits: `feat:`, `fix:`, `test:`, `docs:`, `ci:`, `refactor:`, `chore:`.

## Pull requests

1. Branch from `main` (`feat/short-name` or `fix/short-name`).
2. Keep one logical change per commit.
3. Describe the behavior change, the test that proves it, and any trade-offs.
4. Make sure the `ci` workflow is green before requesting review.

## Reporting bugs

Open an issue with the command you ran, the expected result, the actual result, and the Python
version and operating system. Do not include real credentials or customer data.
