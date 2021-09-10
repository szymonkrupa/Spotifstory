import re

#Generate playlistID from a link to a playlist.
def playlist_id_cleaner(url: str) -> str:
    try:
        playlist_id = re.search(r'playlist\/(.*?)\?si', url).group(1)
        return playlist_id
    except re.error:
        print('Invalid playlist link')