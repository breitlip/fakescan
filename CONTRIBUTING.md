# Contributing to fakescan

## Local development setup

### 1. Prerequisites

Install [poppler](https://poppler.freedesktop.org/), which provides `pdftoppm`:

```bash
# macOS
brew install poppler

# Ubuntu / Debian
sudo apt install poppler-utils
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install in editable mode

```bash
pip install -e .
```

This installs the package so that any changes you make to files under `fakescan/` are reflected immediately — no reinstall needed.

### 4. Run the CLI against a real PDF

```bash
fakescan -h                          # show help
fakescan input.pdf                   # writes input_scanned.pdf
fakescan input.pdf output.pdf --dpi 150
```

You can also invoke it as a module (without the entry point):

```bash
python -m fakescan input.pdf
```

### 5. Exercise the Python API directly

```python
from fakescan import make_printed_pdf, apply_printed_effect

# Full pipeline
make_printed_pdf("input.pdf", "output.pdf", dpi=200)

# Single image
from PIL import Image
img = Image.open("page.png")
scanned = apply_printed_effect(img, page_index=0)
scanned.save("out.png")
```

### 6. Deactivate when done

```bash
deactivate
```
