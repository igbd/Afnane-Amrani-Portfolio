import re
from pathlib import Path

workspace_root = Path("/Users/tamtamairm3/Desktop/IG/Afnane/Afnane website Portfolio")
index_file = workspace_root / "index.html"
content = index_file.read_text(encoding="utf-8")

# 1. Update <video class="mockup-reel-video" src="..." preload="metadata"> to data-src="..." preload="none"
video_pattern = re.compile(r'(<video class="mockup-reel-video"[^>]*?)src="([^"]+)"([^>]*?)preload="metadata"([^>]*?>)', re.IGNORECASE)
content, v_count = video_pattern.subn(r'\1data-src="\2"\3preload="none"\4', content)
print(f"Updated {v_count} mockup videos to data-src and preload='none'")

# 2. Image Replacements to WebP
replacements = [
    # Hero journey photo
    ('assets/images/journey_photo.png', 'assets/images/journey_photo.webp'),
    ('assets/images/hero_camera.jpg', 'assets/images/hero_camera.webp'),
    
    # Recommendation letters
    ('assets/images/recommendations/letter_01_hand_in_hand.png', 'assets/images/recommendations/letter_01_hand_in_hand.webp'),
    ('assets/images/recommendations/letter_02_aiesec.png', 'assets/images/recommendations/letter_02_aiesec.webp'),
    ('assets/images/recommendations/letter_03_dar_essaki.png', 'assets/images/recommendations/letter_03_dar_essaki.webp'),
    ('assets/images/recommendations/letter_04_tamazing.png', 'assets/images/recommendations/letter_04_tamazing.webp'),
    ('assets/images/recommendations/letter_05_zarrouk_film.png', 'assets/images/recommendations/letter_05_zarrouk_film.webp'),
    
    # SBR Dashboard & Social
    ('assets/work/images/sbr_dash_profile.png', 'assets/work/images/sbr_dash_profile.webp'),
    ('assets/work/images/sbr_dash_stats_breakdown.png', 'assets/work/images/sbr_dash_stats_breakdown.webp'),
    ('assets/work/images/sbr_dash_views_1m.png', 'assets/work/images/sbr_dash_views_1m.webp'),
    ('assets/work/images/sbr_fiche_etablissement.jpg', 'assets/work/images/sbr_fiche_etablissement.webp'),
    ('assets/work/images/sbr_avis_client.jpg', 'assets/work/images/sbr_avis_client.webp'),
    ('assets/work/images/sbr_google_ads.jpg', 'assets/work/images/sbr_google_ads.webp'),
    
    # SBR Posts
    ('assets/work/images/sbr_post_1.jpg', 'assets/work/images/sbr_post_1.webp'),
    ('assets/work/images/sbr_post_2.jpg', 'assets/work/images/sbr_post_2.webp'),
    ('assets/work/images/sbr_post_3.jpg', 'assets/work/images/sbr_post_3.webp'),
    ('assets/work/images/sbr_post_4.jpg', 'assets/work/images/sbr_post_4.webp'),
    
    # Flamant Hotel
    ('assets/work/images/flamant_hotel_ad_photo.jpg', 'assets/work/images/flamant_hotel_ad_photo.webp'),
    
    # Tamazing
    ('assets/work/images/tamazing_brand.jpg', 'assets/work/images/tamazing_brand.webp'),
    ('assets/work/images/tamazing_statistics.jpg', 'assets/work/images/tamazing_statistics.webp'),
    ('assets/work/images/tamazing_feed.jpg', 'assets/work/images/tamazing_feed.webp'),
    ('assets/work/images/tamazing_bts_3.jpg', 'assets/work/images/tamazing_bts_3.webp'),
    ('assets/work/images/tamazing_bts_4.jpg', 'assets/work/images/tamazing_bts_4.webp'),
    ('assets/work/images/tamazing_full_landing_page.jpg', 'assets/work/images/tamazing_full_landing_page.webp'),
]

# Add Food 1-9
for i in range(1, 10):
    replacements.append((f'assets/work/images/frr_food_{i}.jpg', f'assets/work/images/frr_food_{i}.webp'))

for old, new in replacements:
    c = content.count(old)
    if c > 0:
        content = content.replace(old, new)
        print(f"Replaced {c} instance(s) of {old} -> {new}")

# 3. Add decoding="async" and loading="lazy" to images that lack them
def add_img_attrs(match):
    tag = match.group(0)
    # Check if in hero (we will handle hero separately)
    if 'decoding=' not in tag:
        tag = tag[:-1] + ' decoding="async"' + tag[-1]
    if 'loading=' not in tag:
        tag = tag[:-1] + ' loading="lazy"' + tag[-1]
    return tag

# Split content: hero section (before line with id="about") vs below fold
parts = content.split('<section class="section about-section"', 1)
if len(parts) == 2:
    hero_part = parts[0]
    below_fold = '<section class="section about-section"' + parts[1]
    
    # In below_fold, ensure all <img> have loading="lazy" and decoding="async"
    img_pattern = re.compile(r'<img\s+[^>]+>', re.IGNORECASE)
    below_fold_updated = img_pattern.sub(add_img_attrs, below_fold)
    
    content = hero_part + below_fold_updated
    print("Added loading='lazy' and decoding='async' to all below-the-fold images")

index_file.write_text(content, encoding="utf-8")
print("=== index.html successfully updated! ===")
