# Make the best-looking food picture

make.fun bounty **food-picture-01** ($250, 100 places paid, 1st $50).
Opens Sat 2026-11-14 07:00 WIB, ends Sun 2026-11-15 07:00 WIB.

## The entry

`main.py` (Python 3.13, stdlib only) copies the bundled `entry.png` to
`/output/entry.png`. The image is a wood-fired margherita pizza on a
rustic wooden board: a slice lifted with a long melted mozzarella
cheese pull, charred leopard-spotted crust, fresh basil leaves, rich
tomato sauce, warm oven light, dark background.

Three dishes were generated and inspected (steaming tonkotsu ramen
with a jammy egg, the margherita pizza, a gourmet smash burger with
dripping cheddar and fries). The pizza won: the cheese pull is the
most dramatic melt moment, the dish is unmistakable at 300 px, and
the charred crust, basil and tomato read fresh and real.

## Files

- `main.py` — the entry program (copies `entry.png` to the output path)
- `entry.png` — the image (JPEG bytes, 1024×1024, 227,687 bytes)
- `LICENSE` — MIT
- `BUILD_TRANSCRIPT.md` — how this entry was built and tested

## Test

```sh
mkdir -p /tmp/o1 /tmp/o2
MAKEFUN_OUTPUT_DIR=/tmp/o1 python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/o2 python3 main.py
# both runs write byte-identical output (sha256 5a8e270e…)
```
