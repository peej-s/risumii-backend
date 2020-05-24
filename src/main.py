from os import environ
from flask import Flask, request, render_template
from flask_cors import CORS
import requests
import json
from datetime import datetime, timedelta

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "https://risumii-app.netlify.app"}})
CLIENT_CREDENTIALS = environ.get('SPOTIFY_CLIENT_CREDENTIALS')
SPOTIFY_API_URL = "https://api.spotify.com/v1"
SEARCH_LIMIT = 20
API_PATH = "/api/v1"
API_ACCESS_TOKEN = ""
TOKEN_EXPIRY = datetime.now()
OFFSET_KEY = 0
OFFSET_TEMPO = 20


# API
def verify_token():
    global API_ACCESS_TOKEN
    global TOKEN_EXPIRY
    global CLIENT_CREDENTIALS
    if (TOKEN_EXPIRY is None) or (datetime.now() > TOKEN_EXPIRY):
        current_time = datetime.now()
        if (CLIENT_CREDENTIALS):
            token_response = requests.post(
                "https://accounts.spotify.com/api/token",
                data={"grant_type": "client_credentials"},
                headers={"Authorization": "Basic " + CLIENT_CREDENTIALS},
            ).json()
            API_ACCESS_TOKEN = token_response["access_token"]
            expiry_time = int(token_response["expires_in"])
            TOKEN_EXPIRY = current_time + timedelta(seconds=expiry_time)
    return API_ACCESS_TOKEN


@app.route(API_PATH + '/search')
def search_tracks():
    q = request.args.get('q')
    tracks = {"tracks": []}
    if (q != ""):
        token = verify_token()
        r = requests.get(
            SPOTIFY_API_URL + "/search",
            params={"q": q, "type": "track", "limit": SEARCH_LIMIT},
            headers={"Authorization": "Bearer " + token},
        ).json()

        returned_tracks = r["tracks"]["items"]
        tracks["tracks"] = [
            {
                "name": t["name"],
                "id": t["id"],
                "artists": t["artists"],
                "href": t["external_urls"],
                "preview_url": t["preview_url"],
            } for t in returned_tracks
        ]

    return tracks


# Keep this for debugging
@ app.route(API_PATH + '/analyze/<track_id>')
def analyze_track(track_id):
    token = verify_token()
    r = requests.get(
        SPOTIFY_API_URL + "/audio-features/" + track_id,
        headers={"Authorization": "Bearer " + token},
    ).json()
    return r


@ app.route(API_PATH + '/recommend/<track_id>')
def recommend_tracks(track_id):
    token = verify_token()
    track_data = analyze_track(track_id)
    if "error" in track_data:
        return {"error": "Invalid track_id provided"}

    request_params = {
        "seed_tracks": track_id,
        "min_key": track_data["key"],
        "max_key": track_data["key"],
        "min_tempo": track_data["tempo"] - OFFSET_TEMPO,
        "max_tempo": track_data["tempo"] + OFFSET_TEMPO,
        "limit": SEARCH_LIMIT
    }

    r = requests.get(
        SPOTIFY_API_URL + "/recommendations",
        params=request_params,
        headers={"Authorization": "Bearer " + token}
    ).json()

    track_name = requests.get(
        SPOTIFY_API_URL + "/tracks/" + track_id,
        headers={"Authorization": "Bearer " + token}
    ).json()["name"]

    response = {"seed_name": track_name, "tracks": r["tracks"]}
    return response


def main():
    app.run()


if __name__ == "__main__":
    main()
