import os
import re
import json
from pathlib import Path
from PIL import Image

workspace_root = Path("/Users/tamtamairm3/Desktop/IG/Afnane/Afnane website Portfolio")

# Read index.html, styles.css, app.js
html_content = (workspace_root / "index.html").read_text(encoding="utf-8", errors="ignore")
css_content = (workspace_root / "styles.css").read_text(encoding="utf-8", errors="ignore")
js_content = (workspace_root / "app.js").read_text(encoding="utf-8", errors="ignore")

all_code = html_content + "\n" + css_content + "\n" + js_content

# Scan all media in assets/
media_extensions = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg", ".mp4", ".mov", ".webm", ".pdf", ".m4v"}
all_media_files = []

for root, dirs, files in os.walk(workspace_root / "assets"):
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in media_extensions:
            full_path = Path(root) / file
            rel_path = full_path.relative_to(workspace_root).as_posix()
            size = full_path.stat().st_size
            
            # Check dimensions if image
            dims = None
            if ext in {".png", ".jpg", ".jpeg", ".webp"}:
                try:
                    with Image.open(full_path) as img:
                        dims = img.size
                except Exception:
                    dims = None
            
            # Check if referenced in code
            # Check rel_path, or filename
            is_referenced_rel = rel_path in all_code
            is_referenced_name = file in all_code
            is_referenced = is_referenced_rel or is_referenced_name

            all_media_files.append({
                "rel_path": rel_path,
                "file_name": file,
                "ext": ext,
                "size_bytes": size,
                "size_mb": round(size / (1024 * 1024), 2),
                "dims": dims,
                "is_referenced": is_referenced
            })

# Sort by size descending
all_media_files.sort(key=lambda x: x["size_bytes"], reverse=True)

# Also find all media references in index.html specifically
media_refs_html = []
# Find src="...", href="...", data-video-src="...", data-img="...", data-pdf="..."
ref_pattern = re.compile(r'(?:src|href|data-video-src|data-img|data-pdf|poster)=["\']([^"\']+\.(?:png|jpg|jpeg|webp|gif|svg|mp4|mov|webm|pdf|m4v))["\']', re.IGNORECASE)
for match in ref_pattern.finditer(html_content):
    media_refs_html.append(match.group(1))

# Also in styles.css url(...)
css_url_pattern = re.compile(r'url\(["\']?([^"\'\)]+\.(?:png|jpg|jpeg|webp|gif|svg|mp4|mov|webm|pdf|m4v))["\']?\)', re.IGNORECASE)
for match in css_url_pattern.finditer(css_content):
    media_refs_html.append(match.group(1))

unique_refs = sorted(list(set(media_refs_html)))

# Summaries
total_assets_count = len(all_media_files)
total_assets_size = sum(f["size_bytes"] for f in all_media_files)
referenced_files = [f for f in all_media_files if f["is_referenced"]]
unreferenced_files = [f for f in all_media_files if not f["is_referenced"]]

ref_size = sum(f["size_bytes"] for f in referenced_files)
unref_size = sum(f["size_bytes"] for f in unreferenced_files)

videos = [f for f in referenced_files if f["ext"] in {".mp4", ".mov", ".webm", ".m4v"}]
images = [f for f in referenced_files if f["ext"] in {".png", ".jpg", ".jpeg", ".webp"}]
pdfs = [f for f in referenced_files if f["ext"] == ".pdf"]

print("=== MEDIA AUDIT SUMMARY ===")
print(f"Total media files in assets/: {total_assets_count} ({round(total_assets_size / (1024*1024), 2)} MB)")
print(f"Referenced media files: {len(referenced_files)} ({round(ref_size / (1024*1024), 2)} MB)")
print(f"Unreferenced / unused files in assets/: {len(unreferenced_files)} ({round(unref_size / (1024*1024), 2)} MB)")
print()
print(f"Referenced Videos: {len(videos)} ({round(sum(v['size_bytes'] for v in videos)/(1024*1024), 2)} MB)")
print(f"Referenced Images: {len(images)} ({round(sum(i['size_bytes'] for i in images)/(1024*1024), 2)} MB)")
print(f"Referenced PDFs: {len(pdfs)} ({round(sum(p['size_bytes'] for p in pdfs)/(1024*1024), 2)} MB)")
print()

print("--- TOP 20 LARGEST REFERENCED ASSETS ---")
for f in referenced_files[:20]:
    dims_str = f"{f['dims'][0]}x{f['dims'][1]}" if f['dims'] else "N/A"
    print(f"{f['size_mb']:>6.2f} MB | {f['ext']:<5} | {dims_str:<11} | {f['rel_path']}")

print("\n--- UNREFERENCED / DUPLICATE ASSETS ---")
for f in unreferenced_files:
    dims_str = f"{f['dims'][0]}x{f['dims'][1]}" if f['dims'] else "N/A"
    print(f"{f['size_mb']:>6.2f} MB | {f['ext']:<5} | {dims_str:<11} | {f['rel_path']}")

# Output json for programmatic use
result_data = {
    "total_size_mb": round(total_assets_size / (1024*1024), 2),
    "ref_size_mb": round(ref_size / (1024*1024), 2),
    "unref_size_mb": round(unref_size / (1024*1024), 2),
    "videos": videos,
    "images": images,
    "pdfs": pdfs,
    "unreferenced": unreferenced_files
}

with open(workspace_root / "media_audit_result.json", "w", encoding="utf-8") as out:
    json.dump(result_data, out, indent=2)
