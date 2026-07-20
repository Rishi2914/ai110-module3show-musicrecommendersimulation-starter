import csv
import heapq
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

GENRE_MATCH_POINTS = 2.0
MOOD_MATCH_POINTS = 1.0
ENERGY_SIMILARITY_MAX_POINTS = 2.0

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file into a list of dicts, casting numeric fields to int/float."""
    numeric_fields = {"id", "energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    songs = []
    with open(csv_path, newline="") as f:
        for row in csv.DictReader(f):
            for field in numeric_fields:
                row[field] = float(row[field]) if "." in row[field] else int(row[field])
            songs.append(row)
    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song against user preferences via genre/mood match bonuses plus energy similarity."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["genre"]:
        score += GENRE_MATCH_POINTS
        reasons.append(f"Matches your favorite genre ({user_prefs['genre']}) (+{GENRE_MATCH_POINTS:.1f})")

    if song["mood"] == user_prefs["mood"]:
        score += MOOD_MATCH_POINTS
        reasons.append(f"Matches your favorite mood ({user_prefs['mood']}) (+{MOOD_MATCH_POINTS:.1f})")

    energy_diff = abs(song["energy"] - user_prefs["energy"])
    energy_points = ENERGY_SIMILARITY_MAX_POINTS * (1 - energy_diff)
    score += energy_points
    reasons.append(
        f"Energy {song['energy']:.2f} is close to your target {user_prefs['energy']:.2f} (+{energy_points:.2f})"
    )

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Scores every song against user_prefs and returns the top k, sorted highest score first."""
    scored = ((song, *score_song(user_prefs, song)) for song in songs)
    return heapq.nlargest(k, scored, key=lambda item: item[1])
