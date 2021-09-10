import pandas as pd
from collections import Counter
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np

#Top5 most popular songs on the playlist.
def most_popular_song(df=None):
    most_ps = df.nlargest(5, 'popularity')[['artist_name', 'song_name']]
    return most_ps

#Top5 least popular songs on the playlist.
def least_popular_song(df=None):
    least_ps = df.nsmallest(5, 'popularity')[['artist_name', 'song_name']]
    return least_ps

#Generate text with mean values about the playlist features.
def aggregated_features(df=None):
    agg_ft = df[['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'tempo', 'valence']].agg('mean')
    keys = [key.title() for key in agg_ft.keys()]
    values = [round(val,3) for val in agg_ft]
    agg_ft_text_one = f'🤸{keys[0]}: {values[0]}, ⚡{keys[1]}: {values[1]}, 📢{keys[2]}: {values[2]}, 🗣️{keys[3]}: {values[3]}, 🪕{keys[4]}: {values[4]},'
    aff_ft_text_one = f'🎛️{keys[5]}: {values[5]}, 🎉{keys[6]}: {values[6]}, 💨{keys[7]}: {values[7]}, 😊{keys[8]}: {values[8]}'
    return agg_ft_text_one, aff_ft_text_one

#Top5 most frequent genres on the playlist.
def most_common_genre(df=None):
    data_genres = []
    for i in df['genres']:
        data_genres += i

    test_list = list(filter(None, data_genres))
    counter = Counter(test_list)
    top_genres = [gen[0] for gen in counter.most_common(5)]
    return top_genres

#Top5 most frequent artists on the playlist.
def most_common_artist(df=None):
    data_artists = []
    for i in df['artist_name']:
        data_artists += i

    test_list = list(filter(None, data_artists))
    counter = Counter(test_list)
    top_artists = [art[0] for art in counter.most_common(5)]
    return top_artists

#Basic statistics about songs duration
def duration_stats(df):
    max_var = format(df['duration_ms'].max(),'.3f')
    min_var = format(df['duration_ms'].min(),'.3f')
    mean_var = format(df['duration_ms'].mean(),'.3f')
    text_info = "The longest track: {0}, The shortest track: {1}, The average track duration: {2}".format(max_var, min_var, mean_var)
    return text_info

#Bar plot showing the popularity of each song on the playlist.
def songs_popularity_bar(df=None):
    hover_names = [", ".join(df['artist_name'][ind]) + ' - ' + song for ind, song in enumerate(df['song_name'])]
    
    fig = go.Figure(data=go.Bar(x=df.index,
                                    y=df['popularity'],
                                    marker_color=df['popularity'],
                                    text=hover_names))
    return fig

#Bar plot showing the duration of each song on the playlist.
def songs_duration_bar(df=None):
    hover_names = [", ".join(df['artist_name'][ind]) + ' - ' + song for ind, song in enumerate(df['song_name'])]
    
    fig = go.Figure(data=go.Bar(x=df.index,
                                    y=df['duration_ms'],
                                    marker_color=df['duration_ms'],
                                    text=hover_names))
    return fig

#Scatter plot showing the tempo of each song on the playlist.
def song_tempo_plot(df=None):
    hover_names = [", ".join(df['artist_name'][ind]) + ' - ' + song for ind, song in enumerate(df['song_name'])]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['tempo'],
                    mode='lines+markers',
                    name="Tempo",
                    text=hover_names))
    return fig

#Scatter plot showing some of the features of each song on the playlist.
def song_features_plot(df=None):
    hover_names = [", ".join(df['artist_name'][ind]) + ' - ' + song for ind, song in enumerate(df['song_name'])]
    
    fig = go.Figure()
    columns = ["acousticness","danceability","energy","speechiness","liveness","valence"]
    for col in columns:
        fig.add_trace(go.Scatter(x=df.index, y=df[col],
                        mode='lines+markers',
                        name=col,
                        text=hover_names))
    return fig

#Pie chart showing components of each key in the playlist.
def keys_piechart(df=None):
    labels = ["acousticness","danceability","energy","speechiness","liveness","valence"]
    key_values = df.groupby('key')[["acousticness","danceability","energy","speechiness","liveness","valence"]].mean().values

    values_d, counts_d = np.unique(df['key'], return_counts=True)
    songs_per_key = dict(zip(values_d.T, counts_d.T))
    songs_per_key = [f'Key{c[0]} - {c[1]} songs' for c in songs_per_key.items()]

    specs = [[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}],
            [{'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}],
            [{'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}]]
    # subplot_titles = [f'Key{c}' for c, i in enumerate(key_values)]
    fig = make_subplots(rows=3, cols=4, specs=specs, subplot_titles=songs_per_key)

    for c, v in enumerate(key_values):
        if c+1 <=4:
            fig.add_trace(go.Pie(labels=labels, values=v), 1, c+1)
        elif c+1 >=5 and c+1 <=8:
            fig.add_trace(go.Pie(labels=labels, values=v), 2, c-3)
        else:
            fig.add_trace(go.Pie(labels=labels, values=v), 3, c-7)
    fig.update_traces(hoverinfo='label+percent+name', textinfo='none')
    fig = go.Figure(fig)
    return fig

#Bar plot showing when songs were added to the playlist (day).
def date_song_added(df=None):
    if len(df['added_at_date'].unique()) > 1:
        values_d, counts_d = np.unique(df['added_at_date'], return_counts=True)
        fig_d = px.bar(x=values_d, y=counts_d, color=counts_d)
        fig_d.update_xaxes(type='date', range=[values_d.min(),values_d.max()], title="Date")
        fig_d.update_yaxes(title="Amount")
        fig_d.update_layout(bargap=(1 / len(values_d) * 1.8))
        return fig_d
    else:
        return None

#Bar plot showing when songs were added to the playlist (hour).
def hour_song_added(df=None):
    if len(df['added_at_date'].unique()) > 1:
        values_h, counts_h = np.unique([pd.Timestamp(1970, 1, 1, h.hour) for h in df['added_at_hour']], return_counts=True)
        fig_h = px.bar(x=values_h, y=counts_h, color=counts_h)
        fig_h.update_xaxes(type='date', range=[0,86400000], title="Hour", tickformat='%H:%M')
        fig_h.update_yaxes(title="Amount")
        return fig_h
    else:
        return None