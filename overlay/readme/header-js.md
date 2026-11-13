# BoxFab Desktop (JavaScript / TypeScript)

A virtual Linux desktop (Xfce) in a [BoxFab](https://boxfab.dev) sandbox, ready for computer-use
agents: mouse, keyboard, screenshots, application windows, and a browser stream of the screen.

BoxFab Desktop is derived from the open-source [E2B Desktop](https://github.com/e2b-dev/desktop)
SDK and includes modifications for BoxFab's sandbox infrastructure. BoxFab is an independent
project and is not affiliated with or endorsed by E2B. Source:
[boxfab/desktop](https://github.com/boxfab/desktop) (`js/`).

## Getting started

### 1. Get a BoxFab API key

Get a key from your BoxFab administrator (keys are listed at https://dashboard.boxfab.io) and set
it as `BOXFAB_API_KEY`. The SDK reads only `BOXFAB_*` variables; `E2B_*` variables are ignored.

### 2. Install the SDK

```bash
npm install @boxfab/desktop
```

> **Stream access.** Like upstream, `desktop.stream.start()` runs without a password unless you
> pass `requireAuth: true`. The stream URL contains the sandbox ID, and anyone who has the URL can
> see and control the desktop. Pass `requireAuth: true` whenever the URL leaves your backend; the
> auth key is then part of the URL returned by `getUrl({ authKey })`, so share that URL only with
> the intended viewer.

