import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const source = join(dirname(fileURLToPath(import.meta.url)), "entry.png");
const destinationFolder = resolve(process.env.MAKEFUN_OUTPUT_DIR || "/output");
const destination = join(destinationFolder, "entry.png");

function fail(message: string): never {
  throw new Error(message);
}

function dimensionsOfJpeg(bytes: Buffer): { width: number; height: number } {
  let cursor = 2;

  while (cursor < bytes.length) {
    if (bytes[cursor] !== 0xff) fail("JPEG marker stream is malformed");
    while (cursor < bytes.length && bytes[cursor] === 0xff) cursor++;
    if (cursor >= bytes.length) break;

    const marker = bytes[cursor++];
    if (marker === 0xd9 || marker === 0xda) break;
    if (marker === 0x01 || (marker >= 0xd0 && marker <= 0xd7)) continue;
    if (cursor + 2 > bytes.length) fail("JPEG segment header is incomplete");

    const segmentSize = bytes.readUInt16BE(cursor);
    if (segmentSize < 2 || cursor + segmentSize > bytes.length) {
      fail("JPEG segment length is invalid");
    }

    if (marker === 0xc0 || marker === 0xc1 || marker === 0xc2) {
      if (segmentSize < 7) fail("JPEG frame header is incomplete");
      return {
        height: bytes.readUInt16BE(cursor + 3),
        width: bytes.readUInt16BE(cursor + 5),
      };
    }
    cursor += segmentSize;
  }

  fail("JPEG has no supported baseline or progressive frame");
}

async function run(): Promise<void> {
  const picture = await readFile(source);
  if (picture.length === 0) fail("The picture file is empty");
  if (picture.length > 1_048_576) fail("The picture exceeds the 1 MiB limit");
  if (picture[0] !== 0xff || picture[1] !== 0xd8 || picture[2] !== 0xff) {
    fail("The picture does not begin with a JPEG signature");
  }
  if (picture[picture.length - 2] !== 0xff || picture[picture.length - 1] !== 0xd9) {
    fail("The JPEG is missing its FF D9 end marker");
  }

  const { width, height } = dimensionsOfJpeg(picture);
  if (width === 0 || height === 0) fail("JPEG dimensions must be positive");
  if (width > 1024 || height > 1024) fail("The picture exceeds 1024 pixels per side");

  await mkdir(destinationFolder, { recursive: true });
  await writeFile(destination, picture);
  const digest = createHash("sha256").update(picture).digest("hex");
  process.stdout.write(
    `Wrote ${destination} | ${picture.length} bytes | ${width}x${height} | sha256 ${digest}\n`,
  );
}

run().catch((error: unknown) => {
  const detail = error instanceof Error ? error.message : String(error);
  process.stderr.write(`Picture copy failed: ${detail}\n`);
  process.exitCode = 1;
});
