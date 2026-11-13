# Upstream

BoxFab Desktop is derived from the open-source E2B Desktop: the SDKs
[`packages/desktop-python`](https://github.com/e2b-dev/E2B/tree/main/packages/desktop-python) and
[`packages/desktop-js`](https://github.com/e2b-dev/E2B/tree/main/packages/desktop-js) in the E2B
monorepo (MIT), and the sandbox template in
[`e2b-dev/desktop`](https://github.com/e2b-dev/desktop/tree/main/template) (Apache-2.0). It
includes modifications for BoxFab's sandbox infrastructure. BoxFab is an independent project and
is not affiliated with or endorsed by E2B.

## Pinned sources

- Monorepo commit: `3a904178b2f1d1c40fd2ba1c2ad9a10f43896bf1`
  - `e2b-desktop` 2.7.2 and `@e2b/desktop` 2.5.0. The desktop code at this commit is identical to
    their release tags (`@e2b/desktop-python@2.7.2` = `d7c022e9`, `@e2b/desktop@2.5.0` =
    `62a17dfc`).
  - The same commit `boxfab` 0.1.0a2 (Python) is generated from (`e2b` 2.62.0). The JS package
    depends on `boxfab` 0.1.0-alpha.2, generated from `e2b` 2.61.0 (`ee355b76`), where the desktop
    JS code is also identical.
- Desktop repo commit: `91f23acaab7312e847596acc44e6f7763f56917f` (`e2b-dev/desktop` main,
  2026-11-02)
- noVNC commit: `af7c2d17a92b04025a0b91c21b45dcbf7d3ff5e8` (`e2b-dev/noVNC` branch `e2b-desktop`,
  2026-10-30; the template clones this commit, the script does not fetch it)

The script checks that the checkouts it is given are at these commits.

## How the code is produced

`scripts/sync_upstream.py` writes these paths, which are never edited by hand:

| path | from |
|---|---|
| `python/boxfab_desktop/`, `python/tests/`, `python/pytest.ini`, `python/CHANGELOG-E2B.md` | `packages/desktop-python` |
| `js/src/`, `js/tests/` (without `tests/runtimes/`), `js/CHANGELOG-E2B.md` | `packages/desktop-js` |
| `python/README.md`, `js/README.md` | our introduction (`overlay/readme/`), then upstream's README from "3. Create Desktop Sandbox" on |
| `template/template.py`, `template/build_*.py`, `template/files/` | `e2b-dev/desktop` `template/`; `overlay/template/files/` (our `wallpaper.png` and `novnc-icons/`, made by `scripts/make_branding.py`) is copied over it |
| `LICENSE-E2B` (MIT), `LICENSE-E2B-DESKTOP` (Apache-2.0), and `LICENSE`, `LICENSE-E2B` copied into `python/` and `js/` | upstream license files |

`overlay/js/tests/boxfab-env.setup.ts` (from `boxfab/js-sdk`) is copied in as a test setup file: it
stops a test run that is pointed at an E2B domain.

Every rule asserts how often it matched. A final audit fails the sync if generated code still has
an `e2b` import, the upstream package name, an `E2B_*` configuration variable or an E2B domain.

## Rewrites (first release: renames only)

| Change | Where | Why |
|---|---|---|
| package `e2b_desktop` → `boxfab_desktop`; `@e2b/desktop` → `@boxfab/desktop` (distribution `boxfab-desktop`) | Python, JS, READMEs | distribution and import name |
| SDK imports `e2b` → `boxfab` | Python, JS, template build scripts | the `boxfab` SDK reads only `BOXFAB_*` and defaults to `boxfab.io`, so a BoxFab install never picks up an E2B key or domain |
| `E2B_*` variables read by tests (`API_KEY`, `DOMAIN`, `DEBUG`, `API_URL`, `SANDBOX_URL`) → `BOXFAB_*` | tests | tests exercise BoxFab only |
| client class `E2B` → `BoxFab`, `E2BClientParams` / `E2BClientOpts` → `BoxFab*`; the upstream names stay exported as aliases | Python, JS | branding; existing code ports by changing the import |
| client doc comment and example: "BoxFab client", `domain="boxfab.io"` | Python, JS | the docs users read in their editor |
| live tests take the template from `BOXFAB_DESKTOP_TEMPLATE` (default: the SDK's `desktop`) | tests | run before `desktop` is a BoxFab default |
| `tests/runtimes/` (Cloudflare Workers smoke suite) removed | JS tests | needs its own toolchain and deploy target |
| a "Modified by ContextFab, Inc." notice at the top of each generated template script | template | Apache-2.0 §4(b) |
| noVNC cloned at the pinned commit instead of following the `e2b-desktop` branch | template | reproducible builds |
| wallpaper, the noVNC page title ("BoxFab Desktop") and its favicons, app icons and web manifest | template | branding; the template's last step fails the build if `vnc.html` still mentions E2B |
| hostname `boxfab.local` (`hostname`, `/etc/hostname`, `/etc/hosts`), so the prompt reads `user@boxfab` | template | BoxFab's runtime names every sandbox `e2b.local`; drop this step once the runtime sets `boxfab.local` itself |

## Deliberately unchanged

- **Stream auth stays off by default** (`stream.start(require_auth=False)` / `requireAuth: false`),
  as upstream. Our READMEs advise `require_auth=True` whenever the stream URL leaves the caller's
  backend. Reasoning:
  - The stream URL (`https://6080-<sandbox id>.boxfab.io/vnc.html`) contains the unguessable
    sandbox ID, like every sandbox port.
  - BoxFab serves sandbox hosts through wildcard DNS and a wildcard certificate, so IDs don't
    appear in DNS or certificate-transparency logs.
  - With auth on, `get_url(auth_key=…)` puts the password in the URL query.
  - Header-based protection (`network={"allow_public_traffic": False}` in the core SDK) can't be
    used by a browser iframe.
  - The stream runs only after `stream.start()`; agents use screenshots and input through the SDK.
- The default template name `desktop`, display `:0`, 1024x768 at 96 DPI, ports 5900 (VNC) and 6080
  (noVNC), the `x11vnc` / `novnc_proxy` command lines, and every mouse, keyboard and window method.
- The template: base image, package list, noVNC from `e2b-dev/noVNC` (its UI changes, including the
  orange accent colour, apart from the title and icons), websockify `v0.12.0`, the Google / Microsoft / Mozilla apt sources, 8 vCPU / 8 GiB, aliases
  `desktop` and `desktop-dev`.
- Wire-level identifiers: the `e2b_` API-key prefix in test fixtures, and everything the core SDK
  leaves alone (see `boxfab/python-sdk` and `boxfab/js-sdk` `UPSTREAM.md`).
- Upstream's tests, apart from the renames above.

## Licensing

- The SDK packages are MIT (`LICENSE-E2B`, "Copyright (c) 2025 FOUNDRYLABS, INC.").
- The template is Apache-2.0 (`LICENSE-E2B-DESKTOP`). Neither upstream ships a NOTICE file.
- BoxFab's changes are MIT (`LICENSE`, Copyright (c) 2026 ContextFab, Inc.). The Python wheel and
  the npm package include `LICENSE` and `LICENSE-E2B`.

## Updating

1. Put the new commits in "Pinned sources" above: a monorepo commit where the core SDK version
   matches a `boxfab` release, and an `e2b-dev/desktop` commit.
2. `python3 scripts/sync_upstream.py` (or `--monorepo <checkout> --desktop <checkout>`). A failing
   rule means upstream moved the code it targets: adjust the rule, not the generated files.
3. Review `git diff`, run the offline tests, then the live tests against BoxFab, and update
   `CHANGELOG.md`.
