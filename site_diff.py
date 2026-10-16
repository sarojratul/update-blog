#!/usr/bin/env python3
"""Compare two copies of a folder and report what changed.

usage:
  site_diff.py ORIG EDITED                       # upload list (Replace / New / Delete by hand)
  site_diff.py ORIG EDITED --outputs DIR         # also copy changed + new files into DIR/<rel path>
  site_diff.py ORIG EDITED --commit-json WINROOT # print device_commit_files JSON (stagedPath under
                                                 #   --outputs DIR, devicePath under WINROOT)
  site_diff.py ORIG EDITED --map --ignore 'class="preview-bar"'
                                                 # print {rel: abs EDITED path} JSON of changed + new
                                                 #   files; use on two preview builds for the
                                                 #   Artifact `files` map (--ignore drops lines
                                                 #   matching a regex, here the build timestamp)

ORIG is the untouched staged copy (e.g. /mnt/user-data/uploads/AIR-MOUSE/github-site),
EDITED the working copy. Files are compared by SHA-256, so touched-but-identical files are
not reported. Removed files are listed under "Delete by hand".

Example (deliver step of the update-blog skill):
  python3 site_diff.py /mnt/user-data/uploads/AIR-MOUSE/github-site $W/github-site \
      --outputs /mnt/user-data/outputs/github-site \
      --commit-json 'C:\\Users\\saroj\\OneDrive\\Documents\\Claude Projects\\AIR-MOUSE\\github-site'
"""
import argparse, hashlib, json, os, re, shutil, sys

TEXT = (".html", ".md", ".css", ".scss", ".yml", ".json", ".svg", ".xml", ".txt")


def files(root, ignore=None):
    out = {}
    for d, _, names in os.walk(root):
        for n in names:
            p = os.path.join(d, n)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            with open(p, "rb") as f:
                data = f.read()
            if ignore and n.endswith(TEXT):
                data = b"\n".join(l for l in data.split(b"\n") if not ignore.search(l))
            out[rel] = hashlib.sha256(data).hexdigest()
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("orig"); ap.add_argument("edited")
    ap.add_argument("--outputs", help="copy changed and new files here, keeping relative paths")
    ap.add_argument("--commit-json", metavar="WINROOT", help="print device_commit_files JSON for WINROOT")
    ap.add_argument("--map", action="store_true", help="print JSON map of changed + new files")
    ap.add_argument("--ignore", help="regex; lines matching it in text files are ignored when comparing")
    a = ap.parse_args()

    ig = re.compile(a.ignore.encode()) if a.ignore else None
    o, e = files(a.orig, ig), files(a.edited, ig)
    changed = sorted(k for k in e if k in o and e[k] != o[k])
    new = sorted(k for k in e if k not in o)
    removed = sorted(k for k in o if k not in e)

    if a.map:
        print(json.dumps({k: os.path.abspath(os.path.join(a.edited, k)) for k in changed + new}, indent=1))
        return

    print("1. Replace:" + ("" if changed else " none"))
    for k in changed: print("   - " + k)
    print("2. New:" + ("" if new else " none"))
    for k in new: print("   - " + k)
    print("3. Delete by hand:" + ("" if removed else " none (no file was renamed or removed)"))
    for k in removed: print("   - " + k)

    if a.outputs:
        for k in changed + new:
            dst = os.path.join(a.outputs, k)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(os.path.join(a.edited, k), dst)
        print(f"copied {len(changed) + len(new)} file(s) to {a.outputs}", file=sys.stderr)

    if a.commit_json:
        if not a.outputs:
            sys.exit("--commit-json needs --outputs")
        root = a.commit_json.rstrip("\\")
        print(json.dumps([{"stagedPath": os.path.abspath(os.path.join(a.outputs, k)),
                           "devicePath": root + "\\" + k.replace("/", "\\")}
                          for k in changed + new], indent=1))


if __name__ == "__main__":
    main()
