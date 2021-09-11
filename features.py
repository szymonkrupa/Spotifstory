import spotipy
import time

#Get playlist name from the spotify API.
def playlist_name(playlist_id: str, token: str) -> dict:
    sp = spotipy.Spotify(auth=token)
    try:
        playlist = sp.playlist(playlist_id, fields="name")
        return playlist
    except Exception as e:
        None

#Get playlist items from the spotify API.
def get_api_playlist_tracks(playlist_id: str, token: str) -> list:
    sp = spotipy.Spotify(auth=token)
    try:
        playlist = sp.playlist_items(playlist_id, fields="items(added_at,added_by(id),track(artists(name,id),name,id,duration_ms,popularity,album(name)))")
        seprate_request = [ele for ele in playlist['items']]
        list_of_dict = []
        for ele in seprate_request:
            added_at = {'added_at': ele['added_at']}
            playlist_name = {'playlist_name': ele['added_by']['id']}
            artist_name = {'artist_name': [a_dict['name'] for a_dict in ele['track']['artists']]}
            artist_id = {'artistID': [a_dict['id'] for a_dict in ele['track']['artists']]}
            song_name = {'song_name': ele['track']['name']}
            song_id = {'songID': ele['track']['id']}
            album_name = {'album_name': ele['track']['album']['name']}
            popularity = {'popularity': ele['track']['popularity']}
            duration_ms = {'duration_ms': ele['track']['duration_ms']}
            concat_dict = {**playlist_name, **artist_name, **artist_id, **song_name, **song_id, **album_name, **popularity, **duration_ms, **added_at}
            list_of_dict.append(concat_dict)
        return list_of_dict
    except Exception as e:
        return None

#Get genre of artits from the spotify API.
def get_api_artist(artist_id: str, token: str) -> dict:
    sp = spotipy.Spotify(auth=token)
    try:
        artist_response = sp.artists([artist_id])
        seprate_artist_response = [ele for ele in artist_response['artists']]
        for ele in seprate_artist_response:
            return ele['genres']
    except Exception as e:
        return None
        
#Get track features from the spotify API.
def get_api_features(track_id: str, token: str) -> dict:
    sp = spotipy.Spotify(auth=token)
    try:
        features = sp.audio_features([track_id])
        return features[0]
    except Exception as e:
        return None

#Convert miliseconds to minutes and seconds.
def convertMillis(millis: int) -> float:
    seconds=(millis/1000)
    ty_res = time.gmtime(seconds)
    res = float(time.strftime("%M.%S",ty_res))
    return res
