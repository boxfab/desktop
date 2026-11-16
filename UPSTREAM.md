# Upstream

The template, the README and the streaming examples in this repository are derived from the
open-source [E2B Desktop](https://github.com/e2b-dev/desktop) project (Apache-2.0) and include
modifications for BoxFab. The desktop SDKs are derived from the E2B Desktop SDKs (MIT) and are
generated in [boxfab/python-sdk](https://github.com/boxfab/python-sdk/tree/main/desktop) and
[boxfab/js-sdk](https://github.com/boxfab/js-sdk/tree/main/desktop), from the same upstream commit
as the core BoxFab SDKs. BoxFab is an independent project and is not affiliated with or endorsed by
E2B.

## Pinned sources

- Desktop repo commit: `91f23acaab7312e847596acc44e6f7763f56917f` (`e2b-dev/desktop` main,
  2026-11-02)
- noVNC commit: `af7c2d17a92b04025a0b91c21b45dcbf7d3ff5e8` (`e2b-dev/noVNC` branch `e2b-desktop`,
  2026-10-30; the template clones this commit, the script does not fetch it)

The script checks that the checkout it is given is at the pinned commit.

## How the files are produced

`scripts/sync_upstream.py` writes these paths, which are never edited by hand:

| path | from |
|---|---|
| `template/template.py`, `template/build_*.py`, `template/files/` | `e2b-dev/desktop` `template/`; `overlay/template/files/` (our `wallpaper.png` and `novnc-icons/`, made by `scripts/make_branding.py`) is copied over it |
| `README.md` | our introduction (`overlay/readme/header.md`), upstream's README from "3. Create Desktop Sandbox" on, renamed, with our paragraphs in "Under the hood" (`overlay/readme/under-the-hood.md`) and the License section (`overlay/readme/footer.md`) |
| `examples/streaming-apps-python/README.md`, `examples/streaming-apps-javascript/README.md` | upstream's examples of the same name, renamed |

`LICENSE` is upstream's Apache-2.0 text; the script checks it is unchanged. This repository's own
files: `template/pyproject.toml`, `template/README.md`, `examples/computer-use-claude-python/`,
`readme-assets/screenshot.png` (taken in a BoxFab desktop sandbox), `overlay/`, `scripts/`, this
file and `CHANGELOG.md`.

Every rule asserts how often it matched. A final audit fails the sync if a generated file still
has an `e2b` import, an upstream package name, an `E2B_*` configuration variable or an E2B domain.

## Rewrites

| Change | Where | Why |
|---|---|---|
| SDK imports `e2b` → `boxfab` | template build scripts | built with the BoxFab SDK |
| a "Modified by ContextFab, Inc." notice at the top of each generated file | template scripts, READMEs | Apache-2.0 §4(b) |
| noVNC cloned at the pinned commit instead of following the `e2b-desktop` branch | template | reproducible builds |
| wallpaper, the noVNC page title ("BoxFab Desktop") and its favicons, app icons and web manifest | template | branding; the template's last step fails the build if `vnc.html` still mentions E2B |
| hostname `boxfab.local` (`hostname`, `/etc/hostname`, `/etc/hosts`), so the prompt reads `user@boxfab` | template | BoxFab's runtime names every sandbox `e2b.local`; drop this step once the runtime sets `boxfab.local` itself |
| package names `e2b_desktop` / `@e2b/desktop` → `boxfab_desktop` / `@boxfab/desktop`, install commands, API key instructions | README, examples | the BoxFab packages |
| the screenshots in the streaming examples are left out | examples | upstream's show E2B's domain in the address bar |
| the basic examples (pywebview / Electron windows) are not included | examples | they need desktop GUI toolkits only to open a window; the streaming examples show the same |

## Deliberately unchanged

- **Stream auth stays off by default** (`stream.start(require_auth=False)` / `requireAuth: false`),
  as upstream. The READMEs advise requiring auth whenever the stream URL leaves the caller's
  backend. Reasoning:
  - The stream URL (`https://6080-<sandbox id>.us-west.boxfab.dev/vnc.html`) contains the unguessable
    sandbox ID, like every sandbox port.
  - BoxFab serves sandbox hosts through wildcard DNS and a wildcard certificate, so IDs don't
    appear in DNS or certificate-transparency logs.
  - With auth on, `get_url(auth_key=…)` puts the password in the URL query.
  - The stream runs only after `stream.start()`; agents use screenshots and input through the SDK.
- The template: base image, package list, noVNC from `e2b-dev/noVNC` (its UI, including the orange
  accent colour, apart from the title and icons), websockify `v0.12.0`, the Google / Microsoft /
  Mozilla apt sources, 8 vCPU / 8 GiB, aliases `desktop` and `desktop-dev`.
- The README's API sections (Features, Under the hood, Customizing the template), apart from the
  package names.

## Updating

1. Put the new `e2b-dev/desktop` commit in "Pinned sources" above.
2. `python3 scripts/sync_upstream.py` (or `--desktop <checkout>`). A failing rule means upstream
   moved the text it targets: adjust the rule, not the generated files.
3. Review `git diff`, build `desktop-dev` and check it (hostname, wallpaper, noVNC title, the SDKs'
   live tests with `BOXFAB_DESKTOP_TEMPLATE=desktop-dev`), then update `CHANGELOG.md`.
