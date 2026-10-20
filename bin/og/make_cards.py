"""Draw a social-media preview card (1200x630) for every post and paper.

Runs in the deploy workflow before the site is built; the cards are written to
assets/og/ and are not committed. _includes/metadata.liquid points og:image at
them. A post or paper with its own `og_image:` in the header keeps that instead.

Run locally:  pip install pillow pyyaml && python bin/og/make_cards.py
"""
import pathlib
import re

import yaml
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "og"
FONT = str(pathlib.Path(__file__).with_name("Inter.ttf"))
W, H, PAD = 1200, 630, 80
BG, INK, SOFT = (255, 252, 248), (24, 24, 27), (90, 90, 100)
SITE = "Active AI Reading"


def font(size, weight):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_axes([14, weight]) if len(f.get_variation_axes()) == 2 else f.set_variation_by_axes([weight])
    return f


def front_matter(path):
    m = re.match(r"^---\s*\n(.*?)\n---", path.read_text(encoding="utf-8"), re.S)
    try:
        return (yaml.safe_load(m.group(1)) or {}) if m else {}
    except yaml.YAMLError:
        return {}


def hex_rgb(h):
    h = str(h).lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4)) if len(h) == 6 else (194, 65, 12)


def wrap(draw, text, f, width, max_lines):
    words, lines, line = str(text).split(), [], ""
    for w in words:
        trial = f"{line} {w}".strip()
        if draw.textlength(trial, font=f) <= width:
            line = trial
        else:
            lines.append(line)
            line = w
    lines.append(line)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while draw.textlength(lines[-1] + "…", font=f) > width:
            lines[-1] = lines[-1].rsplit(" ", 1)[0]
        lines[-1] += "…"
    return lines


def card(path, title, kicker, kicker_color, footer):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 18, H], fill=kicker_color)
    y = PAD
    if kicker:
        d.text((PAD, y), kicker, font=font(34, 650), fill=kicker_color)
        y += 70
    for size, lines_max in ((72, 3), (60, 4), (50, 5)):
        tf = font(size, 750)
        lines = wrap(d, title, tf, W - 2 * PAD, lines_max)
        if not lines[-1].endswith("…") or size == 50:
            break
    for line in lines:
        d.text((PAD, y), line, font=tf, fill=INK)
        y += int(size * 1.18)
    if footer:
        ff = font(30, 450)
        d.text((PAD, H - PAD - 70), wrap(d, footer, ff, W - 2 * PAD, 1)[0], font=ff, fill=SOFT)
    d.text((PAD, H - PAD - 10), SITE, font=font(30, 700), fill=(194, 65, 12))
    img.save(path, optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    roles = {r["id"]: r for r in yaml.safe_load((ROOT / "_data" / "roles.yml").read_text(encoding="utf-8"))}
    papers = {p.stem: front_matter(p) for p in (ROOT / "_papers").glob("*.md")}
    n = 0
    for p in sorted((ROOT / "_posts").glob("*.md")):
        fm = front_matter(p)
        if not fm.get("title"):
            continue
        role = roles.get(fm.get("role"), {})
        task = next((t for t in role.get("tasks", []) if t.get("id") == fm.get("task")), {})
        kicker = " · ".join(x for x in (role.get("name"), task.get("name")) if x)
        paper = papers.get(str(fm.get("paper")), {})
        footer = f"On: {paper['title']}" if paper.get("title") else ""
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", p.stem)
        card(OUT / f"{slug}.png", fm["title"], kicker, hex_rgb(role.get("color", "#c2410c")), footer)
        n += 1
    for slug, fm in papers.items():
        if fm.get("title"):
            card(OUT / f"paper-{slug}.png", fm["title"], "Paper", (194, 65, 12), fm.get("authors", ""))
            n += 1
    print(f"made {n} cards in {OUT}")


if __name__ == "__main__":
    main()
