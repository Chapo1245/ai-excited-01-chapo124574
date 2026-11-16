#!/usr/bin/env python3
"""ai-excited-01 entry: copy the bundled image to the output path.

The image (entry.png, a T-Rex bursting out of a storybook) lives in this
repository; this program only copies its exact bytes to /output/entry.png,
so both graded runs write identical bytes. Standard library only.
"""

import os
import shutil
import sys


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    # Determinism guard: the copy must be byte-identical to the source.
    if os.path.getsize(source) != os.path.getsize(target):
        raise SystemExit("entry.png copy size mismatch")
    return 0


if __name__ == "__main__":
    sys.exit(main())
