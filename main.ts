// news-image-20261125 — entry program.
//
// What it does: copy the pre-rendered front page (entry.png, sitting
// next to this file) into the bounty output directory as entry.png.
//
// Runtime: Node 22, standard library only, no network access.
// Deterministic by construction: the output is a byte-for-byte copy of
// entry.png, so two runs always produce identical bytes.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Directory of this file — entry.png lives right beside it.
const here = dirname(fileURLToPath(import.meta.url));

// Bounty harness override, otherwise the standard /output location.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });

const src = join(here, "entry.png");
if (!existsSync(src)) {
  throw new Error(`entry.png not found next to main.ts (${here})`);
}

copyFileSync(src, join(outDir, "entry.png"));
