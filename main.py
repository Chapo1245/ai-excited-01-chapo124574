"""ai-excited-01 entry: "The T-Rex Out of the Storybook".

Copies the bundled image (entry.png, a JPEG by magic bytes) to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output). Deterministic: the same
input bytes are written on every run. Standard library only, no network.

The image: a T-Rex bursts out of an open storybook on a desk — its roaring
head, claws and shoulders are fully real, while its tail is still flat
printed ink on the page. One giant focal point, readable at 300 px.
"""

import os
import shutil
import sys

MAX_BYTES = 1_048_576  # gate: at most 1 MiB
SOURCE_NAME = "entry.png"
DEST_NAME = "entry.png"


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest = os.path.join(out_dir, DEST_NAME)

    size = os.path.getsize(source)
    if size > MAX_BYTES:
        print(f"error: {SOURCE_NAME} is {size} bytes, over the 1 MiB gate",
              file=sys.stderr)
        return 1

    with open(source, "rb") as fh:
        magic = fh.read(8)
    if magic[:2] != b"\xff\xd8" and magic[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: entry.png is neither JPEG nor PNG by magic bytes",
              file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(source, dest)

    written = os.path.getsize(dest)
    if written != size:
        print(f"error: wrote {written} bytes, expected {size}",
              file=sys.stderr)
        return 1

    print(f"wrote {dest} ({written} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
