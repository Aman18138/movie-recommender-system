import streamlit as st
import pickle
import pandas as pd
import requests
import os

API_KEY = "e9811014"


def fetch_poster(movie_id, movie_title):
    poster_path = f"posters/{movie_id}.jpg"

    if os.path.exists(poster_path):
        return poster_path

    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    if data.get("Response") == "True":
        poster_url = data.get("Poster")

        if poster_url != "N/A":
            image = requests.get(poster_url).content

            with open(poster_path, "wb") as f:
                f.write(image)

            return poster_path

    return "https://via.placeholder.com/300x450?text=No+Poster"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        movie_title = movies.iloc[i[0]].title

        recommended_movies.append(movie_title)
        recommended_posters.append(fetch_poster(movie_id, movie_title))

    return recommended_movies, recommended_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Check your dataframe columns
print(movies.columns)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a Movie",
    movies['title'].values
)

if st.button("Recommend"):
    recommended_movies, recommended_posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(recommended_posters[0])
        st.text(recommended_movies[0])

    with col2:
        st.image(recommended_posters[1])
        st.text(recommended_movies[1])

    with col3:
        st.image(recommended_posters[2])
        st.text(recommended_movies[2])

    with col4:
        st.image(recommended_posters[3])
        st.text(recommended_movies[3])

    with col5:
        st.image(recommended_posters[4])
        st.text(recommended_movies[4])