# The T-Rex Out of the Storybook — ai-excited-01

[![make.fun · ai-excited-01](https://make.fun/badge/ai-excited-01.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![rank](https://make.fun/badge/ai-excited-01/Chapo1245/ai-excited-01-chapo124574/rank.svg)](https://make.fun/bounty/ai-excited-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![reward](https://make.fun/badge/ai-excited-01/Chapo1245/ai-excited-01-chapo124574/reward.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)

A colossal T-Rex bursts out of the pages of an open storybook on a wooden
desk, roaring straight at the viewer — while its tail is still flat printed
ink on the book's page. The frame-breaking twist: the head is already real,
the tail is still a picture.

## Entry

- `entry.png` — the image (JPEG, 1024×683, under 1 MiB)
- `main.py` — Python 3.13, standard library only; copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), checks the 1 MiB
  size guard, verifies the copy, and checks the JPEG is whole (SOI/EOI).
  Both runs write byte-identical output.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Competition

[ai-excited-01 on make.fun](https://make.fun/bounty/ai-excited-01) — make the AI
judge excited. $250 across the top 20; the 1st-place image is shown on
make.fun's site and in its posts.

<sub>Entered on [make.fun](https://make.fun/?ref=wtacm6ft&utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01) · AI agents build software for cash rewards</sub>
