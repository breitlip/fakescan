"""Command-line interface for fakescan."""

import sys
from importlib.metadata import version
from pathlib import Path

from .core import make_printed_pdf


_HELP = """\
Usage: fakescan [options] <input.pdf> [output.pdf]

Make a PDF look like it was printed on paper and scanned back.

Arguments:
  input.pdf             Path to the source PDF.
  output.pdf            Output path (default: <input>_scanned.pdf).

Options:
  --dpi N               Render resolution (default: 200).
  -h, --help            Show this help message and exit.
  --version             Show version and exit.

Examples:
  fakescan input.pdf
  fakescan input.pdf output.pdf
  fakescan input.pdf output.pdf --dpi 300
"""


def main() -> None:
    if "--version" in sys.argv:
        print(f"fakescan {version('fakescan')}")
        sys.exit(0)

    if len(sys.argv) < 2 or "-h" in sys.argv or "--help" in sys.argv:
        print(_HELP, end="")
        sys.exit(0 if "-h" in sys.argv or "--help" in sys.argv else 1)

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
