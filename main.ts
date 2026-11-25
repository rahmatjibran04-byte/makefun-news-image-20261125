// news-image-20261125 — entry program.
//
// What it does: copy the pre-rendered front page (entry.png, sitting
// next to this file) into the bounty output directory as entry.png,
// then validate the output before exiting.
//
// Runtime: Node 22, standard library only, no network access.
// Deterministic by construction: the output is a byte-for-byte copy of
// entry.png, so two runs always produce identical bytes.
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
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

const dest = join(outDir, "entry.png");
copyFileSync(src, dest);

// Validate the output before reporting success: it must exist, be a
// structurally valid PNG (signature + IHDR chunk), and fit the 1 MiB
// bounty size limit. Any failure exits non-zero with a clear message
// instead of silently leaving a broken output behind.
const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const MAX_BYTES = 1024 * 1024; // 1 MiB

if (!existsSync(dest)) {
  console.error(`error: output missing after copy: ${dest}`);
  process.exit(1);
}

const out = readFileSync(dest);
if (
  out.length < PNG_SIGNATURE.length + 8 ||
  !out.subarray(0, 8).equals(PNG_SIGNATURE) ||
  out.subarray(12, 16).toString("ascii") !== "IHDR"
) {
  console.error(`error: output is not a valid PNG: ${dest}`);
  process.exit(1);
}

if (out.length > MAX_BYTES) {
  console.error(
    `error: output exceeds 1 MiB (${out.length} bytes): ${dest}`,
  );
  process.exit(1);
}

console.log(`wrote ${dest} (${out.length} bytes, valid PNG)`);
