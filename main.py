#!/usr/bin/env python3
"""ai-excited-01 entry: copy the bundled image to the output path.

The artwork (a T-Rex bursting out of a storybook) lives in the repository
as entry.png next to this program. This program does nothing clever: it
reads those exact bytes, checks them against the competition gate
(JPEG, at most 1 MiB, at most 1024x1024), and writes the identical bytes
to the output file. Two runs therefore always produce the same bytes.

Standard library only. No network, no randomness, no timestamps in the
output.
"""

import hashlib
import os
import struct
import sys

MAX_BYTES = 1_048_576
MAX_SIDE = 1024


def jpeg_dimensions(data: bytes) -> tuple[int, int]:
    """Return (width, height) of a baseline/extended JPEG, stdlib only."""
    if len(data) < 4 or data[0:2] != b"\xff\xd8":
        raise ValueError("not a JPEG: missing SOI marker")
    pos = 2
    while pos + 9 <= len(data):
        if data[pos] != 0xFF:
            raise ValueError("not a JPEG: bad marker at offset %d" % pos)
        marker = data[pos + 1]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            pos += 2
            continue
        size = struct.unpack(">H", data[pos + 2:pos + 4])[0]
        if size < 2 or pos + 2 + size > len(data):
            raise ValueError("not a JPEG: truncated segment")
        if marker in (0xC0, 0xC1, 0xC2):
            height, width = struct.unpack(">HH", data[pos + 5:pos + 9])
            return width, height
        pos += 2 + size
    raise ValueError("not a JPEG: no SOF frame found")


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, "entry.png")

    with open(source, "rb") as handle:
        data = handle.read()

    if len(data) > MAX_BYTES:
        print("entry.png is %d bytes, over the 1 MiB gate" % len(data),
              file=sys.stderr)
        return 1
    if data[0:2] != b"\xff\xd8" or data[-2:] != b"\xff\xd9":
        print("entry.png is not a whole JPEG (SOI/EOI markers)",
              file=sys.stderr)
        return 1

    width, height = jpeg_dimensions(data)
    if width > MAX_SIDE or height > MAX_SIDE:
        print("entry.png is %dx%d, over the 1024x1024 gate" % (width, height),
              file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(data)

    with open(target, "rb") as handle:
        written = handle.read()
    if written != data:
        print("output differs from source after write", file=sys.stderr)
        return 1

    digest = hashlib.sha256(data).hexdigest()
    print("wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (target, width, height, len(data), digest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
