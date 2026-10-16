#!/usr/bin/env python3
"""Create a new build-log post skeleton with correct front matter and part number.

usage:
  new_post.py GITHUB_SITE SERIES DATE SLUG "Title text" [--time HH:MM] [--sections "A" "B" ...]

  SERIES  comet-air-mouse | turn-signal (any key in _data/series.yml)
  DATE    YYYY-MM-DD, the day the work happened (America/Regina). Refused if in the future.
  SLUG    short-slug (no part prefix); file becomes _posts/DATE-part-N-SLUG.md and the
          permalink /SERIES-url/part-N-SLUG/
  Title   text after "Part N: " (no colon allowed)

Part numbering: next number after the highest part in the series. If the series has a roadmap
post (front matter `roadmap: true`, or a title containing "Next Steps" / "What's Next"), the new
post takes the roadmap's number and the roadmap's `part:` and title number are bumped by one
(filename and permalink unchanged), as the update-blog skill requires.

Writes the continuity line linking the previous part, the contents box (3+ sections) and one
skeleton per section (heading, entry-date, Objective / Method / Result / Conclusion). Prints the
paths written so the deliver step's upload list is exact.
"""
import argparse, datetime, os, re, sys

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]


def front(path):
    txt = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", txt, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith(" "):
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"')
    return fm, txt


def series_url(site, key):
    txt = open(os.path.join(site, "_data", "series.yml"), encoding="utf-8").read()
    m = re.search(rf"^{re.escape(key)}:\n(?:  .*\n)*?  url:\s*(\S+)", txt, re.M)
    if not m:
        sys.exit(f"series {key!r} not in _data/series.yml")
    return m.group(1).rstrip("/")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("site"); ap.add_argument("series"); ap.add_argument("date")
    ap.add_argument("slug"); ap.add_argument("title")
    ap.add_argument("--time", default="12:00")
    ap.add_argument("--sections", nargs="*", default=["Section title"])
    a = ap.parse_args()

    if ":" in a.title:
        sys.exit("title must not contain a colon (the layout splits on the one after Part N)")
    d = datetime.date.fromisoformat(a.date)
    today = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=6)).date()  # America/Regina, no DST
    if d > today:
        sys.exit(f"{a.date} is in the future for America/Regina ({today}); GitHub Pages would skip it")

    posts = os.path.join(a.site, "_posts")
    parts, roadmap = [], None
    for n in sorted(os.listdir(posts)):
        if not n.endswith(".md"):
            continue
        fm, _ = front(os.path.join(posts, n))
        if fm.get("series") != a.series:
            continue
        p = int(fm.get("part", -1))
        is_road = fm.get("roadmap") == "true" or re.search(r"Next Steps|What's Next", fm.get("title", ""))
        if is_road:
            roadmap = (n, p)
        else:
            parts.append((p, n, fm))
    parts.sort()
    if roadmap:
        num = roadmap[1]
    else:
        num = parts[-1][0] + 1 if parts else 0
    prev = parts[-1] if parts else None

    base = series_url(a.site, a.series)
    fname = f"{a.date}-part-{num}-{a.slug}.md"
    dst = os.path.join(posts, fname)
    if os.path.exists(dst):
        sys.exit(f"{dst} exists")
    human = f"{d.day} {MONTHS[d.month - 1]} {d.year}"

    out = ["---", "layout: series-post", f'title: "Part {num}: {a.title}"',
           f"date: {a.date} {a.time}:00 -0600", f"series: {a.series}", f"part: {num}",
           f'covers: "{human}"', 'excerpt: "TODO one sentence, shown as the lede and in the build-log list."',
           f"permalink: {base}/part-{num}-{a.slug}/", "---", ""]
    if prev:
        out += [f"This entry continues from [Part {prev[0]}]({prev[2].get('permalink', '')}), TODO one line on where it left off.", ""]
    if len(a.sections) >= 3:
        out += ['<details class="toc" markdown="1">', "<summary>Contents</summary>", "",
                "* TOC", "{:toc}", "", "</details>", ""]
    for s in a.sections:
        out += [f"## {s}", "", f'<p class="entry-date">{human}</p>', "",
                "**Objective.** TODO", "", "**Method.** TODO", "", "**Result.** TODO", "",
                "**Conclusion.** TODO", ""]
    out += ["**Next:** TODO", ""]
    open(dst, "w", encoding="utf-8").write("\n".join(out))
    print("new:", dst)

    if roadmap:
        rp = os.path.join(posts, roadmap[0])
        _, txt = front(rp)
        txt = re.sub(r"^part:\s*\d+", f"part: {num + 1}", txt, count=1, flags=re.M)
        txt = re.sub(r'^title:\s*"Part \d+:', f'title: "Part {num + 1}:', txt, count=1, flags=re.M)
        open(rp, "w", encoding="utf-8").write(txt)
        print("bumped roadmap:", rp, f"-> Part {num + 1}")
    print("TODO left in the skeleton:", "grep -n TODO " + dst)


if __name__ == "__main__":
    main()
