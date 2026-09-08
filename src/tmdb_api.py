import os
from functools import lru_cache

import requests
from dotenv import load_dotenv


load_dotenv()


class TMDBClient:

    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self):

        self.api_key = os.getenv("TMDB_API_KEY")

        if not self.api_key:
            raise ValueError(
                "TMDB_API_KEY is not set. "
                "Add it to your .env file."
            )

    @lru_cache(maxsize=500)
    def get_movie_details(self, movie_id):

        url = f"{self.BASE_URL}/movie/{movie_id}"

        params = {
            "api_key": self.api_key,
            "language": "en-US"
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    def get_poster_url(self, poster_path):

        if not poster_path:
            return None

        return (
            f"https://image.tmdb.org/t/p/w500"
            f"{poster_path}"
        )

    @lru_cache(maxsize=500)
    def get_movie_poster(self, movie_id, title):

        details = self.get_movie_details(movie_id)
        poster_path = details.get("poster_path")

        if not poster_path:

            response = requests.get(
                f"{self.BASE_URL}/search/movie",
                params={
                    "api_key": self.api_key,
                    "language": "en-US",
                    "query": title
                },
                timeout=10
            )

            response.raise_for_status()

            results = response.json().get(
                "results",
                []
            )

            if results:
                poster_path = results[0].get(
                    "poster_path"
                )

        return self.get_poster_url(poster_path) 