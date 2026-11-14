# Changelog

## Unreleased

- README "Under the hood": using the E2B Desktop SDKs with BoxFab (`E2B_DOMAIN` and `E2B_API_KEY`),
  tested with `e2b-desktop` 2.7.2 (Python) and `@e2b/desktop` 2.5.0 (JavaScript).
- The repository holds the desktop sandbox template and the examples, like `e2b-dev/desktop`. The
  SDKs moved next to the core SDKs: `boxfab-desktop` to
  [boxfab/python-sdk](https://github.com/boxfab/python-sdk/tree/main/desktop) and
  `@boxfab/desktop` to [boxfab/js-sdk](https://github.com/boxfab/js-sdk/tree/main/desktop).
- License: Apache-2.0 for the whole repository (`LICENSE`, upstream's text).
- README generated from upstream's, with a BoxFab introduction and screenshot.
- Examples: `streaming-apps-python` and `streaming-apps-javascript` (from upstream, renamed), and
  `computer-use-claude-python` (Claude operating the desktop with the computer toolset).
- Template generated from `e2b-dev/desktop` `91f23aca`, built with the BoxFab SDK, with BoxFab
  branding: wallpaper, noVNC page title and icons (noVNC pinned to `af7c2d17`), and the hostname
  `boxfab.local` (prompt `user@boxfab`). It is the platform's `desktop` template since 2026-11-13.
