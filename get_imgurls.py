import pandas as pd
import urllib.parse

# Load the CSV
df = pd.read_csv("spotify_trimmed.csv")

# Drop NaNs and get unique artist names
unique_artists = df["master_metadata_album_artist_name"].dropna().unique()

# Format image URLs
base_url = "https://github.com/Leander-Antony/my-spotify/blob/main/artist_images/"
image_data = []

for artist in unique_artists:
    encoded_name = urllib.parse.quote(artist)
    image_url = f"{base_url}{encoded_name}.jpg?raw=true"  # <-- Appended ?raw=true
    image_data.append({"artist_name": artist, "image_url": image_url})

# Create a new DataFrame and save it
output_df = pd.DataFrame(image_data)
output_df.to_csv("artist_image_urls.csv", index=False)

print("CSV with artist image URLs (with ?raw=true) has been created as 'artist_image_urls.csv'")
