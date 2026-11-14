# BoxFab Desktop

A virtual Linux desktop in the cloud, ready for computer-use agents: each desktop runs in its own
isolated [BoxFab](https://boxfab.io) sandbox, controlled from Python or JavaScript (mouse,
keyboard, screenshots, application windows) and viewable live in the browser.

![BoxFab Desktop](readme-assets/screenshot.png)

This repository holds the desktop sandbox template and the examples. The SDKs live next to the
core BoxFab SDKs: [`boxfab-desktop`](https://github.com/boxfab/python-sdk/tree/main/desktop)
(Python) and [`@boxfab/desktop`](https://github.com/boxfab/js-sdk/tree/main/desktop)
(JavaScript / TypeScript).

## Examples

- Streaming desktop applications:
  - [Python](./examples/streaming-apps-python)
  - [JavaScript](./examples/streaming-apps-javascript)
- Computer use with Claude: [Python](./examples/computer-use-claude-python)

## Getting started

### 1. Get a BoxFab API key

Get a key from the [BoxFab dashboard](https://dashboard.boxfab.io) and set it as
`BOXFAB_API_KEY`.

### 2. Install the SDK

**Python**

```bash
pip install boxfab-desktop
```

**JavaScript**

```bash
npm install @boxfab/desktop
```

> **Stream access.** The stream runs without a password unless you pass `require_auth=True`
> (Python) or `requireAuth: true` (JavaScript). The stream URL contains the sandbox ID, and anyone
> who has the URL can see and control the desktop. Require auth whenever the URL leaves your
> backend, and share the URL with the auth key only with the intended viewer.

