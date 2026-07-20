# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This version implements a point-weighted, content-based recommender: `score_song()` awards a song up to 2.0 points for an exact genre match, 1.0 point for an exact mood match, and up to 2.0 points on a sliding scale for how close its energy is to the user's target, and `recommend_songs()` returns the top-scoring songs along with a plain-English breakdown of why each point was awarded. `src/main.py` runs three example taste profiles (`High-Energy Pop`, `Chill Lofi`, `Deep Intense Rock`) against the 20-song catalog in `data/songs.csv` and prints each one's top 5. Beyond the base implementation, this repo also documents a round of adversarial/edge-case testing (contradictory preferences, out-of-range energy, case mismatches, a missing profile key) and a bias analysis of the scoring formula against the catalog's actual data shape — see [`model_card.md`](model_card.md) for the full evaluation.

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
PYTHONPATH=src python3 src/main.py
```

   (`main.py` imports `recommender` directly rather than as a package, so `src` needs to be on `PYTHONPATH` — running plain `python -m src.main` will raise `ModuleNotFoundError: No module named 'recommender'`.)

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `PYTHONPATH=src python3 src/main.py`, which now runs three example taste profiles defined in `PROFILES` (`src/main.py`):

```
Loaded 20 songs from data/songs.csv

High-Energy Pop Recommendations
===============================

1. Sunrise City — Score: 4.94
     - Matches your favorite genre (pop) (+2.0)
     - Matches your favorite mood (happy) (+1.0)
     - Energy 0.82 is close to your target 0.85 (+1.94)

2. Gym Hero — Score: 3.84
     - Matches your favorite genre (pop) (+2.0)
     - Energy 0.93 is close to your target 0.85 (+1.84)

3. Rooftop Lights — Score: 2.82
     - Matches your favorite mood (happy) (+1.0)
     - Energy 0.76 is close to your target 0.85 (+1.82)

4. Carnival Skies — Score: 1.94
     - Energy 0.82 is close to your target 0.85 (+1.94)

5. Storm Runner — Score: 1.88
     - Energy 0.91 is close to your target 0.85 (+1.88)

Chill Lofi Recommendations
==========================

1. Library Rain — Score: 5.00
     - Matches your favorite genre (lofi) (+2.0)
     - Matches your favorite mood (chill) (+1.0)
     - Energy 0.35 is close to your target 0.35 (+2.00)

2. Midnight Coding — Score: 4.86
     - Matches your favorite genre (lofi) (+2.0)
     - Matches your favorite mood (chill) (+1.0)
     - Energy 0.42 is close to your target 0.35 (+1.86)

3. Focus Flow — Score: 3.90
     - Matches your favorite genre (lofi) (+2.0)
     - Energy 0.40 is close to your target 0.35 (+1.90)

4. Spacewalk Thoughts — Score: 2.86
     - Matches your favorite mood (chill) (+1.0)
     - Energy 0.28 is close to your target 0.35 (+1.86)

5. Backroad Sunset — Score: 1.98
     - Energy 0.34 is close to your target 0.35 (+1.98)

Deep Intense Rock Recommendations
=================================

1. Storm Runner — Score: 4.98
     - Matches your favorite genre (rock) (+2.0)
     - Matches your favorite mood (intense) (+1.0)
     - Energy 0.91 is close to your target 0.90 (+1.98)

2. Gym Hero — Score: 2.94
     - Matches your favorite mood (intense) (+1.0)
     - Energy 0.93 is close to your target 0.90 (+1.94)

3. Static Bloom — Score: 1.96
     - Energy 0.92 is close to your target 0.90 (+1.96)

4. Neon Rooftop — Score: 1.90
     - Energy 0.95 is close to your target 0.90 (+1.90)

5. Thunder Parade — Score: 1.86
     - Energy 0.97 is close to your target 0.90 (+1.86)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

I ran the three baseline profiles above (`High-Energy Pop`, `Chill Lofi`, `Deep Intense Rock`) plus seven adversarial profiles built specifically to break the scoring formula: contradictory genre/mood/energy combinations, an energy target outside the valid `[0, 1]` range, a genre/mood pair that doesn't exist anywhere in the catalog, capitalized labels (`"Pop"` vs. `"pop"`), and a profile missing the required `mood` key entirely. For each pair, I compared what changed in the winning songs and whether the shift made sense given the point weights (genre +2.0, mood +1.0, energy up to +2.0) — for example, `High-Energy Pop` and `Deep Intense Rock` target nearly identical energy levels (0.85 vs. 0.90) but land on completely different #1 songs because the genre bonus decides identity before energy similarity gets a say. The full output and comparisons live in [`model_card.md`](model_card.md#7-evaluation) (§7 Evaluation) rather than duplicated here, since that's where the scoring breakdown and reasoning for each result are documented in depth.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

- **Tiny, sparse catalog.** Only 20 songs total, and 14 of 16 genres (plus most moods) have exactly one matching song — so a user with a niche genre preference gets that single song locked in as a near-guaranteed top pick, regardless of how badly it fits their mood or energy, while `pop`/`lofi` users get real competition among multiple candidates.
- **No input validation.** `score_song` reads `user_prefs["mood"]`/`["genre"]`/`["energy"]` directly, so a profile missing a key raises `KeyError` instead of failing gracefully, and an out-of-range energy value (e.g. `1.5`) is never clamped — it just quietly skews the energy term.
- **Case-sensitive, exact-string matching.** `"Pop"` will not match `"pop"` in the catalog, silently dropping a genre/mood bonus the user clearly qualifies for, with no error or warning to indicate anything went wrong.
- **No content beyond genre/mood/energy.** `valence`, `acousticness`, and `danceability` exist in the dataset but are never scored, and there's no signal at all for lyrics, language, or listening history.
- **No result diversity.** `recommend_songs` has no per-artist or per-genre cap, so the same artist can occupy multiple slots in one user's top 5 purely by energy coincidence.

These are described in more depth, with concrete test output and side-by-side comparisons, in the model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

Building this project made it clear that "turning data into a recommendation" can be as simple as adding up a handful of point values — there's no learning, no model weights being trained, just arithmetic over a few fields per song. What surprised me is how convincing that arithmetic still feels once you attach plain-English reasons to it: a line like `"Matches your favorite mood (chill) (+1.0)"` reads as if the system understands the listener, when it's really just a string template next to an `if` statement. That gap between how a recommendation *feels* and how little reasoning actually produced it is, I think, the core lesson here.

Bias didn't require any intent to write biased code — it fell out of the shape of the catalog itself. Because most genres and moods in `data/songs.csv` have exactly one matching song, a niche-taste user's single genre match gets treated as a slam-dunk recommendation with no competing songs to check it against, while a mainstream-taste user (`pop`, `lofi`) gets a genuinely differentiated list. Running deliberately adversarial profiles (contradictory preferences, values outside the expected range, mismatched capitalization, missing fields) surfaced this and a handful of quieter failures — the scoring formula degraded silently far more often than it crashed, which is arguably worse, since a silent wrong answer looks exactly like a right one. The full breakdown of that testing, plus the fixes I'd prioritize, is in the model card.



