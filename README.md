# fakescan

Make a PDF look like it was printed on paper and scanned back.

## Effects

- Random per-page rotation (misaligned paper feed)
- Vignette / corner darkening (scanner lamp falloff)
- Gaussian noise (sensor grain)
- Warm paper tint (cream/yellowish whites)
- Uneven left-right illumination (scanner lamp gradient)
- Slight blur (halftone + scanner softness)
- Subtle contrast and sharpness reduction

## Requirements

System dependency (provides `pdftoppm`):

```bash
# macOS
brew install poppler

# Ubuntu / Debian
sudo apt install poppler-utils
```

## Installation

```bash
pip install fakescan
```

## Usage

### CLI

```bash
fakescan input.pdf                      # writes input_scanned.pdf
fakescan input.pdf output.pdf           # custom output name
fakescan input.pdf --dpi 150            # lower DPI = smaller file
fakescan input.pdf output.pdf --dpi 300 # high quality
```

### Python API

```python
from fakescan import make_printed_pdf

make_printed_pdf("input.pdf", "output.pdf", dpi=200)
```

Or apply effects to a single PIL image:

```python
from PIL import Image
from fakescan import apply_printed_effect

img = Image.open("page.png")
scanned = apply_printed_effect(img, page_index=0)
scanned.save("page_scanned.png")
```

## License

MIT
