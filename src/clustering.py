import ast
import pickle

import pandas as pd
from collections import Counter

class MovieClusterer:

    def __init__(
        self,
        movies_path="data/processed/processed_movies.csv",
        model_path="models/kmeans.pkl"
    ):

        self.movies = pd.read_csv(movies_path)

        with open(model_path, "rb") as file:
            self.kmeans = pickle.load(file)

    def get_cluster(self, movie_id):

        movie = self.movies[
            self.movies["id"] == movie_id
        ]

        if movie.empty:
            return None

        return int(movie.iloc[0]["cluster"])

    def get_movies_in_cluster(self, cluster_id):

        cluster_movies = self.movies[
            self.movies["cluster"] == cluster_id
        ]

        return cluster_movies[
            ["id", "title", "overview"]
        ].copy()

    def get_cluster_size(self, cluster_id):

        return int(
            (
                self.movies["cluster"] == cluster_id
            ).sum()
        )

    def get_cluster_movies(self, cluster_id):

         return self.movies[
              self.movies["cluster"] == cluster_id
         ].copy()

    def get_top_genres(self, cluster_id, top_n=5):

         cluster_movies = self.get_cluster_movies(
              cluster_id
         )

         genre_counter = Counter()

         for genres in cluster_movies["genres"]:

            try:

                 parsed = ast.literal_eval(genres)

                 for genre in parsed:

                    if "name" in genre:
                         genre_counter[
                             genre["name"]
                        ] += 1

            except (ValueError, SyntaxError, TypeError):
                 continue

         return genre_counter.most_common(top_n)