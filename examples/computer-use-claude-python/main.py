"""Claude operates a BoxFab desktop: a minimal computer-use agent loop.

    pip install boxfab-desktop anthropic
    export BOXFAB_API_KEY=... ANTHROPIC_API_KEY=...
    python main.py "Open Firefox, go to https://example.com and tell me the page title."

Claude sees screenshots of the desktop and answers with actions (click, type, key, scroll, ...);
this script carries them out in the sandbox with boxfab-desktop and sends back the results, until
Claude stops calling tools. The desktop can be watched live at the printed stream URL.
"""

import base64
import shlex
import sys
import time

import anthropic
from boxfab_desktop import Sandbox

MODEL = "claude-opus-5-5"
SCREEN = (1280, 800)  # within the model's screenshot limit, so coordinates need no scaling
MAX_TURNS = 30
# The computer toolset; members this example does not implement are switched off.
TOOLS = [
    {
        "type": "computer_toolset_20260801",
        "configs": {m: {"enabled": False} for m in ("zoom", "hold_key", "left_mouse_down", "left_mouse_up")},
    }
]
SYSTEM = (
    "You are operating an Ubuntu Xfce desktop at 1280x800 through the computer tools. Firefox, "
    "Google Chrome, a terminal and the text editor gedit are installed. Applications can take a "
    "few seconds to open: take a screenshot to check before you continue. When the task is done, "
    "stop calling tools and reply with a short answer."
)
CLICKS = {"left_click": "1", "right_click": "3", "middle_click": "2",
          "double_click": "--repeat 2 1", "triple_click": "--repeat 3 1"}
SCROLL = {"up": "4", "down": "5", "left": "6", "right": "7"}


def screenshot(desktop: Sandbox) -> list:
    data = base64.standard_b64encode(bytes(desktop.screenshot())).decode()
    return [{"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": data}}]


def xdotool(desktop: Sandbox, args: str):
    desktop.commands.run(f"xdotool {args}")


def act(desktop: Sandbox, name: str, inp: dict):
    """Carry out one computer action and return the tool result content."""
    if name == "screenshot":
        return screenshot(desktop)
    if inp.get("coordinate") and name not in ("left_click_drag",):
        desktop.move_mouse(*map(int, inp["coordinate"]))
    mods = [m for m in (inp.get("text") or "").split("+") if m] if name in CLICKS or name == "scroll" else []
    for m in mods:  # modifier keys held during a click or scroll, e.g. "ctrl" or "shift"
        xdotool(desktop, f"keydown {shlex.quote(m)}")
    try:
        if name in CLICKS:
            xdotool(desktop, f"click {CLICKS[name]}")
        elif name == "scroll":
            xdotool(desktop, f"click --repeat {int(inp.get('scroll_amount', 1))} {SCROLL[inp['scroll_direction']]}")
        elif name == "left_click_drag":
            desktop.drag(tuple(map(int, inp["start_coordinate"])), tuple(map(int, inp["coordinate"])))
        elif name == "mouse_move":
            pass  # moved above
        elif name == "type":
            desktop.write(inp["text"])
        elif name == "key":  # xdotool key names, e.g. "Return" or "ctrl+l"
            xdotool(desktop, f"key --repeat {int(inp.get('repeat', 1))} {shlex.quote(inp['text'])}")
        elif name == "wait":
            time.sleep(float(inp["duration"]))
        elif name == "cursor_position":
            x, y = desktop.get_cursor_position()
            return f"[{x}, {y}]"
        else:
            raise ValueError(f"{name} is not supported by this example")
    finally:
        for m in reversed(mods):
            xdotool(desktop, f"keyup {shlex.quote(m)}")
    return "OK"


def main(task: str):
    client = anthropic.Anthropic()
    desktop = Sandbox.create(resolution=SCREEN, timeout=900)
    try:
        desktop.stream.start(require_auth=True)
        print("Watch live:", desktop.stream.get_url(auth_key=desktop.stream.get_auth_key()))
        messages = [{"role": "user", "content": task}]
        for _ in range(MAX_TURNS):
            response = client.messages.create(
                model=MODEL, max_tokens=8192, system=SYSTEM, tools=TOOLS, messages=messages,
                cache_control={"type": "ephemeral"},  # the history is resent every turn
            )
            messages.append({"role": "assistant", "content": response.content})
            calls = [b for b in response.content
                     if b.type == "tool_use" and getattr(b, "toolset_name", None) == "computer"]
            if not calls:
                print("Claude:", " ".join(b.text for b in response.content if b.type == "text").strip())
                return
            results, failed = [], False
            for call in calls:  # run in order; after a failure, the rest of the turn is skipped
                result = {"type": "tool_result", "tool_use_id": call.id, "toolset_name": "computer"}
                if failed:
                    result.update(content="Not executed: an earlier computer action in this turn failed.", is_error=True)
                else:
                    try:
                        result["content"] = act(desktop, call.name, call.input)
                    except Exception as e:
                        result.update(content=f"Error: {e}", is_error=True)
                        failed = True
                print(f"  {call.name} {call.input if call.input else ''}")
                results.append(result)
            messages.append({"role": "user", "content": results})
        print(f"Stopped after {MAX_TURNS} turns")
    finally:
        desktop.kill()


if __name__ == "__main__":
    main(" ".join(sys.argv[1:]) or "Open Firefox, go to https://example.com and tell me the page title.")
