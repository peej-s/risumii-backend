# unnamedMusicApp

Cool music app that will probably do this:
Take a song and find other songs that have a matching Key and BPM, and return that back to a user so they can make a cool playlist or something

Also this was Maydha's idea not mine

Requirements:
1) [Flask](https://pypi.org/project/Flask/)
2) [requests](https://pypi.org/project/requests/)
3) [A Spotify API Key](https://developer.spotify.com/documentation/general/guides/authorization-guide/) (This will eventually be removed as a requirement)

How to run:
1) Set an environment variable for SPOTIFY_API_KEY (This was not included in the code for security reasons)  
```export SPOTIFY_API_KEY=YOUR_API_KEY```
2) Run `main.py` using `python3`

Sample Calls
1) Search for a song by Keyword (returns track info for any tracks that Spotify matches to that keyword)  
```curl "http://localhost:5000/search?q=KEYWORD"```
2) Search for recommendations using a `track_id` (a value which is returned by the search endpoint)  
```curl "http://localhost:5000/recommend/TRACK_ID"```
