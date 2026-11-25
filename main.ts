// World news image entry for make.fun's "Sum up 25 November's world news" bounty.
// Node 22, standard library only. The judge sees exactly the bytes copied here.
// Outside the grader: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = fileURLToPath(new URL('.', import.meta.url));
const output = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(output, { recursive: true });

const source = join(here, 'entry.png');
const target = join(output, 'entry.png');
copyFileSync(source, target);
// The gate refuses anything other than one whole image under 1 MiB.
const bytes = statSync(target).size;
if (bytes > 1048576) {
  throw new Error(`entry.png is ${bytes} bytes, above the 1 MiB limit`);
}
if (bytes < 4096) {
  throw new Error(`entry.png is only ${bytes} bytes, too small to be a real image`);
}
