import os
import subprocess
import json
from pathlib import Path

workspace_root = Path("/Users/tamtamairm3/Desktop/IG/Afnane/Afnane website Portfolio")

with open(workspace_root / "media_audit_result.json", "r") as f:
    data = json.load(f)

videos = data["videos"]

video_info = []

# Use mdls (macOS metadata query) which is always available on macOS to inspect video properties!
for v in videos:
    rel_path = v["rel_path"]
    full_path = workspace_root / rel_path
    
    cmd = ["mdls", "-name", "kMDItemPixelWidth", "-name", "kMDItemPixelHeight", "-name", "kMDItemDurationSeconds", "-name", "kMDItemCodecs", "-name", "kMDItemTotalBitRate", str(full_path)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    
    info = {
        "rel_path": rel_path,
        "size_mb": v["size_mb"],
    }
    
    for line in res.stdout.strip().split("\n"):
        if "=" in line:
            k, val = line.split("=", 1)
            k = k.strip()
            val = val.strip().strip('"')
            if k == "kMDItemPixelWidth":
                info["width"] = val
            elif k == "kMDItemPixelHeight":
                info["height"] = val
            elif k == "kMDItemDurationSeconds":
                try:
                    info["duration_sec"] = round(float(val), 1)
                except:
                    info["duration_sec"] = val
            elif k == "kMDItemCodecs":
                info["codecs"] = val
            elif k == "kMDItemTotalBitRate":
                try:
                    info["bitrate_kbps"] = round(float(val) / 1000)
                except:
                    info["bitrate_kbps"] = val
                    
    video_info.append(info)

print(f"{'Path':<45} | {'Size':<8} | {'Res':<10} | {'Dur':<6} | {'Bitrate'}")
print("-" * 85)
for vi in video_info:
    res_str = f"{vi.get('width', '?')}x{vi.get('height', '?')}"
    dur_str = f"{vi.get('duration_sec', '?')}s"
    br_str = f"{vi.get('bitrate_kbps', '?')} kbps"
    print(f"{vi['rel_path']:<45} | {vi['size_mb']:>5.2f} MB | {res_str:<10} | {dur_str:<6} | {br_str}")
