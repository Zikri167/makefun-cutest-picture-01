import { copyFileSync } from 'node:fs';
import { resolve } from 'node:path';

// The illustration is generated ahead of time; this program draws nothing at run time.
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
// The target directory is supplied by the runner or falls back to /output.
copyFileSync(new URL('./entry.png', import.meta.url), resolve(outputDir, 'entry.png'));
