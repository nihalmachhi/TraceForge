# CI, releases, and Pages

The `ci` workflow runs lint, formatting, strict typing, coverage, and the
regression gate across Ubuntu, Windows, and macOS with Python 3.11–3.13. Set
the `ci` job as a required status check in repository branch protection.

Tags beginning with `v` build distributions and publish GitHub Releases. PyPI
trusted publishing requires registering this repository and workflow as the
publisher on PyPI. The Pages workflow deploys `site/` using GitHub's Pages
artifact flow; select GitHub Actions as the Pages build source in repository
settings. Hosted checks and deployments can only be confirmed after push.
