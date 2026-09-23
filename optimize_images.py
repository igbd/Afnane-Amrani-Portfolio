import os
from pathlib import Path
from PIL import Image

workspace_root = Path("/Users/tamtamairm3/Desktop/IG/Afnane/Afnane website Portfolio")

print("=== OPTIMIZING PORTFOLIO IMAGES TO WEBP ===")

# 1. Recommendation Letters
rec_dir = workspace_root / "assets/images/recommendations"
for i in range(1, 6):
    src_png = rec_dir / f"letter_{i:02d}_*.png"
    matches = list(rec_dir.glob(f"letter_{i:02d}_*.png"))
    for src in matches:
        dst = src.with_suffix(".webp")
        with Image.open(src) as img:
            img.save(dst, "WEBP", quality=88, method=6)
        print(f"Rec Letter: {src.name} ({src.stat().st_size/1024:.1f}KB) -> {dst.name} ({dst.stat().st_size/1024:.1f}KB)")

# 2. Food Photography (FRR)
food_dir = workspace_root / "assets/work/images"
for i in range(1, 10):
    src = food_dir / f"frr_food_{i}.jpg"
    if src.exists():
        dst = food_dir / f"frr_food_{i}.webp"
        with Image.open(src) as img:
            # Resize from 1600x2400 to crisp 2x retina 800x1200
            w, h = img.size
            if w > 800:
                new_w = 800
                new_h = int(h * (800 / w))
                resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                resized.save(dst, "WEBP", quality=86, method=6)
            else:
                img.save(dst, "WEBP", quality=86, method=6)
        print(f"Food {i}: {src.name} ({src.stat().st_size/1024:.1f}KB) -> {dst.name} ({dst.stat().st_size/1024:.1f}KB)")

# 3. Social Media & Dashboard Analytics Screenshots
sbr_files = [
    "sbr_dash_profile.png",
    "sbr_dash_stats_breakdown.png",
    "sbr_dash_views_1m.png",
    "sbr_fiche_etablissement.jpg",
    "sbr_avis_client.jpg",
    "sbr_google_ads.jpg",
    "flamant_hotel_ad_photo.jpg",
    "tamazing_brand.jpg",
    "tamazing_statistics.jpg",
    "tamazing_feed.jpg",
    "tamazing_bts_3.jpg",
    "tamazing_bts_4.jpg"
]

for sf in sbr_files:
    src = food_dir / sf
    if src.exists():
        dst = src.with_suffix(".webp")
        with Image.open(src) as img:
            w, h = img.size
            # Cap width at 1200 max if larger
            if w > 1200:
                new_w = 1200
                new_h = int(h * (1200 / w))
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            img.save(dst, "WEBP", quality=86, method=6)
        print(f"Screenshot/Media: {src.name} ({src.stat().st_size/1024:.1f}KB) -> {dst.name} ({dst.stat().st_size/1024:.1f}KB)")

# 4. SBR Post Visuals (1-4)
for i in range(1, 5):
    src = food_dir / f"sbr_post_{i}.jpg"
    if src.exists():
        dst = food_dir / f"sbr_post_{i}.webp"
        with Image.open(src) as img:
            w, h = img.size
            if w > 900:
                new_w = 900
                new_h = int(h * (900 / w))
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            img.save(dst, "WEBP", quality=86, method=6)
        print(f"SBR Post {i}: {src.name} ({src.stat().st_size/1024:.1f}KB) -> {dst.name} ({dst.stat().st_size/1024:.1f}KB)")

# 5. Tamazing Full Landing Page
src = food_dir / "tamazing_full_landing_page.jpg"
if src.exists():
    dst = food_dir / "tamazing_full_landing_page.webp"
    with Image.open(src) as img:
        img.save(dst, "WEBP", quality=84, method=6)
    print(f"Landing Page: {src.name} ({src.stat().st_size/1024:.1f}KB) -> {dst.name} ({dst.stat().st_size/1024:.1f}KB)")

# 6. Hero Camera
src = workspace_root / "assets/images/hero_camera.jpg"
if src.exists():
    dst = src.with_suffix(".webp")
    with Image.open(src) as img:
        img.save(dst, "WEBP", quality=86, method=6)
    print(f"Hero Camera: {src.name} ({src.stat().st_size/1024:.1f}KB) -> {dst.name} ({dst.stat().st_size/1024:.1f}KB)")

print("\n=== IMAGE CONVERSION COMPLETE ===")
