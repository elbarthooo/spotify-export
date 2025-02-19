import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

print("✅ Début du script")

# Charger les identifiants Spotify depuis GitHub Actions
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

print("🔑 Identification en cours...")

# Créer un dossier de cache pour stocker le token
CACHE_PATH = ".cache"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="user-library-read",
    open_browser=False,
    cache_path=CACHE_PATH  # Permet de réutiliser le token
))

print("🎵 Récupération des titres likés...")

# Récupérer les titres likés
liked_tracks = []
results = sp.current_user_saved_tracks(limit=50)
while results:
    for item in results['items']:
        track = item['track']
        liked_tracks.append({
            "name": track['name'],
            "artist": track['artists'][0]['name'],
            "album": track['album']['name']
        })
    print(f"📥 {len(liked_tracks)} titres récupérés...")
    results = sp.next(results) if results['next'] else None

print("💿 Récupération des albums enregistrés...")

# Récupérer les albums enregistrés
saved_albums = []
results = sp.current_user_saved_albums(limit=50)
while results:
    for item in results['items']:
        album = item['album']
        saved_albums.append({
            "name": album['name'],
            "artist": album['artists'][0]['name'],
            "release_date": album['release_date']
        })
    print(f"📀 {len(saved_albums)} albums récupérés...")
    results = sp.next(results) if results['next'] else None

print("💾 Sauvegarde des données...")

# Sauvegarder les données dans un fichier JSON
data = {"liked_tracks": liked_tracks, "saved_albums": saved_albums}
with open("spotify_data.json", "w") as f:
    json.dump(data, f, indent=4)

print("✅ Exportation terminée !")
