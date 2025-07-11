import pandas as pd

df = pd.read_csv("combined_spotify_history.csv")

# print(df.columns)
# Index(['ts', 'platform', 'ms_played', 'conn_country', 'ip_addr',
#        'master_metadata_track_name', 'master_metadata_album_artist_name',
#        'master_metadata_album_album_name', 'spotify_track_uri', 'episode_name',
#        'episode_show_name', 'spotify_episode_uri', 'audiobook_title',
#        'audiobook_uri', 'audiobook_chapter_uri', 'audiobook_chapter_title',
#        'reason_start', 'reason_end', 'shuffle', 'skipped', 'offline',
#        'offline_timestamp', 'incognito_mode'],
#       dtype='object')



df['play_datetime'] = df.apply(
    lambda row: pd.to_datetime(row['offline_timestamp'], unit='ms') if row['offline'] else pd.to_datetime(row['ts']),
    axis=1
)
