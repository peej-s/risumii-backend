from os import environ
from flask import Flask, request
import requests
import json

app = Flask(__name__)
ACCESS_TOKEN = environ.get('SPOTIFY_API_KEY')
SPOTIFY_API_URL = "https://api.spotify.com/v1"
SEARCH_LIMIT = 5
API_PATH = "/api/v1"


# Keep this for debugging
@app.route(API_PATH + '/key')
def get_api_key():
    if ACCESS_TOKEN:
        return ACCESS_TOKEN
    else:
        return "No access token found"


@app.route(API_PATH + '/search')
def list_tracks():
    q = request.args.get('q')
    r = requests.get(
        SPOTIFY_API_URL + "/search",
        params={"q": q, "type": "track", "limit": SEARCH_LIMIT},
        headers={"Authorization": "Bearer " + ACCESS_TOKEN},
    ).json()

    # Not sure if it is necessary right now to remove the excess data,
    # but I'll keep it around so its easier for the frontend
    returned_tracks = r["tracks"]["items"]
    tracks = {"tracks": [
           {
                "track_name": t["name"],
                "track_id": t["id"],
                "artists": t["artists"],
                "preview_url": t["preview_url"]
            } for t in returned_tracks
        ]
    }

    return tracks


# Keep this for debugging
@app.route(API_PATH + '/analyze/<track_id>')
def analyze_track(track_id):
    r = requests.get(
        SPOTIFY_API_URL + "/audio-features/" + track_id,
        headers={"Authorization": "Bearer " + ACCESS_TOKEN},
    ).json()
    return r


@app.route(API_PATH + '/recommend/<track_id>')
def recommend_tracks(track_id):
    track_data = analyze_track(track_id)
    request_params = {
        "seed_tracks": track_id,
        "target_key": track_data["key"],
        "target_tempo": track_data["tempo"],
        "limit": SEARCH_LIMIT
    }
    r = requests.get(
        SPOTIFY_API_URL + "/recommendations",
        params=request_params,
        headers={"Authorization": "Bearer " + ACCESS_TOKEN}
    ).json()
    return r


def main():
    app.run()

if __name__ == "__main__":
    main()
