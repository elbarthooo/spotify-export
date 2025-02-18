import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Chargement des variables d'environnement
from dotenv import load_dotenv
load_dotenv()

# Authentification Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-library-read"
))

# Récupération des titres likés
results = sp.current_user_saved_tracks(limit=10)  # Récupère les 10 premiers morceaux
for idx, item in enumerate(results['items']):
    track = item['track']
    print(f"{idx+1}. {track['name']} - {track['artists'][0]['name']}")
