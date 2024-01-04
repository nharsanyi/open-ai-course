import openai
import os
import tiktoken
import argparse
import numpy as np
import pickle
import pandas as pd

from matplotlib import pyplot as plt
from tenacity import retry, wait_random_exponential, stop_after_attempt
from sklearn.manifold import TSNE
from openai.embeddings_utils import distances_from_embeddings, indices_of_nearest_neighbors_from_distances

openai.api_key = os.getenv("OPENAI_API_KEY")
path = "resources/wiki_movie_plots_deduped.csv"
embedding_cache_path = "tmp/cache/movie_embeddings.pkl"
model_name = "text-embedding-ada-002"
enc = tiktoken.encoding_for_model(model_name)
cost = 0.0001 # per 1k tokens

try:
    embedding_cache = pd.read_pickle(embedding_cache_path)
except FileNotFoundError:
    embedding_cache = {}
except EOFError:
    embedding_cache = {}


def persist_cache():
    with open(embedding_cache_path, "wb") as embedding_cache_file:
        pickle.dump(embedding_cache, embedding_cache_file)


persist_cache()


def get_embedding(text, model="text-embedding-ada-002", cache=embedding_cache):
    if (text, model) not in cache.keys():
        print(f"found text in cache")
        embedding_cache[(text, model)] = generate_embedding(text, model)
        persist_cache()
    return embedding_cache[(text, model)]


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def generate_embedding(text: str, model='text-embedding-ada-002'):
    print("generate embedding")
    text = text.replace("\n", " ")
    res = openai.Embedding.create(
        input=text,
        model=model
    )
    embedding = res["data"][0]["embedding"]
    return embedding


def main():

    df = pd.read_csv(path)
    movies = df[df["Origin/Ethnicity"] == 'American'] \
        .sort_values("Release Year", ascending=False).head(500)
    # embedding = get_embeddings("some text")
    # print(movies.head())
    movie_plots = movies["Plot"].values
    nr_of_tokens = sum([len(enc.encode(plot)) for plot in movie_plots])
    print(f"Nr of tokens={nr_of_tokens}")
    request_cost = nr_of_tokens / 1000 * cost
    print(f"Estimated cost: {request_cost}")
    plot_embeddings = np.array([get_embedding(plot, model=model_name) for plot in movie_plots])
    # print(plot_embeddings)
    recommend_movies(movie_plots, 5)
    visualise(movies, plot_embeddings)
    # print(embs[:5])


def recommend_movies(movie_plots: list, index_of_source: int, k_nearest_neighbours=3, model="text-embedding-ada-002"):
    print("recommend")
    # get all the embeddings
    embeddings = [get_embedding(s) for s in movie_plots]
    # get embedding for our query string
    query_embedding = embeddings[index_of_source]
    # get distances between our embedding and all other embeddings
    distances = distances_from_embeddings(query_embedding=query_embedding, embeddings=embeddings)
    # get indices of the nearest neighbours
    indices = indices_of_nearest_neighbors_from_distances(distances)
    query_string = movie_plots[index_of_source]
    print(f"query string={query_string}")
    match_count = 0
    for i in indices:
        if query_string == movie_plots[i]:
            continue # original plot, we don't want to return this
        if match_count >= k_nearest_neighbours:
            break
        match_count += 1
        print(f"found {match_count} closest match:")
        print(f"distance: {distances[i]}")
        print(f"plot: {movie_plots[i]}")


def visualise(movies: pd.DataFrame, plot_embeddings):
    # c = np.random.randint(1, 5, size=45)
    # s = np.random.randint(10, 220, size=45)
    # transform to 2D
    tsne = TSNE(random_state=1, n_iter=1000, metric="cosine")
    embs = tsne.fit_transform(plot_embeddings)
    print(embs.shape)
    movies['x'] = embs[:, 0]
    movies['y'] = embs[:, 1]
    movies.to_csv('movies_tsne.csv')
    fig, ax = plt.subplots(figsize=(10, 8))

    scatter = ax.scatter(movies.x, movies.y, alpha=.1)
    legend1 = ax.legend(*scatter.legend_elements(), loc="lower left", title="Classes")
    ax.add_artist(legend1)
    handles, labels = scatter.legend_elements(prop="sizes", alpha=0.6)
    legend2 = ax.legend(handles, labels, loc="upper right", title="Sizes")
    ax.add_artist(legend2)
    plt.show()


if __name__ == "__main__":
    main()
