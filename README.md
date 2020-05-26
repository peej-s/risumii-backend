# Risumii (リスミー)

Cool music app allows a user to search for a song (by artist or by title) and find playlist recommendations for that song (matching key and similar BPM)
Also this was Maydha's idea not mine.  
Frontend can be found here: https://github.com/peej-s/risumii-frontend

https://risumii-project.nn.r.appspot.com/

Requirements:
1) [Flask](https://pypi.org/project/Flask/)
2) [Flask-Cors] (https://pypi.org/project/Flask-Cors/)
3) [requests](https://pypi.org/project/requests/)
4) [A Spotify API Key](https://developer.spotify.com/documentation/general/guides/authorization-guide/) (This will eventually be removed as a requirement)

How to run:
1) Set an environment variable for SPOTIFY_API_KEY (This was not included in the code for security reasons)  
```export SPOTIFY_API_KEY=YOUR_API_KEY```
2) Run `main.py` using `python3`

Sample Calls
1) Search for a song by Keyword (returns track info for any tracks that Spotify matches to that keyword)  
```curl "https://risumii-project.nn.r.appspot.com/api/v1/search?q=KEYWORD"```
2) Search for recommendations using a `track_id` (a value which is returned by the search endpoint)  
```curl "https://risumii-project.nn.r.appspot.com/api/v1/recommend/TRACK_ID"```
