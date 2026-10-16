#!/usr/bin/env python3
"""Zip the github-site folder into the deliverable sarojratul-github-site.zip.

usage: make_zip.py GITHUB_SITE OUT.zip

The folder itself is the zip's top level (github-site/...), as when it is compressed from
Explorer. Skips editor and OS clutter (.DS_Store, Thumbs.db, desktop.ini, ~$ lock files).
Prints the file count and size so it can be compared with the copy on the device.
"""
import os, sys, zipfile

SKIP = {".DS_Store", "Thumbs.db", "desktop.ini"}


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    site, out = os.path.abspath(sys.argv[1]), sys.argv[2]
    top = os.path.basename(site.rstrip("/"))
    n = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for d, dirs, names in os.walk(site):
            dirs.sort()
            for name in sorted(names):
                if name in SKIP or name.startswith("~$"):
                    continue
                p = os.path.join(d, name)
                z.write(p, os.path.join(top, os.path.relpath(p, site)))
                n += 1
    print(f"{out}: {n} files, {os.path.getsize(out):,} bytes")


if __name__ == "__main__":
    main()
