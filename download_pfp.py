import pandas as pd
from duckduckgo_search import DDGS
import requests
import os

df = pd.read_csv('spotify_trimmed.csv')
artists = df['master_metadata_album_artist_name'].dropna().unique()

os.makedirs("artist_images", exist_ok=True)

for artist_name in artists:
    print(f"Searching for: {artist_name}")

    try:
        with DDGS() as ddgs:
            # Search for the artist's Spotify profile picture
            results = ddgs.images(f"{artist_name} spotify profile picture", max_results=1)
            if results:
                image_url = results[0]['image']
                print(f"Downloading: {artist_name} → {image_url}")

                response = requests.get(image_url, timeout=10)
                file_path = os.path.join("artist_images", f"{artist_name}.jpg")

                with open(file_path, 'wb') as f:
                    f.write(response.content)

                print(f"Saved: {file_path}")
            else:
                print(f"No image found for {artist_name}")

    except Exception as e:
        print(f"Error with {artist_name}: {e}")
