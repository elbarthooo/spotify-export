import os
import csv
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SCOPE = "user-library-read"

# Vérifier que les variables d'environnement sont bien chargées
if not all([SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI]):
    raise ValueError("Les variables d'environnement SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET ou SPOTIPY_REDIRECT_URI sont manquantes. Vérifie ton fichier .env.")

# Initialiser Spotipy avec OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
))

# Fonction pour récupérer tous les titres likés
def get_liked_tracks():
    print("✅ Authentification réussie !")
    print("🎵 Récupération des titres likés...")
    tracks = []
    results = sp.current_user_saved_tracks(limit=50)
    
    while results:
        for item in results['items']:
            track = item['track']
            tracks.append([track['name'], track['artists'][0]['name']])
        
        if results['next']:
            results = sp.next(results)
            time.sleep(1)  # Pause pour éviter le rate limit de l'API
        else:
            break
    return tracks

# Fonction pour enregistrer les titres dans un fichier CSV
def save_to_csv(tracks, filename="spotify_liked_tracks.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Titre", "Artiste"])
        writer.writerows(tracks)
    print(f"✅ {len(tracks)} titres enregistrés dans {filename}")

if __name__ == "__main__":
    liked_tracks = get_liked_tracks()
    save_to_csv(liked_tracks)