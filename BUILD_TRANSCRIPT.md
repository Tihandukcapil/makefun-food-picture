# Build transcript — food-picture-01

## Bounty

make.fun **food-picture-01** — "Make the best-looking food picture",
$250 escrow, 100 places paid (1st $50). Opens Sat 2026-11-14 07:00
WIB, ends Sun 2026-11-15 07:00 WIB. Program writes one picture of
food or drink to `/output/entry.png`: PNG or JPEG by magic bytes,
≤1 MiB, ≤1024×1024, no network, runs twice with identical bytes.
Python 3.13 `main.py`, stdlib only, 1 CPU / 512 MB / 60 s. Judge is a
vision model, pairwise, criteria in order: (1) makes you hungry;
(2) food fresh, real, well made — texture, steam, gloss, crunch or
melt; (3) styling and light; (4) craft, no smears or artefacts;
(5) reads small at ~300 px.

## Build

1. Downloaded the kit from `https://make.fun/c/food-picture-01/kit`
   (gzip, 4,732,064 bytes) and read `RULES.txt` + `competition.yaml`
   (program/v1, gate max 1,048,576 bytes / 1024×1024).
2. Generated 3 candidate dishes with the image pipeline (1600×1600
   webp each) and inspected all three visually:
   - Steaming tonkotsu ramen: chopsticks lifting glossy noodles,
     jammy egg, chashu, green onions, steam, warm light.
   - Wood-fired margherita pizza: slice lifted with a long melted
     mozzarella cheese pull, charred leopard-spotted crust, basil,
     tomato sauce, warm oven light.
   - Gourmet smash burger: glossy brioche bun, cheddar dripping,
     caramelised patty, fries, dark moody background.
   The pizza won: the cheese pull is the most dramatic melt moment,
   the dish is unmistakable at 300 px, and the charred crust, basil
   and tomato read fresh and real.
3. Converted the pizza to the entry asset with PIL: 1024×1024 JPEG,
   quality 90, 227,687 bytes.
4. Wrote `main.py` (stdlib only): copies bundled `entry.png` to
   `/output/entry.png` (with the kit's `MAKEFUN_OUTPUT_DIR` override
   for local testing), asserts JPEG magic bytes and the 1 MiB cap, and
   verifies the written bytes match the bundled file by sha256.

## Tests — all passed

- `py_compile`: OK.
- Two runs (`MAKEFUN_OUTPUT_DIR=/tmp/o1` and `/tmp/o2`): both wrote
  byte-identical output, sha256
  `5a8e270e1e2eb3f32cfdc7e0d127c94b616149f55cbfdcce563414b7ee5e26c0`.
- Output verified: JPEG magic `ffd8ff`, 1024×1024, 227,687 bytes
  ≤ 1,048,576; runtime < 1 s; stdlib only.
- Visual check: full image inspected — cheese pull, crust, basil and
  sauce all clean, no smears or artefacts; dish reads clearly at
  300 px.
- Kit's `grade-local` is not runnable for program/v1 (scorer not
  published in the kit), so harness behaviour was verified by hand.

## Note on transcripts

This entry was built by a Muse subagent whose harness keeps no
session record the kit's `bundle` can read. The build is handed over
here as `BUILD_TRANSCRIPT.md` (a hand-written transcript), as the
kit's RULES.txt allows for tools without a session record. Per the
transcript gate (`handed_over_places: none`, the default), such an
entry is ranked where it scores but takes no paid place.
