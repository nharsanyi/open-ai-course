import openai
import os
import argparse
import json
import spotipy
import urllib.parse
from spotipy.oauth2 import SpotifyClientCredentials

openai.api_key = os.getenv("OPENAI_API_KEY")
sp = spotipy.Spotify(
    auth_manager=spotipy.SpotifyOAuth(client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                                      client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                                      redirect_uri="http://localhost:9999",
                                      cache_path=".cache",
                                      scope='playlist-modify-private')
)


def main():
    q, n, user_id = init()
    playlist = get_playlist_recommendation_from_chatgpt(q, n)

    track_ids = []
    for track in playlist:
        track_ids.append(fetch_track(track['artist'], track['song']))
    create_playlist(track_ids, q, user_id)


def init():
    parser = argparse.ArgumentParser(description="Spotify playlist generator for a given mood, theme, activity etc.")
    parser.add_argument("--query", type=str)
    parser.add_argument("--n", type=int, help="The number of songs required in the playlist")
    args = parser.parse_args()
    current_user = sp.current_user()
    print(current_user)
    assert current_user is not None
    user_id = current_user['id']
    print(user_id)
    return args.query, args.n, user_id


def create_playlist(track_ids: list, name: str, user_id: str):
    print(f"create playlist with {len(track_ids)} songs with {name} for {user_id}")
    playlist = sp.user_playlist_create(user=user_id, name=f"chatgpt-{name}", public=False, collaborative=False, description="chatgpt-test")
    playlist_id = playlist['id']
    sp.playlist_add_items(playlist_id=playlist_id, items=track_ids)


def fetch_track(artist: str, song: str):
    query = urllib.parse.quote(f"track:{song} artist:{artist}")
    res = sp.search(q=query, type='track', limit=5)
    track_id = res['tracks']['items'][0]['id']
    return track_id


def get_playlist_recommendation_from_chatgpt(prompt: str, count=8):
    example_json = """
        [
          {"song": "Happy", "artist": "Pharrell Williams"},
          {"song": "Don't Stop Me Now", "artist": "Queen"},
          {"song": "Can't Stop The Feeling", "artist": "Justin Timberlake"},
          {"song": "I Wanna Dance with Somebody", "artist": "Whitney Houston"},
          {"song": "Hey Ya!", "artist": "OutKast"},
          {"song": "Walking on Sunshine", "artist": "Katrina and the Waves"},
          {"song": "Three Little Birds", "artist": "Bob Marley"},
          {"song": "Good Vibrations", "artist": "The Beach Boys"},
          {"song": "Dancing Queen", "artist": "ABBA"},
          {"song": "Waka Waka (This Time for Africa)", "artist": "Shakira"}
        ]
    """

    messages = [
        {"role": "system", "content": """
            You are a helpful playlist generating assistant.
            You should generate a list of songs and their artists according to a text prompt.
            You should return a JSON array, where each element follows this format: 
            {"song": <song title>, "artist": <artist_name>}
            """
         },
        {"role": "user", "content": "Generate a playlist of 5 songs based on this prompt: super happy songs"},
        {"role": "assistant", "content": example_json},
        {"role": "user", "content": f"Generate a playlist of {count} songs based on this prompt: {prompt}"}
    ]

    print(f"Generating playlist for `{prompt}`")
    res = openai.ChatCompletion.create(
        messages=messages,
        model='gpt-4',
        max_tokens=400
    )
    return json.loads(res["choices"][0]["message"]["content"])


if __name__ == "__main__":
    main()
