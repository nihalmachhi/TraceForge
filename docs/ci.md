# CI, releases, and Pages

The `ci` workflow runs lint, formatting, strict typing, coverage, and the
regression gate across Ubuntu, Windows, and macOS with Python 3.11–3.13. Set
the `ci` job as a required status check in repository branch protection.

Tags beginning with `v` build distributions and publish GitHub Releases. PyPI
trusted publishing requires registering this repository and workflow as the
publisher on PyPI.

## Pages

The `pages` workflow builds `site/` with Vite, uploads `site/dist`, and deploys
it on every push to `main` that touches `site/**` or the workflow itself. The
live site is <https://nihalmachhi.github.io/TraceForge/>.

Pages must be enabled once per repository with **Source: GitHub Actions**. On
this repository that is already configured (`build_type: workflow`). For a
fork, either flip the setting under **Settings → Pages** or run the workflow
with a token that has repository admin rights.

`actions/configure-pages` runs with `enablement: true` so a fresh repository can
try to switch Pages on during the first deploy. `GITHUB_TOKEN` is not allowed to
create a Pages site, so that call fails with `Resource not accessible by
integration` until Pages is enabled. The error is a repository setting, not a
build failure: `python -m traceforge demo` and `npm run build` both succeed
before it. Use a personal access token with `repo` scope, or enable Pages in the
UI, and re-run the workflow.

The workflow installs the package in editable mode so `traceforge.config` finds
`datasets/faq_v1.json` in the checkout instead of the bundled copy. Both paths
work, but the editable install keeps the generated report identical to the one
produced by a local `make demo`.
