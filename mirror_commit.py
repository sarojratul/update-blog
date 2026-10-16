#!/usr/bin/env python3
"""Mirror the files changed by site-repo commits back to Saroj's local github-site folder.

usage: mirror_commit.py REPO BASE_REV OUTDIR WINROOT

  REPO      clone of sarojratul.github.io
  BASE_REV  commit the push started from (e.g. the HEAD before editing, or HEAD~1)
  OUTDIR    container folder to copy the files into (e.g. /mnt/user-data/outputs/github-site)
  WINROOT   the device folder, e.g. 'C:\\Users\\saroj\\OneDrive\\Documents\\Claude Projects\\AIR-MOUSE\\github-site'

Copies every file added or modified between BASE_REV and HEAD into OUTDIR (keeping paths) and
prints the device_commit_files JSON on stdout. Files deleted or renamed away in the repo are
listed on stderr: device tools cannot delete, so move them to AIR-MOUSE\\_to_delete\\ or tell
Saroj to remove them.
"""
import json, os, shutil, subprocess, sys


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    repo, base, outdir, winroot = sys.argv[1:]
    names = subprocess.run(["git", "-C", repo, "diff", "--name-status", "-M", base, "HEAD"],
                           check=True, capture_output=True, text=True).stdout.splitlines()
    copy, gone = [], []
    for line in names:
        parts = line.split("\t")
        st = parts[0][0]
        if st in "AM":
            copy.append(parts[1])
        elif st == "D":
            gone.append(parts[1])
        elif st == "R":
            gone.append(parts[1]); copy.append(parts[2])
    for rel in copy:
        dst = os.path.join(outdir, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(os.path.join(repo, rel), dst)
    root = winroot.rstrip("\\")
    print(json.dumps([{"stagedPath": os.path.abspath(os.path.join(outdir, r)),
                       "devicePath": root + "\\" + r.replace("/", "\\")} for r in copy], indent=1))
    for r in gone:
        print("removed in repo, still on device:", r, file=sys.stderr)
    print(f"{len(copy)} file(s) to commit", file=sys.stderr)


if __name__ == "__main__":
    main()
