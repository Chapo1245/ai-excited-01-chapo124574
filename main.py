#!/usr/bin/env python3
"""ai-excited-01 entry: copy the entry image to the output directory.

The image (entry.png, JPEG bytes) is shipped in this repository. The
program copies it to $MAKEFUN_OUTPUT_DIR/entry.png (default /output),
checking the 1 MiB size guard before the copy and verifying the copy
afterwards, so both runs write byte-identical output.
"""

import hashlib
import os
import shutil
import sys

MAX_BYTES = 1_048_576
IMAGE_NAME = "entry.png"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, IMAGE_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, IMAGE_NAME)

    size = os.path.getsize(source)
    if size > MAX_BYTES:
        print(f"entry image too large: {size} bytes", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, target)

    written = os.path.getsize(target)
    if written != size:
        print("copy size mismatch", file=sys.stderr)
        return 1

    # Whole-file check: a JPEG must start with SOI and end with EOI.
    with open(target, "rb") as fh:
        head = fh.read(2)
        fh.seek(-2, os.SEEK_END)
        tail = fh.read(2)
    if head != b"\xff\xd8" or tail != b"\xff\xd9":
        print("entry image is not a whole JPEG", file=sys.stderr)
        return 1

    digest = hashlib.sha256(open(target, "rb").read()).hexdigest()
    print(f"wrote {target} ({written} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
