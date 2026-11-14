# Notes for AI agents and reviewers

## Review guidelines

This repository holds the BoxFab desktop sandbox template, the examples and the README, derived
from the open-source E2B Desktop project. Several files are generated from upstream by
`scripts/sync_upstream.py` and then changed by a fixed set of asserted rewrites (see
`UPSTREAM.md`).

- **Generated paths are out of scope for behaviour review:** `template/template.py`,
  `template/build_*.py`, `template/files/`, `README.md`, `examples/streaming-apps-python/README.md`
  and `examples/streaming-apps-javascript/README.md`. Their content is upstream's apart from the
  listed rewrites; upstream issues are not fixed here. Do not report them.
- **Do review:** `scripts/` (the sync rules, the branding script), the rewrites in
  `scripts/sync_upstream.py` that change the template (noVNC pin, branding, hostname),
  `overlay/`, `examples/computer-use-claude-python/`, `template/pyproject.toml`, the workflows in
  `.github/workflows/` and the hand-written docs.
- Report concrete P1/P2 defects with the triggering input and effect; skip style.
