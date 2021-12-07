import streamlit as st
from playlistid import playlist_id_cleaner
from data import data_generator, playlist_name_generator
from dashboard import (
    most_popular_song,
    least_popular_song,
    aggregated_features,
    most_common_genre,
    most_common_artist,
    songs_popularity_bar,
    song_features_plot,
    keys_piechart,
    date_song_added,
    hour_song_added,
    songs_duration_bar,
    duration_stats,
    song_tempo_plot,
)


st.set_page_config(page_title="SpotifStory", page_icon="🎵", layout="wide")


# Container
header = st.container()
playlist_link = st.container()
dashboard = st.container()


with header:
    col_a, col_b, col_c = header.columns([1, 2, 1])
    col_b.subheader("Welcome!")
    col_b.text(
        "Check out what story playlist has to say about herself!\nMore info on the sidebar.*"
    )
    col_b.markdown("___")

with playlist_link:
    buffer_one, use_info, buffer_two = playlist_link.columns([1, 2, 1])
    link_data = use_info.text_input(
        "spotify playlist link",
        "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=b487fd2dd05047cf",
    )


playlist_link.markdown('___')
with dashboard:
    if use_info.button("Play"):
        output_id = playlist_id_cleaner(link_data)
        data = data_generator(output_id)

        dashboard.header(playlist_name_generator(output_id))

        dashboard.subheader("General statistics about the playlist:")
        dashboard.text(aggregated_features(data)[0])
        dashboard.text(aggregated_features(data)[1])

        col1, col2 = dashboard.columns(2)
        col1.subheader("Playlist genres:")
        col1.text(most_common_genre(data))
        col2.subheader("Top5 most present artists on the playlist:")
        col2.text(most_common_artist(data))

        col3, buffer0, col4 = dashboard.columns([3, 1, 4])
        col3.subheader("Top5 most popular songs on the playlist:")
        col3.write(most_popular_song(data))
        col4.subheader("Top5 least popular songs on the playlist:")
        col4.write(least_popular_song(data))

        dashboard.subheader("Popularity of the songs:")
        dashboard.plotly_chart(songs_popularity_bar(
            data), use_container_width=True)

        dashboard.subheader("Duration of the songs:")
        dashboard.write(duration_stats(data))
        dashboard.plotly_chart(songs_duration_bar(data),
                               use_container_width=True)

        dashboard.subheader("Features of the songs:")
        dashboard.plotly_chart(song_features_plot(data),
                               use_container_width=True)

        dashboard.subheader("Tempo of the songs:")
        dashboard.plotly_chart(song_tempo_plot(data), use_container_width=True)

        if date_song_added(data) != None:
            col5, col6 = dashboard.columns(2)
            col5.subheader("At what date are most songs added:")
            col5.plotly_chart(date_song_added(data), use_container_width=True)
            col6.subheader("At what time are most songs added:")
            col6.plotly_chart(hour_song_added(data), use_container_width=True)
        else:
            pass

        dashboard.subheader("Keys analysis:")
        dashboard.plotly_chart(keys_piechart(data), use_container_width=True)


# Sidebar
st.sidebar.image('media/SpotifStory.png')
st.sidebar.subheader('⚠️INFO&HOWTO:')
st.sidebar.write(
    "To know how to get spotify playlist link, check out this 🌐: [link](https://tutstake.com/2020/08/spotify-playlist-link.html)")
st.sidebar.write("*Playlist can not be longer than 100 tracks.")
st.sidebar.write(
    "📱If you are using a smartphone, I recommend using it horizontally.")
st.sidebar.markdown('___')
# Features description
st.sidebar.subheader("Features description:")
st.sidebar.write(
    "🤸Danceability - describes how suitable a track is for dancing based on a combination of musical elements including tempo,\
     rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable."
)
st.sidebar.write(
    "⚡Energy - a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. \
    Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach \
    prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy."
)
st.sidebar.write(
    "📢Loudness - the overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track \
    and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological \
    correlate of physical strength (amplitude). Values typical range between -60 and 0 db."
)
st.sidebar.write(
    "🗣️Speechiness - detects the presence of spoken words in a track. The more exclusively speech-like the recording\
    (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that \
    are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and \
    speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks."
)
st.sidebar.write(
    "🪕Acousticness - a confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic."
)
st.sidebar.write(
    "🎛️Instrumentalness - predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context.\
    Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track \
    contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0."
)
st.sidebar.write(
    "🎉Liveness - detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live.\
     A value above 0.8 provides strong likelihood that the track is live."
)
st.sidebar.write(
    "💨Tempo - the overall estimated tempo of a track in beats per minute (BPM). In musical terminology,\
     tempo is the speed or pace of a given piece and derives directly from the average beat duration."
)
st.sidebar.write(
    "😊Valence - a measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive\
     (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry)."
)
st.sidebar.write(
    "🤘Popularity - the popularity of the track. The value will be between 0 and 100, with 100 being the most popular.\
     The popularity is calculated by algorithm and is based, in the most part, on the total number of plays the track has had and how recent those plays are.\
     Generally speaking, songs that are being played a lot now will have a higher popularity than songs that were played a lot in the past.\
     Artist and album popularity is derived mathematically from track popularity. Note that the popularity value may lag actual popularity by a few days:\
     the value is not updated in real time."
)
st.sidebar.write(
    "🎼Key - the estimated overall key of the track. Integers map to pitches using standard Pitch Class notation.\
     E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1."
)