"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


PROFILES = [
    ("High-Energy Pop", {"genre": "pop", "mood": "happy", "energy": 0.85}),
    ("Chill Lofi", {"genre": "lofi", "mood": "chill", "energy": 0.35}),
    ("Deep Intense Rock", {"genre": "rock", "mood": "intense", "energy": 0.90}),
]


def main() -> None:
    songs = load_songs("data/songs.csv")

    for profile_name, user_prefs in PROFILES:
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n{profile_name} Recommendations\n" + "=" * (len(profile_name) + 16))
        for rank, (song, score, reasons) in enumerate(recommendations, start=1):
            print(f"\n{rank}. {song['title']} — Score: {score:.2f}")
            for reason in reasons:
                print(f"     - {reason}")


if __name__ == "__main__":
    main()
