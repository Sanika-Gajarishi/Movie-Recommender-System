import pickle

import pandas as pd
import requests

from src.tmdb_api import TMDBClient


class MovieRecommender:

    def __init__(self):

        self.movies = pd.read_csv(
            "data/processed/processed_movies.csv"
        )

        
        with open("models/similarity.pkl", "rb") as file:
            self.similarity = pickle.load(file)

        
        try:

            self.tmdb = TMDBClient()
            self.tmdb_available = True

        except ValueError:

            self.tmdb = None
            self.tmdb_available = False

    

    def recommend(
        self,
        movie_id,
        number_of_recommendations=5,
        minimum_similarity=0.10
    ):

       

        matches = self.movies[
            self.movies["id"] == movie_id
        ]

        
        if matches.empty:
            return []

        

        movie_index = matches.index[0]

        

        movie_scores = self.similarity[movie_index]

        sorted_scores = sorted(
            list(enumerate(movie_scores)),
            reverse=True,
            key=lambda x: x[1]
        )

        recommendations = []

    

        for index, score in sorted_scores[1:]:

            

            if score < minimum_similarity:
                break

            
            movie = self.movies.iloc[index]

            movie_id = int(movie["id"])

            
            poster_url = None

            

            if self.tmdb_available:

                try:

                    poster_url = self.tmdb.get_movie_poster(
                        movie_id,
                        movie["title"]
                    )

                except (
                    requests.RequestException,
                    ValueError,
                    KeyError
                ):

                    
                    poster_url = None

            

            recommendations.append(
                {
                    "id": movie_id,

                    "title": movie["title"],

                    "score": float(score),

                    "overview": movie.get(
                        "overview",
                        ""
                    ),

                    "genres": movie.get(
                        "genres",
                        ""
                    ),

                    "poster_url": poster_url
                }
            )

           

            if len(recommendations) >= number_of_recommendations:
                break

        

        return recommendations