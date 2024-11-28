import os
import time
import json
import requests
from kafka import KafkaProducer

# Environment Variables
KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TOPIC_NAME = os.environ.get("TOPIC_NAME")
SLEEP_TIME = int(os.environ.get("SLEEP_TIME", 1))

TMDB_API_KEY = "bb99300f474a467b409edc1fbc61f6da"
BASE_URL = "https://api.themoviedb.org/3"


def fetch_movies(amount=100):
    movies = []
    page = 1
    while len(movies) < amount:
        remaining_movies = amount - len(movies)
        url = f"{BASE_URL}/movie/popular"
        params = {"api_key": TMDB_API_KEY, "language": "en-US", "page": page}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error fetching movies from TMDb: {response.status_code} - {response.text}")
            break
        results = response.json().get("results", [])
        if not results:
            print("No more movies to fetch.")
            break
        movies.extend(results[:remaining_movies])
        if len(movies) >= amount:
            break
    return movies


def format_movie_data(movie):
    try:
        formatted_movie = {
            "id": int(movie.get("id", 0)),
            "title": str(movie.get("title", "")),
            "original_title": str(movie.get("original_title", "")),
            "overview": str(movie.get("overview", "")),
            "original_language": str(movie.get("original_language", "")),
            "adult": bool(movie.get("adult", False)),
            "popularity": float(movie.get("popularity", 0.0)),
            "vote_average": float(movie.get("vote_average", 0.0)),
            "vote_count": int(movie.get("vote_count", 0)),
            "release_date": str(movie.get("release_date", ""))
        }
    except Exception as e:
        print(f"Error formatting movie data: {e}")
        formatted_movie = None

    return formatted_movie


def run():
    iterator = 0
    movies_amount = 500

    print("Setting up TMDB producer at {}".format(KAFKA_BROKER_URL))
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
    )

    movies = fetch_movies(movies_amount)
    for i in range(movies_amount):
        formatted_movie = format_movie_data(movies[i])
        print("Sending new movie data iteration - {}".format(iterator))
        producer.send(TOPIC_NAME, value=formatted_movie)
        print("New movie data sent")
        time.sleep(SLEEP_TIME)
        print("Waking up!")
        iterator += 1

if __name__ == "__main__":
    run()
