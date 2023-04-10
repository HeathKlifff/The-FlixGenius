import streamlit as st
import pickle
import pandas as pd
import requests
  # getting title from index


movies_dict = pickle.load(open('moviesdict.pkl','rb')) #rb means read binary
movies = pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommeder System')

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=d1aa166f63fc68c2ba2e94a836a1c632'.format(movie_id))
    data=response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500"+ data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # Taking out the index
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters=[]
    for i in movies_list:
        movieid = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)

        # fetch poster from API
        recommended_movies.append(fetch_poster(movieid))
    return recommended_movies,recommended_movies_posters

selected_movie=st.selectbox(
    'Name of the movie',(movies['title'].values)
)

if st.button('Search For Similar Movie'):
    names,posters = recommend(selected_movie)

    col1,col2,col3,col4,col5 = st.beta_columns(5)
    with col1:
        st.header(names[0])
        st.image(posters[0])
    with col2:
        st.header(names[1])
        st.image(posters[1])
    with col3:
        st.header(names[2])
        st.image(posters[2])
    with col4:
        st.header(names[3])
        st.image(posters[3])
    with col5:
        st.header(names[4])
        st.image(posters[4])

