"""Command-line interface for fakescan."""

import sys
from pathlib import Path

from .core import make_printed_pdf


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: fakescan <input.pdf> [output.pdf] [--dpi N]")
        print("       python -m fakescan <input.pdf> [output.pdf] [--dpi N]")
        sys.exit(1)

    input_pdf = sys.argv[1]
    dpi = 200
    output_pdf = None

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--dpi" and i + 1 < len(args):
            dpi = int(args[i + 1])
            i += 2
        elif not args[i].startswith("--"):
            output_pdf = args[i]
            i += 1
        else:
            i += 1

    if output_pdf is None:
        p = Path(input_pdf)
        output_pdf = str(p.parent / (p.stem + "_scanned" + p.suffix))

    make_printed_pdf(input_pdf, output_pdf, dpi=dpi)


if __name__ == "__main__":
    main()
