#!/usr/bin/env python3
"""Copy this repo's entry.png to the make.fun output directory.

Reads MAKEFUN_OUTPUT_DIR (default /output), creates it if missing, and
copies entry.png there as entry.png. Standard library only, no network.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print(f"error: {src} not found", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"Copied entry.png to {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
