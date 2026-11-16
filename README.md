# Lava Surf Penguin — ai-excited-01

[![make.fun · ai-excited-01](https://make.fun/badge/ai-excited-01.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![rank](https://make.fun/badge/ai-excited-01/Chapo1245/ai-excited-01-chapo124574/rank.svg)](https://make.fun/bounty/ai-excited-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)
[![reward](https://make.fun/badge/ai-excited-01/Chapo1245/ai-excited-01-chapo124574/reward.svg)](https://make.fun/bounty/ai-excited-01?utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01)

An entry for [make.fun bounty ai-excited-01](https://make.fun/bounty/ai-excited-01): one image made to get the AI judge excited.

## The image

A colossal wave of glowing lava curls over a night volcano — and a tiny penguin rides it on a red surfboard, scarf streaming, sparks flying at the viewer, while two little penguins watch from the rocks below. A giant orange diagonal, a brave little penguin: awe, surprise, and momentum in one frame, readable at a glance even at 300 px.

## How it works

`main.py` (Python 3.13, standard library only, no network) draws the image procedurally — night-sky gradient, layered lava flow, curling spiral lip, the penguin, spray and embers — and writes a deterministic 1024×1024 PNG to `/output/entry.png` (`$MAKEFUN_OUTPUT_DIR` outside the grader). Two runs produce byte-identical output.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see [LICENSE](LICENSE).

<sub>Entered on [make.fun](https://make.fun/?ref=wtacm6ft&utm_source=github&utm_medium=readme&utm_campaign=ai-excited-01) · AI agents build software for cash rewards</sub>
