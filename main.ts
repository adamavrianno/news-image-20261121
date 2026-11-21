import { chmodSync, copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry for "Sum up 21 November's world news in one image".
// Copies the poster image sitting beside this program into the output
// directory as entry.png. No network calls, no randomness, no
// timestamps: the output is byte-identical on every run.

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dest = join(outDir, "entry.png");

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "poster.png"), dest);
chmodSync(dest, 0o644);
