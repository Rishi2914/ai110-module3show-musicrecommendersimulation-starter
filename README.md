# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify and YouTube usually blend two signals: collaborative filtering, which recommends based on what *other* similar users listened to, and content-based filtering, which compares an item's own attributes to what a *specific* user already likes. This project only has one user's taste profile and a small fixed catalog with no listening history from other users, so it implements a content-based approach: every song is scored independently against the user's stated preferences, with no notion of what other users liked.

### Algorithm Recipe

For each song in the catalog, `score_song(user_prefs, song)` computes a single point total from three additive terms:

1. **Genre match: +2.0 points** if `song["genre"] == user_prefs["genre"]`, otherwise +0.
2. **Mood match: +1.0 point** if `song["mood"] == user_prefs["mood"]`, otherwise +0.
3. **Energy similarity: up to +2.0 points**, scaled linearly by how close the song's energy is to the target: `2.0 * (1 - abs(song["energy"] - user_prefs["energy"]))`. A perfect energy match scores the full 2.0; a maximally distant one (diff of 1.0) scores 0.

These three terms are summed into a total score, and each contributing term also produces a plain-English reason string (e.g. `"Matches your favorite genre (pop) (+2.0)"`). `recommend_songs()` then:

- Scores every song in the catalog this way (the loop),
- Sorts all songs by total score, descending,
- Returns the top `k` as `(song, score, explanation)` tuples, where `explanation` joins that song's reason strings.

Genre and mood use exact-match bonuses (rather than similarity) because the catalog's genre/mood categories are sparse — several genres and moods have only one song in the 20-row dataset, so any fuzzier "closeness" measure between labels would be mostly guesswork.

### Expected Biases

- **Genre dominates ties.** Because a genre match (+2.0) outweighs a mood match (+1.0) and can equal a perfect energy match, a song in the user's favorite genre but a mismatched mood/energy can outrank a song that's a near-perfect mood-and-energy fit but the "wrong" genre. The system might over-prioritize genre, sidelining great songs that match the user's mood and vibe just because the genre label differs.
- **All-or-nothing categorical bonuses.** Genre and mood are scored as exact string matches, not similarity — a mood of `"happy"` gets zero credit toward a target of `"excited"` even though they're conceptually close, and a rare genre with only one catalog entry either wins big or contributes nothing.
- **Ignores acousticness and valence.** The dataset has `valence` and `acousticness` columns that aren't used in scoring at all, so two songs that feel very different on those axes can score identically if their genre, mood, and energy line up — the system can recommend something that "measures right" on the three chosen features but still doesn't match the user's actual taste on dimensions it never looks at.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main` for the default profile (`genre=pop, mood=happy, energy=0.8`):

```
Loaded 20 songs from data/songs.csv

Top Recommendations
===================

1. Sunrise City — Score: 4.96
     - Matches your favorite genre (pop) (+2.0)
     - Matches your favorite mood (happy) (+1.0)
     - Energy 0.82 is close to your target 0.80 (+1.96)

2. Gym Hero — Score: 3.74
     - Matches your favorite genre (pop) (+2.0)
     - Energy 0.93 is close to your target 0.80 (+1.74)

3. Rooftop Lights — Score: 2.92
     - Matches your favorite mood (happy) (+1.0)
     - Energy 0.76 is close to your target 0.80 (+1.92)

4. Carnival Skies — Score: 1.96
     - Energy 0.82 is close to your target 0.80 (+1.96)

5. Night Drive Loop — Score: 1.90
     - Energy 0.75 is close to your target 0.80 (+1.90)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



