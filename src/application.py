from os import environ
from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__)
ACCESS_TOKEN = environ.get('SPOTIFY_API_KEY')
SPOTIFY_API_URL = "https://api.spotify.com/v1"
SEARCH_LIMIT = 20
API_PATH = "/api/v1"

## API

# Keep this for debugging
@app.route(API_PATH + '/key')
def get_api_key():
    if ACCESS_TOKEN:
        return ACCESS_TOKEN
    else:
        return "No access token found"


@app.route(API_PATH + '/search')
def search_tracks():
    q = request.args.get('q')
    if (q != ""):
        r = requests.get(
            SPOTIFY_API_URL + "/search",
            params={"q": q, "type": "track", "limit": SEARCH_LIMIT},
            headers={"Authorization": "Bearer " + ACCESS_TOKEN},
        ).json()

        returned_tracks = r["tracks"]["items"]
        tracks = {"tracks": [
            {
                    "name": t["name"],
                    "id": t["id"],
                    "artists": t["artists"],
                    "href": t["external_urls"],
                    "preview_url": t["preview_url"],
                } for t in returned_tracks
            ]
        }
    else:
        tracks = {"tracks": []}

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
    ).json()["tracks"]
    return r

## Server-Side Rendering

@app.route('/')
def render_homepage():
    return render_template("index.html")

@app.route('/search')
def render_search_tracks():
    tracks = search_tracks()["tracks"]
    return render_template("search.html", tracks=tracks, query=request.args.get('q'))

@app.route('/recommend/<track_id>')
def render_recommend_tracks(track_id):
    recommended_tracks = recommend_tracks(track_id)
    return render_template("recommend.html", tracks=recommended_tracks)


def main():
    app.run()

if __name__ == "__main__":
    main()
