// SPDX-License-Identifier: MIT
// ai-excited-01 — "Make the AI judge excited".
//
// A colossal blue whale bursts through the ceiling of a tiny, cozy living
// room while a man on the sofa looks up in awe. Scale twist, frozen
// mid-breach momentum, one huge shape that still hits at 300 px.
//
// The program is deliberately deterministic: it copies the bundled
// entry.png byte-for-byte to the output directory. No network, no clock,
// no randomness — two runs produce identical bytes.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = join(here, "entry.png");
const dst = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
console.log(`wrote ${dst}`);
