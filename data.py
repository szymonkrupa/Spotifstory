from features import get_api_playlist_tracks, get_api_features, get_api_artist, playlist_name, convertMillis
from auth import get_token
import pandas as pd
from datetime import datetime

#Authorization.
TOKEN = get_token()

#Generate dataframe, using functions from features.py.
def data_generator(playlist_id: str):
    songs_info_from_playlist = get_api_playlist_tracks(playlist_id, TOKEN)
    full_list = []
    # For each song generate a list of features.
    for song in songs_info_from_playlist:
            song_info = song
            features = get_api_features(song['songID'], TOKEN)
            if len(song['artistID']) > 1:
                genres_list_list = ([get_api_artist(artist, TOKEN) for artist in song['artistID']])
                genre_dict = {'genres': [j for i in genres_list_list for j in i]}
            else:
                genre_dict = {'genres': get_api_artist(song['artistID'][0], TOKEN)}
            merge = {**song_info, **features, **genre_dict}
            full_list.append(merge)
            
    df = pd.DataFrame(full_list)
    #Convert miliseconds to min.sec.
    df['duration_ms'] = df['duration_ms'].apply(lambda x: convertMillis(x))
    #Split the column into one with dates, the other with times.
    df[['added_at_date','added_at_hour']] = df['added_at'].str.split('T', expand=True)
    df['added_at_hour'] = df['added_at_hour'].apply(lambda x: datetime.strptime(str(x).replace('Z',''), '%H:%M:%S').time())
    df['added_at_hour'] = pd.to_datetime(df['added_at_hour'], format='%H:%M:%S')
    df['added_at_date'] = pd.to_datetime(df['added_at_date'], format='%Y-%m-%d')
    #Drop unnecessary columns from the dataframe.
    df = df.drop(columns=['artistID', 'songID', 'type', 'id', 'uri', 'track_href', 'analysis_url'])
    return df

#Get a name of the playlist.
def playlist_name_generator(playlist_id: str):
    playlist_nick = playlist_name(playlist_id, TOKEN)
    return playlist_nick['name']
