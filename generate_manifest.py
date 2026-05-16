#!/usr/bin/env python3
"""
Run this script once to generate music/manifest.json
so the player can find your MP3 files on GitHub Pages.

FOLDER STRUCTURE:
  music/
    rock/
      song1.mp3
      song2.mp3
    rap/
      track1.mp3
    loose_song.mp3      ← ungrouped tracks also supported

Usage:  python generate_manifest.py
"""
import os, json, pathlib

MUSIC_DIR = pathlib.Path("music")
EXTENSIONS = {".mp3", ".ogg", ".wav", ".flac", ".m4a", ".aac"}

result = {}   # { genre: [filenames] }  — or flat list for un-genred files

for item in sorted(MUSIC_DIR.iterdir()):
    if item.is_dir():
        # Genre subfolder
        genre = item.name
        files = sorted(
            f.name for f in item.iterdir()
            if f.is_file() and f.suffix.lower() in EXTENSIONS
        )
        if files:
            result[genre] = files
    elif item.is_file() and item.suffix.lower() in EXTENSIONS:
        # Loose file at root of music/
        result.setdefault("_ungrouped", []).append(item.name)

# If there are only flat/ungrouped files, write as plain array for backwards compat
if list(result.keys()) == ["_ungrouped"]:
    output = result["_ungrouped"]
else:
    # Remove _ungrouped key and fold them in as a separate "other" genre
    ungrouped = result.pop("_ungrouped", [])
    if ungrouped:
        result["other"] = ungrouped
    output = result

manifest_path = MUSIC_DIR / "manifest.json"
manifest_path.write_text(json.dumps(output, indent=2), encoding="utf-8")

total = sum(len(v) for v in (output.values() if isinstance(output, dict) else [output]))
print(f"✓ Written manifest.json — {total} track(s)")

if isinstance(output, dict):
    for genre, files in output.items():
        print(f"  [{genre}]  ({len(files)} tracks)")
        for f in files:
            print(f"    · {f}")
else:
    for f in output:
        print(f"  · {f}")
