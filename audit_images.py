import os
import re
import json
from pathlib import Path
from PIL import Image

workspace_root = Path("/Users/tamtamairm3/Desktop/IG/Afnane/Afnane website Portfolio")

with open(workspace_root / "media_audit_result.json", "r") as f:
    data = json.load(f)

images = data["images"]

print(f"{'Path':<50} | {'Size':<8} | {'Dims':<11} | {'Aspect':<6}")
print("-" * 85)

for img in sorted(images, key=lambda x: x["size_bytes"], reverse=True):
    dims_str = f"{img['dims'][0]}x{img['dims'][1]}" if img.get('dims') else "N/A"
    aspect_str = f"{round(img['dims'][0]/img['dims'][1], 2)}" if img.get('dims') and img['dims'][1] else "N/A"
    print(f"{img['rel_path']:<50} | {img['size_mb']:>5.2f} MB | {dims_str:<11} | {aspect_str:<6}")
