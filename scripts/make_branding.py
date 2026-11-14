"""Generate the BoxFab branding files for the desktop template (run by hand, output is committed).

  uv run --no-project --with pillow python scripts/make_branding.py

Writes overlay/template/files/wallpaper.png (replaces upstream's E2B wallpaper) and
overlay/template/files/novnc-icons/ (favicons, app icons and the web manifest for the noVNC
stream page; same file names as upstream's icons/e2b/ set). The wordmark is plain text until
BoxFab has a logo: replace the drawing code here and rerun.
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "overlay/template/files"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BG, FG = (11, 11, 12), (245, 245, 245)
NAME, SHORT = "BoxFab Desktop", "BoxFab"


def wallpaper(w=2048, h=1536):
    OUT.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT, 160)
    box = d.textbbox((0, 0), SHORT, font=font)
    tw, th = box[2] - box[0], box[3] - box[1]
    d.text(((w - tw) / 2 - box[0], (h - th) / 2 - box[1]), SHORT, font=font, fill=FG)
    img.save(OUT / "wallpaper.png", optimize=True)


def icon(size: int, dark: bool = False) -> Image.Image:
    bg, fg = (FG, BG) if dark else (BG, FG)
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=max(2, size // 5), fill=bg)
    font = ImageFont.truetype(FONT, int(size * 0.7))
    box = d.textbbox((0, 0), "B", font=font)
    tw, th = box[2] - box[0], box[3] - box[1]
    d.text(((size - tw) / 2 - box[0], (size - th) / 2 - box[1]), "B", font=font, fill=fg)
    return img


def svg(bg, fg) -> str:
    hexc = lambda c: "#%02x%02x%02x" % c
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">\n'
            f'  <rect width="32" height="32" rx="6" fill="{hexc(bg)}"/>\n'
            f'  <text x="16" y="23.5" text-anchor="middle" font-family="DejaVu Sans, Verdana, sans-serif" '
            f'font-weight="700" font-size="22" fill="{hexc(fg)}">B</text>\n</svg>\n')


def icons():
    d = OUT / "novnc-icons"
    d.mkdir(parents=True, exist_ok=True)
    pngs = {f"android-icon-{s}x{s}.png": s for s in (36, 48, 72, 96, 144, 192)}
    pngs |= {f"apple-icon-{s}x{s}.png": s for s in (57, 60, 72, 76, 114, 120, 144, 152, 180)}
    pngs |= {"apple-icon.png": 192, "apple-icon-precomposed.png": 192}
    pngs |= {f"favicon-{s}x{s}.png": s for s in (16, 32, 96)}
    pngs |= {f"ms-icon-{s}x{s}.png": s for s in (70, 144, 150, 310)}
    for name, s in pngs.items():
        icon(s).save(d / name, optimize=True)
    icon(48).save(d / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    (d / "favicon.svg").write_text(svg(BG, FG))
    (d / "favicon-dark.svg").write_text(svg(FG, BG))
    manifest = {"name": NAME, "short_name": SHORT, "icons": [
        {"src": f"android-icon-{s}x{s}.png", "sizes": f"{s}x{s}", "type": "image/png"}
        for s in (36, 48, 72, 96, 144, 192)]}
    (d / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")


if __name__ == "__main__":
    wallpaper()
    icons()
    print("wrote", OUT / "wallpaper.png", "and", OUT / "novnc-icons")
