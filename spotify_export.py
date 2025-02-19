import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Charger les identifiants Spotify depuis GitHub Actions
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

# Authentification
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="user-library-read"
))

# Récupérer les titres likés
liked_tracks = []
results = sp.current_user_saved_tracks()
while results:
    for item in results['items']:
        track = item['track']
        liked_tracks.append({
            "name": track['name'],
            "artist": track['artists'][0]['name'],
            "album": track['album']['name']
        })
    results = sp.next(results) if results['next'] else None

# Récupérer les albums enregistrés
saved_albums = []
results = sp.current_user_saved_albums()
while results:
    for item in results['items']:
        album = item['album']
        saved_albums.append({
            "name": album['name'],
            "artist": album['artists'][0]['name'],
            "release_date": album['release_date']
        })
    results = sp.next(results) if results['next'] else None

# Sauvegarder les données dans un fichier JSON
data = {"liked_tracks": liked_tracks, "saved_albums": saved_albums}
with open("spotify_data.json", "w") as f:
    json.dump(data, f, indent=4)

print("✅ Exportation réussie !")
