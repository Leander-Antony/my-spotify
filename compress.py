import pandas as pd
from duckduckgo_search import DDGS
import requests
from PIL import Image
import os
import time
import random

IMAGE_FOLDER = "artist_images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

df = pd.read_csv('spotify_trimmed.csv')
artists = df['master_metadata_album_artist_name'].dropna().unique()

def compress_image(file_path, quality=75):
    try:
        with Image.open(file_path) as img:
            img = img.convert("RGB")
            img.save(file_path, optimize=True, quality=quality)
            print(f"Compressed: {file_path}")
    except Exception as e:
        print(f"Compression failed for {file_path}: {e}")

# Step 1: Verify existing images + collect corrupted and missing files
corrupted_files = []
missing_files = []

print("Verifying and compressing existing images...")

for artist_name in artists:
    safe_filename = f"{artist_name}.jpg"
    file_path = os.path.join(IMAGE_FOLDER, safe_filename)

    if os.path.exists(file_path):
        try:
            with Image.open(file_path) as img:
                img.verify()
            compress_image(file_path, quality=75)
        except Exception:
            print(f"Corrupted: {safe_filename}")
            corrupted_files.append(safe_filename)
    else:
        print(f"Missing: {safe_filename}")
        missing_files.append(safe_filename)

total_to_fix = set(corrupted_files + missing_files)

print(f"Total corrupted files: {len(corrupted_files)}")
print(f"Total missing files: {len(missing_files)}")
print(f"Total files needing download: {len(total_to_fix)}")

# Step 2: Delete corrupted files
for filename in corrupted_files:
    try:
        os.remove(os.path.join(IMAGE_FOLDER, filename))
        print(f"Deleted: {filename}")
    except FileNotFoundError:
        pass

# Step 3: Redownload missing/corrupted images
print("Redownloading and compressing missing/corrupted images...")

for artist_name in artists:
    safe_filename = f"{artist_name}.jpg"
    if safe_filename not in total_to_fix:
        continue

    file_path = os.path.join(IMAGE_FOLDER, safe_filename)

    try:
        with DDGS() as ddgs:
            results = ddgs.images(f"{artist_name} spotify profile picture", max_results=1)
            results = list(results)

            if results:
                image_url = results[0]['image']
                print(f"Downloading: {artist_name} → {image_url}")

                response = requests.get(image_url, timeout=10)
                with open(file_path, 'wb') as f:
                    f.write(response.content)

                compress_image(file_path, quality=75)
                print(f"Saved and compressed: {file_path}")
            else:
                print(f"No image found for {artist_name}")

        time.sleep(random.uniform(0.5, 1.5))

    except Exception as e:
        print(f"Error downloading {artist_name}: {e}")

print("✅ Script complete.")
print(f"Final corrupted count: {len(corrupted_files)}")
print(f"Final missing count: {len(missing_files)}")
