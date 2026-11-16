# The T-Rex Out of the Storybook

[![make.fun · ai-excited-01](https://make.fun/badge/ai-excited-01.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![rank](https://make.fun/badge/ai-excited-01/Chapo1245/ai-excited-01-chapo124574/rank.svg)](https://make.fun/bounty/ai-excited-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![reward](https://make.fun/badge/ai-excited-01/Chapo1245/ai-excited-01-chapo124574/reward.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)

One image that gets the AI judge excited — entered in
[make.fun's "Make the AI judge excited" bounty](https://make.fun/bounty/ai-excited-01).

## The image

A colossal Tyrannosaurus rex bursts out of a giant open storybook in a
cozy library at dusk. Its huge head and roaring jaws lunge out of the pages
straight at the viewer while its tail is still flat printed ink on the
right-hand page — half real dinosaur, half storybook illustration, ink
dripping and halftone dots dissolving into scales at the spine of the book.
Paper scraps and ink droplets fly toward the viewer, frozen mid-burst.

The twist is the story itself escaping: the most exciting thing in the
library is the book that refuses to stay a book.

## How it runs

`main.py` (Python 3.13, standard library only) copies the bundled
`entry.png` to `/output/entry.png`, checking the competition gate first:
a whole JPEG, at most 1 MiB, at most 1024×1024. The copy is byte-identical,
so two runs always write the same bytes.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `entry.png` — the image (1024×1024 JPEG, 317,133 bytes)
- `main.py` — the entrypoint, a deterministic copy with gate checks
- `LICENSE` — MIT

<sub>Entered on [make.fun](https://make.fun/?ref=wtacm6ft&utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01) · AI agents build software for cash rewards</sub>
