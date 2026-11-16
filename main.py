#!/usr/bin/env python3
"""ai-excited-01 entry: "The T-Rex Out of the Storybook".

The entry image (entry.png, JPEG bytes, 1024x1024) is a T-Rex bursting out
of an open storybook: its head and forelegs are a real roaring dinosaur
lunging at the viewer while its tail is still a flat printed-ink drawing
on the page below. This program only copies that image to the output
directory, deterministically, so both runs write identical bytes.

Standard library only. No network.
"""

import os
import shutil
import sys

MAX_BYTES = 1_048_576
SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    size = os.path.getsize(SOURCE)
    if size > MAX_BYTES:
        print(f"entry.png is {size} bytes, over the 1 MiB limit", file=sys.stderr)
        return 1
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    copied = os.path.getsize(dest)
    if copied != size:
        print(f"copy mismatch: wrote {copied} bytes, expected {size}",
              file=sys.stderr)
        return 1
    print(f"wrote {dest} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
