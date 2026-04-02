"""Core image processing logic for fakescan."""

import io
import random
from pathlib import Path

import img2pdf
import numpy as np
import pdf2image
from PIL import Image, ImageEnhance, ImageFilter


def apply_printed_effect(img: Image.Image, page_index: int = 0) -> Image.Image:
    """Apply effects to make an image look like it was printed and scanned."""
    rng = np.random.default_rng(seed=page_index)
    rand = random.Random(page_index)

    if img.mode != "RGB":
        img = img.convert("RGB")

    # 1. Slight random page rotation (simulate misaligned paper feed)
    angle = rand.uniform(-1.2, 1.2)
    img = img.rotate(angle, expand=False, fillcolor=(252, 251, 248))

    arr = np.array(img, dtype=np.float32)
    h, w = arr.shape[:2]

    # 2. Vignette: slightly darker corners (drum/lamp falloff)
    cx, cy = w / 2, h / 2
    Y, X = np.ogrid[:h, :w]
    dist = np.sqrt(((X - cx) / cx) ** 2 + ((Y - cy) / cy) ** 2)
    vignette = 1.0 - 0.06 * np.clip(dist, 0, 1)
    arr *= vignette[:, :, np.newaxis]

    # 3. Gaussian scanner noise
    noise = rng.normal(0, 3.5, arr.shape)
    arr += noise
    arr = np.clip(arr, 0, 255)

    # 4. Warm paper tint (slightly cream/yellowish whites)
    arr[:, :, 0] = np.clip(arr[:, :, 0] * 1.012, 0, 255)  # +red
    arr[:, :, 1] = np.clip(arr[:, :, 1] * 1.005, 0, 255)  # +green (a touch)
    arr[:, :, 2] = np.clip(arr[:, :, 2] * 0.972, 0, 255)  # -blue

    # 5. Simulate uneven illumination (scanner lamp gradient, left-right)
    gradient = np.linspace(0.985, 1.010, w, dtype=np.float32)
    arr *= gradient[np.newaxis, :, np.newaxis]
    arr = np.clip(arr, 0, 255)

    img = Image.fromarray(arr.astype(np.uint8))

    # 6. Slight blur (printer halftone + scanner softness)
    img = img.filter(ImageFilter.GaussianBlur(radius=0.45))

    # 7. Slight contrast reduction (printed ink ≠ perfect black)
    img = ImageEnhance.Contrast(img).enhance(0.93)

    # 8. Slight sharpness reduction
    img = ImageEnhance.Sharpness(img).enhance(0.88)

    return img


def make_printed_pdf(input_path: str, output_path: str, dpi: int = 200) -> None:
    """Convert a PDF to look like it was printed on paper and scanned."""
    src = Path(input_path)
    dst = Path(output_path)

    print(f"Input : {src}")
    print(f"Output: {dst}")
    print(f"DPI   : {dpi}")

    print("\nRendering pages…")
    pages = pdf2image.convert_from_path(str(src), dpi=dpi)
    print(f"  {len(pages)} page(s) found")

    image_bytes: list[bytes] = []
    for i, page in enumerate(pages):
        print(f"  Applying printed effect to page {i + 1}/{len(pages)}…", end=" ", flush=True)
        processed = apply_printed_effect(page, page_index=i)
        buf = io.BytesIO()
        processed.save(buf, format="JPEG", quality=87, optimize=True)
        image_bytes.append(buf.getvalue())
        print("done")

    print("\nWriting output PDF…")
    with open(dst, "wb") as f:
        f.write(img2pdf.convert(image_bytes))

    size_mb = dst.stat().st_size / 1_048_576
    print(f"Saved {dst.name} ({size_mb:.1f} MB)")
