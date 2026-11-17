"""Adds a paper from arXiv: writes _papers/<id>.md and, with --week, puts it on the schedule.

Title, authors, year and license come from arXiv, so nothing is typed by hand. The TL;DR is left
for the class, like every other week.

Usage:
  python3 bin/add_paper.py 2610.08718 --week 5
  python3 bin/add_paper.py 2610.08718 --week 5 --id spurious-forgetting --short "Spurious forgetting"
  python3 bin/add_paper.py 2610.08718 --dry-run      # print what it would write, change nothing

Without --week the page is written but the paper is not scheduled. A week that already has a
paper is left alone unless you pass --replace. Comments under the week in schedule.yml are kept.
"""
import argparse
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "_papers"
SCHEDULE = ROOT / "_data" / "schedule.yml"
ATOM = "{http://www.w3.org/2005/Atom}"
UA = {"User-Agent": "active-ai-reading add_paper.py"}

LICENSES = {
    "by/4.0": "CC BY 4.0",
    "by-sa/4.0": "CC BY-SA 4.0",
    "by-nc-sa/4.0": "CC BY-NC-SA 4.0",
    "by-nc-nd/4.0": "CC BY-NC-ND 4.0",
    "by-nc/4.0": "CC BY-NC 4.0",
    "by-nd/4.0": "CC BY-ND 4.0",
    "zero/1.0": "CC0 1.0",
}


def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read().decode("utf-8")


def arxiv_id(raw):
    """Accepts 2610.08718, 2610.08718v2, or an arxiv.org abs/pdf link; returns 2610.08718."""
    m = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", raw)
    if not m:
        sys.exit(f"Not an arXiv id: {raw}")
    return m.group(1)


def metadata(aid):
    entry = ET.fromstring(fetch(f"https://export.arxiv.org/api/query?id_list={aid}")).find(f"{ATOM}entry")
    title = entry.findtext(f"{ATOM}title") if entry is not None else None
    if not title or entry.findtext(f"{ATOM}id", "").endswith("api/errors"):
        sys.exit(f"arXiv has no paper {aid}")
    meta = {
        "title": " ".join(title.split()),
        "authors": [" ".join(a.findtext(f"{ATOM}name").split()) for a in entry.findall(f"{ATOM}author")],
        "year": int(entry.findtext(f"{ATOM}published")[:4]),
        "license": None,
    }
    # The API does not give the license; the abstract page links to it.
    try:
        m = re.search(r"creativecommons\.org/(?:licenses|publicdomain)/([a-z-]+/\d\.\d)", fetch(f"https://arxiv.org/abs/{aid}"))
        if m:
            meta["license"] = LICENSES.get(m.group(1))
    except OSError:
        pass
    return meta


def slugify(title):
    head = re.split(r"[:?]", title)[0]
    words = re.findall(r"[a-z0-9]+", head.lower())
    return "-".join(words[:5])


def short_name(title):
    head = re.split(r"[:?]", title)[0].strip()
    words = head.split()
    return head if len(words) <= 5 else " ".join(words[:4])


def yaml_str(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"' if re.search(r"[:#\"'\[\]{}&*!|>%@`]", s) else s


def page(meta, aid, short, week):
    after = f"after week {week}" if week is not None else "after we read it"
    lines = [
        "---",
        f"title: {yaml_str(meta['title'])}",
        f"short: {yaml_str(short)}",
        f"authors: {', '.join(meta['authors'])}",
        f"year: {meta['year']}",
        f'arxiv: "{aid}"',
    ]
    if meta["license"]:
        lines.append(f"license: {meta['license']}")
    lines += [
        "tldr: >",
        f"  (To be written by the class {after}. Edit this file: one or two sentences someone can read in 10 seconds.)",
        "tags: []",
        "---",
        "",
    ]
    return "\n".join(lines)


def schedule_with(text, week, pid, replace):
    """Sets `paper: pid` on `- week: <week>`, keeping every other line (comments included)."""
    lines = text.splitlines(keepends=True)
    start = next((i for i, l in enumerate(lines) if re.fullmatch(rf"- week: {week}\s*", l)), None)
    if start is None:
        sys.exit(f"_data/schedule.yml has no week {week}")
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("- ")), len(lines))
    for i in range(start + 1, end):
        m = re.match(r"  paper:\s*(\S+)?", lines[i])
        if m:
            if m.group(1) and m.group(1) != pid and not replace:
                sys.exit(f"Week {week} already reads {m.group(1)}. Pass --replace to change it.")
            lines[i] = f"  paper: {pid}\n"
            return "".join(lines)
    lines.insert(start + 1, f"  paper: {pid}\n")
    return "".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("arxiv", help="arXiv id or link, e.g. 2610.08718")
    ap.add_argument("--week", type=int, help="the meeting to read it at (week number in _data/schedule.yml)")
    ap.add_argument("--id", help="the page id and filename; default: built from the title")
    ap.add_argument("--short", help="2-4 word name for cards; default: the title before any colon")
    ap.add_argument("--replace", action="store_true", help="replace the paper already on that week")
    ap.add_argument("--dry-run", action="store_true", help="print what would be written, change nothing")
    args = ap.parse_args()

    aid = arxiv_id(args.arxiv)
    for f in PAPERS.glob("*.md"):
        if re.search(rf'^arxiv:\s*"?{re.escape(aid)}"?\s*$', f.read_text(encoding="utf-8"), re.M):
            sys.exit(f"{aid} is already {f.relative_to(ROOT)}. To schedule it, set `paper: {f.stem}` on the week.")
    meta = metadata(aid)
    pid = args.id or slugify(meta["title"])
    target = PAPERS / f"{pid}.md"
    if target.exists():
        sys.exit(f"{target.relative_to(ROOT)} already exists. Pass a different --id.")
    content = page(meta, aid, args.short or short_name(meta["title"]), args.week)
    new_schedule = schedule_with(SCHEDULE.read_text(encoding="utf-8"), args.week, pid, args.replace) if args.week is not None else None

    if args.dry_run:
        print(f"--- would write {target.relative_to(ROOT)}\n{content}")
        if new_schedule:
            print(f"--- would set week {args.week} in _data/schedule.yml to paper: {pid}")
        return
    target.write_text(content, encoding="utf-8")
    print(f"Wrote {target.relative_to(ROOT)}: {meta['title']}")
    if new_schedule:
        SCHEDULE.write_text(new_schedule, encoding="utf-8")
        print(f"Week {args.week} in _data/schedule.yml now reads {pid}")
    if not meta["license"]:
        print("No Creative Commons license found on arXiv: don't reuse its figures.")


if __name__ == "__main__":
    main()
