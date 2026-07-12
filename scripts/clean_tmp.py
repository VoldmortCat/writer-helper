#!/usr/bin/env python3
# Clean up AI writing companion temp files
# Usage:
#   python scripts/clean_tmp.py            # delete all
#   python scripts/clean_tmp.py --dry-run  # list only
#   python scripts/clean_tmp.py --days 7   # older than 7 days

import os, sys, time

BASE = os.path.dirname(__file__)
TMP_DIR = os.path.abspath(os.path.join(BASE, "..", "output", "tmp"))


def main():
    dry_run = "--dry-run" in sys.argv
    max_days = None
    for i, arg in enumerate(sys.argv):
        if arg == "--days" and i + 1 < len(sys.argv):
            try:
                max_days = int(sys.argv[i + 1])
            except ValueError:
                pass

    if not os.path.isdir(TMP_DIR):
        print("Temp directory does not exist:", TMP_DIR)
        return

    now = time.time()
    deleted = 0
    kept = 0

    for f in sorted(os.listdir(TMP_DIR)):
        fpath = os.path.join(TMP_DIR, f)
        if not os.path.isfile(fpath) or f.startswith("."):
            continue

        if max_days is not None:
            age_days = (now - os.path.getmtime(fpath)) / 86400
            if age_days < max_days:
                kept += 1
                continue

        if dry_run:
            print("  [dry-run] would delete:", f)
        else:
            os.remove(fpath)
            print("  deleted:", f)
        deleted += 1

    total = deleted + kept
    s = "%d files total, %d deleted, %d kept" % (total, deleted, kept)
    print(s)


if __name__ == "__main__":
    main()
