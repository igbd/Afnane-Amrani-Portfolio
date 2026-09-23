import os
import subprocess
import time
from pathlib import Path
from PIL import Image

workspace_root = Path("/Users/tamtamairm3/Desktop/IG/Afnane/Afnane website Portfolio")
ffmpeg_bin = "/tmp/bin/ffmpeg"
masters_dir = workspace_root / "assets/work/videos_masters"
output_dir = workspace_root / "assets/work/videos"
posters_dir = workspace_root / "assets/work/posters"

posters_dir.mkdir(parents=True, exist_ok=True)

video_files = sorted([f for f in os.listdir(masters_dir) if f.endswith(".mp4")])

total_orig_bytes = 0
total_opt_bytes = 0

print(f"=== BATCH TRANSCODING {len(video_files)} VIDEOS ===")
start_all = time.time()

for idx, vf in enumerate(video_files, 1):
    src = masters_dir / vf
    dst = output_dir / vf
    poster_path = posters_dir / f"{src.stem}.jpg"
    
    orig_size = src.stat().st_size
    total_orig_bytes += orig_size
    
    # Check resolution
    if "flamant_resto_reel_2" in vf:
        scale_filter = "scale=480:854:force_original_aspect_ratio=decrease,pad=480:854:(ow-iw)/2:(oh-ih)/2"
    else:
        scale_filter = "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2"
        
    temp_dst = f"/tmp/opt_{vf}"
    
    cmd = [
        ffmpeg_bin, "-y",
        "-i", str(src),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "22",
        "-maxrate", "1800k",
        "-bufsize", "3600k",
        "-vf", scale_filter,
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        temp_dst
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode == 0 and os.path.exists(temp_dst):
        opt_size = os.path.getsize(temp_dst)
        total_opt_bytes += opt_size
        
        # Replace target file
        os.replace(temp_dst, dst)
        
        # Also ensure crisp poster exists
        poster_temp = f"/tmp/poster_{src.stem}.jpg"
        poster_cmd = [
            ffmpeg_bin, "-y",
            "-ss", "00:00:01.000",
            "-i", str(dst),
            "-vframes", "1",
            "-q:v", "3",
            poster_temp
        ]
        p_res = subprocess.run(poster_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if p_res.returncode == 0 and os.path.exists(poster_temp):
            # Optimize poster with PIL
            with Image.open(poster_temp) as p_img:
                p_img.save(poster_path, "JPEG", quality=82, optimize=True)
            os.remove(poster_temp)
            poster_sz = poster_path.stat().st_size
        else:
            poster_sz = poster_path.stat().st_size if poster_path.exists() else 0
            
        savings_pct = round((1 - opt_size / orig_size) * 100, 1)
        print(f"[{idx:02d}/{len(video_files):02d}] {vf:<28} | {orig_size/(1024*1024):>5.2f}MB -> {opt_size/(1024*1024):>4.2f}MB (-{savings_pct}%) | Poster: {poster_sz/1024:>4.1f}KB")
    else:
        print(f"[{idx:02d}/{len(video_files):02d}] ERROR transcoding {vf}")
        total_opt_bytes += orig_size

elapsed = round(time.time() - start_all, 1)
print("\n=== TRANSCODING COMPLETE ===")
print(f"Time Elapsed: {elapsed}s")
print(f"Total Video Weight Before: {total_orig_bytes / (1024*1024):.2f} MB")
print(f"Total Video Weight After:  {total_opt_bytes / (1024*1024):.2f} MB")
print(f"Total Bandwidth Saved:     {(total_orig_bytes - total_opt_bytes) / (1024*1024):.2f} MB (-{round((1 - total_opt_bytes/total_orig_bytes)*100, 1)}%)")
