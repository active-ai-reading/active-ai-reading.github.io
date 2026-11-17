"""Lists posts that would be missing from their paper's page or their role, with the fix for each.

Usage: python3 bin/check_posts.py   (exit 1 if anything is listed; CI runs it on every push)
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def problems(text, papers, tasks):
    if not text.startswith("---"):
        return ["the file must start with the --- line, with nothing above it, or the site skips it"]
    m = re.match(r"---[ \t]*\r?\n(.*?)\r?\n---", text, re.S)
    if not m:
        return ["the header has no closing --- line"]
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        return [f"the header is not valid YAML: {str(e).splitlines()[0]}"]
    out = []
    if "paper" in fm and fm["paper"] not in papers:
        out.append(f"paper: {fm['paper']!r} is not one of: {', '.join(sorted(papers))}")
    if "task" in fm and fm["task"] not in tasks:
        out.append(f"task: {fm['task']!r} is not one of: {', '.join(sorted(tasks))}")
    return out


def main():
    papers = {p.stem for p in (ROOT / "_papers").glob("*.md")}
    roles = yaml.safe_load((ROOT / "_data" / "roles.yml").read_text(encoding="utf-8"))
    tasks = {t["id"] for r in roles for t in r.get("tasks", [])}
    found = 0
    for path in sorted((ROOT / "_posts").glob("*.md")):
        for p in problems(path.read_text(encoding="utf-8"), papers, tasks):
            print(f"_posts/{path.name}: {p}")
            found += 1
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
