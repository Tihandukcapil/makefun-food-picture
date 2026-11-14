#!/usr/bin/env python3
"""Make the best-looking food picture - make.fun bounty food-picture-01.

Writes one image to /output/entry.png: a wood-fired margherita
pizza on a rustic wooden board, a slice lifted with a long melted
mozzarella cheese pull, charred leopard-spotted crust, fresh basil,
rich tomato sauce, warm oven light. The image is the entry; the
program simply copies the bundled file to the output path, exactly
as the bounty brief suggests ("the simplest program copies an image
the repository holds").

Deterministic by design: the copied file is a fixed asset, there is
no randomness, no network access and no time dependence, so two runs
write identical bytes - as the bounty requires ("the program runs
twice and both runs must write the same bytes").

The bundled image is fully validated before it is copied (JPEG
structure, end marker, exact 1024x1024 dimensions) and re-validated
after the write, so a truncated or wrong-size asset fails loudly
instead of silently producing a bad entry.

Python 3.13, standard library only.
"""

import hashlib
import os
import shutil
import sys

DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_NAME = "entry.png"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024

# All valid Start-Of-Frame markers (baseline, extended, progressive,
# lossless and differential variants). Excluded on purpose: 0xC4
# (DHT), 0xC8 (JPG) and 0xCC (DAC) are not frame markers.
SOF_MARKERS = frozenset(
    (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
     0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF)
)


def jpeg_dimensions(data: bytes) -> tuple[int, int]:
    """Walk the JPEG marker segments to the SOF segment and return
    (width, height). Raises AssertionError on any structural problem.

    Accepts every valid SOF variant (not just SOF0/1/2) and tolerates
    the 0xFF fill bytes the JPEG spec allows before a marker.
    """
    if data[:2] != b"\xff\xd8":
        raise AssertionError("not a JPEG (missing SOI marker)")
    pos = 2
    while pos + 4 <= len(data):
        if data[pos] != 0xFF:
            raise AssertionError("corrupt JPEG marker at offset %d" % pos)
        # Skip 0xFF fill bytes; the next non-0xFF byte is the marker.
        while pos < len(data) and data[pos] == 0xFF:
            pos += 1
        if pos >= len(data):
            break
        marker = data[pos]
        pos += 1
        if marker == 0xD9:  # EOI reached without seeing SOF
            break
        if marker == 0xDA:  # SOS: scan data follows, SOF must precede it
            break
        if marker == 0x01 or 0xD0 <= marker <= 0xD7:  # standalone markers
            continue
        if pos + 2 > len(data):
            raise AssertionError("truncated JPEG segment at offset %d" % pos)
        seg_len = int.from_bytes(data[pos : pos + 2], "big")
        if seg_len < 2 or pos + seg_len > len(data):
            raise AssertionError("truncated JPEG segment at offset %d" % pos)
        if marker in SOF_MARKERS:
            precision = data[pos + 2]
            assert precision == 8, (
                "bundled entry must be 8-bit JPEG, got %d-bit" % precision
            )
            height = int.from_bytes(data[pos + 3 : pos + 5], "big")
            width = int.from_bytes(data[pos + 5 : pos + 7], "big")
            return width, height
        pos += seg_len
    raise AssertionError("JPEG SOF segment not found")


def validate_jpeg(data: bytes) -> tuple[int, int]:
    """Full structural check of the bundled entry image: SOI, EOI
    (not truncated), size cap, and exact 1024x1024 dimensions.
    Returns (width, height)."""
    assert data[:2] == b"\xff\xd8", "bundled entry must start with JPEG SOI"
    assert data[-2:] == b"\xff\xd9", (
        "bundled entry is truncated (missing JPEG EOI)"
    )
    assert len(data) <= 1048576, "entry must be at most 1 MiB"
    width, height = jpeg_dimensions(data)
    assert (width, height) == (EXPECTED_WIDTH, EXPECTED_HEIGHT), (
        "bundled entry must be %dx%d, got %dx%d"
        % (EXPECTED_WIDTH, EXPECTED_HEIGHT, width, height)
    )
    return width, height


def source_path() -> str:
    """The bundled image, next to this file (the repo is read-only
    in the grader's container, so resolve from __file__, not cwd)."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, OUTPUT_NAME)


def output_path() -> str:
    """Where to write the image.

    MAKEFUN_OUTPUT_DIR is the kit's local-test override (the grader
    provides /output); the judge runs without it set, so the real
    output path is /output/entry.png.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR)
    return os.path.join(out_dir, OUTPUT_NAME)


def main() -> int:
    src = source_path()
    with open(src, "rb") as f:
        expected = f.read()
    width, height = validate_jpeg(expected)
    expected_sha = hashlib.sha256(expected).hexdigest()

    path = output_path()
    try:
        parent = os.path.dirname(path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        shutil.copyfile(src, path)
    except OSError:
        # Local fallback: /output is not writable on a dev machine.
        # The judge sandbox provides /output, so this never triggers
        # there. Writing the fallback keeps the program from crashing
        # while developing; the bytes written are identical.
        alt = os.path.join(os.getcwd(), "output", OUTPUT_NAME)
        os.makedirs(os.path.dirname(alt), exist_ok=True)
        shutil.copyfile(src, alt)
        path = alt
        print(
            "warning: could not write %s; wrote %s instead"
            % (output_path(), alt),
            file=sys.stderr,
        )

    with open(path, "rb") as f:
        written = f.read()
    assert hashlib.sha256(written).hexdigest() == expected_sha, (
        "written bytes differ from bundled entry"
    )
    validate_jpeg(written)

    sys.stdout.write(
        "wrote %s (%d bytes, %dx%d, sha256 %s)\n"
        % (path, len(written), width, height, expected_sha)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
