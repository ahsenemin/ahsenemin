"""
Step 3a - Prep a photo for ASCII conversion.

A flatly-lit face converts to a dark, unreadable blob. Three steps fix that:
    1) remove the background (rembg) so only the subject remains
    2) boost local contrast with CLAHE - gives a flat face real highlights/shadows
    3) composite onto pure white so the background maps to the blank end of
       the ASCII ramp (white -> space character)

Usage:
    python scripts/prep_photo.py source-photo.jpg
"""
import io
import os
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PREPPED_PHOTO


def prep_photo(input_path: str, output_path: str = PREPPED_PHOTO) -> None:
    with open(input_path, "rb") as f:
        input_bytes = f.read()

    # 1) remove background -> RGBA with transparency where the bg was
    output_bytes = remove(input_bytes)
    fg = Image.open(io.BytesIO(output_bytes)).convert("RGBA")

    # 2) composite onto pure white
    white_bg = Image.new("RGBA", fg.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, fg).convert("L")  # -> grayscale

    # 3) CLAHE local-contrast boost
    arr = np.array(composited)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    arr = clahe.apply(arr)

    Image.fromarray(arr).save(output_path)
    print(f"Prepped photo written to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanim: python scripts/prep_photo.py <foto-dosyasi>")
        sys.exit(1)
    prep_photo(sys.argv[1])
