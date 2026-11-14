# Computer use with Claude (Python)

Claude operates a BoxFab desktop: it sees screenshots, decides on actions (click, type, press keys,
scroll), and `main.py` carries them out in the sandbox with `boxfab-desktop`, until the task is
done. You can watch the desktop live in the browser while it works.

It uses the Claude API's computer toolset (`computer_toolset_20260801`) with Claude Opus 5.5.

## How to run

### 1. Get the API keys

- A BoxFab API key from the [BoxFab dashboard](https://dashboard.boxfab.io), as `BOXFAB_API_KEY`.
- An Anthropic API key from the [Claude Console](https://console.anthropic.com), as
  `ANTHROPIC_API_KEY`.

### 2. Install and run

```bash
pip install boxfab-desktop anthropic
python main.py "Open Firefox, go to https://example.com and tell me the page title."
```

The script prints a stream URL (open it to watch), every action Claude takes, and Claude's final
answer, then deletes the sandbox.

## How it works

1. `Sandbox.create(resolution=(1280, 800))` starts a desktop sandbox. At that size, screenshots fit
   the model's image limit, so Claude's coordinates are used as they are.
2. Each turn sends the conversation, including the latest screenshots, to Claude with the computer
   toolset. Claude answers with one or more actions.
3. `act()` runs each action in order: mouse moves and clicks, typing and keys through the SDK and
   `xdotool`, and screenshots through `desktop.screenshot()`. Each result goes back to Claude; if
   an action fails, the rest of that turn is skipped, as the API requires.
4. When Claude replies without actions, its answer is printed and the sandbox is deleted.

Prompt caching (`cache_control`) keeps the cost of resending the growing history low: a short task
like the example above typically costs a few cents.
