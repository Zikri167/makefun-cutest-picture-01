# A Little Snowy Penguin

This entry features a fluffy baby penguin with bright, glossy eyes and a
red knitted scarf, sitting in the snow. The image is already included as
`entry.png`.

The program beside the image reads that JPEG and checks its signature,
file size, frame type, dimensions, and ending marker. If it passes, the
program copies the original bytes to `entry.png` in
`MAKEFUN_OUTPUT_DIR` (which defaults to `/output`) and reports the saved
path, dimensions, byte count, and SHA-256 digest.

Run it with Node:

```sh
node main.ts
```
