# BoxFab Desktop

A virtual Linux desktop in a [BoxFab](https://boxfab.dev) sandbox, for computer-use agents.

| part | package | docs |
|---|---|---|
| Python SDK | `boxfab-desktop` (import `boxfab_desktop`) | [python/README.md](python/README.md) |
| JavaScript / TypeScript SDK | `@boxfab/desktop` | [js/README.md](js/README.md) |
| Sandbox template (`desktop`) | built on BoxFab | [template/README.md](template/README.md) |

BoxFab Desktop is derived from the open-source [E2B Desktop](https://github.com/e2b-dev/desktop)
and includes modifications for BoxFab's sandbox infrastructure. BoxFab is an independent project
and is not affiliated with or endorsed by E2B. What is generated from upstream, and how, is in
[UPSTREAM.md](UPSTREAM.md).

## Development

```bash
python3 scripts/sync_upstream.py        # regenerate the upstream-derived files (pins in UPSTREAM.md)

cd python && uv sync && uv run pytest tests/test_client.py tests/test_readiness.py   # offline
cd js && npm ci && npm run build && npm test                                          # offline

# live, against BoxFab: a key and a desktop template
export BOXFAB_API_KEY=e2b_*** BOXFAB_DESKTOP_TEMPLATE=desktop-dev
cd python && uv run pytest tests/test_controls.py
cd js && npm run test:live
```

Generated files are never edited by hand; change a rule in `scripts/sync_upstream.py` instead.

## License

MIT for BoxFab's changes and the SDKs (`LICENSE`, `LICENSE-E2B`); the template is Apache-2.0
(`LICENSE-E2B-DESKTOP`).
