{\rtf1\ansi\ansicpg1252\cocoartf2821
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import os\
import json\
import spotipy\
from spotipy.oauth2 import SpotifyOAuth\
\
# Charger les identifiants Spotify depuis GitHub Actions\
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")\
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")\
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")\
\
# Authentification\
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(\
    client_id=SPOTIPY_CLIENT_ID,\
    client_secret=SPOTIPY_CLIENT_SECRET,\
    redirect_uri=SPOTIPY_REDIRECT_URI,\
    scope="user-library-read"\
))\
\
# R\'e9cup\'e9rer les titres lik\'e9s\
liked_tracks = []\
results = sp.current_user_saved_tracks()\
while results:\
    for item in results['items']:\
        track = item['track']\
        liked_tracks.append(\{\
            "name": track['name'],\
            "artist": track['artists'][0]['name'],\
            "album": track['album']['name']\
        \})\
    results = sp.next(results) if results['next'] else None\
\
# R\'e9cup\'e9rer les albums enregistr\'e9s\
saved_albums = []\
results = sp.current_user_saved_albums()\
while results:\
    for item in results['items']:\
        album = item['album']\
        saved_albums.append(\{\
            "name": album['name'],\
            "artist": album['artists'][0]['name'],\
            "release_date": album['release_date']\
        \})\
    results = sp.next(results) if results['next'] else None\
\
# Sauvegarder les donn\'e9es dans un fichier JSON\
data = \{"liked_tracks": liked_tracks, "saved_albums": saved_albums\}\
with open("spotify_data.json", "w") as f:\
    json.dump(data, f, indent=4)\
\
print("\uc0\u9989  Exportation r\'e9ussie !")\
}