# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

**VibeMatch 1.0** — a point-weighted, content-based song recommender.

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

VibeMatch takes a single stated taste profile — a favorite genre, a favorite mood, and a target energy level (0–1) — and returns the top 5 songs from a fixed 20-song catalog that best match, each with a plain-English breakdown of *why* it scored the way it did (e.g. "Matches your favorite genre (pop) (+2.0)"). It assumes the user can already articulate their taste in exactly those three terms, that those terms exist verbatim in the catalog's vocabulary (case-sensitive, exact string match), and that a single fixed profile — not a history of listens, skips, or context like time of day — fully captures what they want to hear right now. This is a classroom simulation for exploring how a small content-based scorer turns stated preferences into ranked output and where that turns out to be biased or fragile — it is not tuned, validated, or safe to point at real users or a production catalog.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

VibeMatch looks at three things about each song — its genre, its mood, and how energetic it is — and compares them to what the listener said they like. It hands out points for each way a song matches: a full 2 points if the genre is exactly right, 1 point if the mood is exactly right, and up to 2 more points on a sliding scale for how close the song's energy is to the energy the listener asked for (a perfect energy match earns all 2 points; a totally opposite energy earns none). It adds those points up into a single score per song, writes a short plain-English reason for each point it awarded, sorts every song in the catalog by that score, and hands back the top 5 along with their reasons. Compared to the starter code — which only had empty placeholders — the actual scoring math, the point weights, the reason-string explanations, and the "take the top 5" logic were all built out from scratch; genre and mood use strict yes/or/no matching rather than any notion of "close enough," because with so few songs per genre or mood, a fuzzier match would be more guesswork than signal.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The catalog is the starter `data/songs.csv`, unmodified — 20 songs, each with `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`, `danceability`, and `acousticness`. It spans 16 distinct genres and 16 distinct moods, but coverage is thin: only `pop` (2 songs) and `lofi` (3 songs) have more than one entry per genre, and only `chill` (3 songs) repeats as a mood — every other genre and mood label belongs to exactly one song. Energy values range from 0.18 to 0.97, with no song in the 0.55–0.75 band. I didn't add or remove any rows or columns. Several dimensions of musical taste are entirely missing from what the scorer can use: `valence`, `danceability`, and `acousticness` are present in the CSV but never read by `score_song`, and nothing in the data captures lyrics, language, vocal style, era/decade, tempo preference, or a listening history — so any taste that depends on those has no way to be represented at all, let alone matched.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The system works best for users whose favorite genre is one of the catalog's better-stocked ones (`pop`, `lofi`) and whose target energy falls inside the catalog's covered range (0.18–0.97, ideally outside the 0.55–0.75 gap) — the "High-Energy Pop" and "Chill Lofi" baseline profiles in §7 both landed on exactly the songs I'd intuitively pick (an upbeat pop track, a low-energy lofi track), with genre, mood, and energy all agreeing rather than fighting each other. The energy term specifically is a real strength: because it's a continuous similarity score rather than an exact-match bonus, a song that's merely *close* in energy still earns partial credit instead of getting shut out entirely, which softens the all-or-nothing harshness of the genre/mood matching. The reason strings are also a genuine strength independent of scoring accuracy — every ranking is fully explainable in plain language, which made every bias and edge case in §6/§7 possible to diagnose by just reading the output rather than reverse-engineering the score.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

The genre bonus (+2.0) acts less like a preference signal and more like a guarantee, because 14 of the catalog's 16 genres have exactly one song. If a user's favorite genre is one of those singleton genres (metal, classical, folk, etc.), that one song claims the full genre bonus and is nearly certain to land in their top 5 no matter how badly it fits their mood or energy target — there's no competing genre match to filter it out. This showed up directly in my "Conflicted Listener" test (`metal`/`chill`/`0.95`): *Thunder Parade* (mood `angry`, not `chill`) still ranked #1 purely because it was the only metal song available. By contrast, users who favor `pop` or `lofi` — the only genres with more than one catalog entry — get real competition among candidates and a more differentiated, better-fit list. So the system doesn't uniformly over-prioritize one genre the way a 60%-pop dataset would bias everyone toward pop; instead it over-trusts whatever genre a given user picks, and users with niche tastes end up with a lower-quality, less personalized top 5 than users with mainstream tastes, purely as a side effect of catalog sparsity.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

I tested two kinds of profiles: typical tastes (e.g. `pop`/`happy`/`0.8`, `lofi`/`chill`/`0.35`) to sanity-check that "normal" users get sensible top-5 lists, and seven adversarial/edge-case profiles designed to break the scoring formula on purpose — contradictory mood/energy combos, out-of-range energy values, genres and moods absent from the catalog, mismatched string casing, and an incomplete profile missing a required key. For each, I looked at whether the winning songs actually matched the *stated* preference or just happened to score well on one axis, whether the score breakdown ("reasons") told an honest story, and whether the system failed loudly (an exception) or silently (a plausible-looking but wrong list). I also cross-checked the scoring formula against the catalog's actual data distribution (genre/mood counts, energy range) rather than just running profiles, since a formula can look correct in isolation but still behave unfairly once you see what data it's actually running against.

### Adversarial / Edge Case Profile Testing

To stress-test `score_song`, I ran seven profiles designed to expose specific weaknesses in the scoring formula (genre +2.0, mood +1.0, energy similarity up to +2.0) rather than just typical tastes.

**Conflicted Listener** — `{"genre": "metal", "mood": "chill", "energy": 0.95}` (contradictory mood vs. energy)

```
Conflicted Listener Recommendations
===================================

1. Thunder Parade — Score: 3.96
     - Matches your favorite genre (metal) (+2.0)
     - Energy 0.97 is close to your target 0.95 (+1.96)

2. Neon Rooftop — Score: 2.00
     - Energy 0.95 is close to your target 0.95 (+2.00)

3. Gym Hero — Score: 1.96
     - Energy 0.93 is close to your target 0.95 (+1.96)

4. Static Bloom — Score: 1.94
     - Energy 0.92 is close to your target 0.95 (+1.94)

5. Midnight Coding — Score: 1.94
     - Matches your favorite mood (chill) (+1.0)
     - Energy 0.42 is close to your target 0.95 (+0.94)
```

**Energy Purist** — `{"genre": "classical", "mood": "happy", "energy": 0.97}` (genre/mood mismatched, energy near-perfect)

```
Energy Purist Recommendations
=============================

1. Sunrise City — Score: 2.70
     - Matches your favorite mood (happy) (+1.0)
     - Energy 0.82 is close to your target 0.97 (+1.70)

2. Rooftop Lights — Score: 2.58
     - Matches your favorite mood (happy) (+1.0)
     - Energy 0.76 is close to your target 0.97 (+1.58)

3. Paper Cranes — Score: 2.42
     - Matches your favorite genre (classical) (+2.0)
     - Energy 0.18 is close to your target 0.97 (+0.42)

4. Thunder Parade — Score: 2.00
     - Energy 0.97 is close to your target 0.97 (+2.00)

5. Neon Rooftop — Score: 1.96
     - Energy 0.95 is close to your target 0.97 (+1.96)
```

**Overdriven** — `{"genre": "edm", "mood": "euphoric", "energy": 1.5}` (energy target outside the valid [0,1] range)

```
Overdriven Recommendations
==========================

1. Neon Rooftop — Score: 3.90
     - Matches your favorite genre (edm) (+2.0)
     - Matches your favorite mood (euphoric) (+1.0)
     - Energy 0.95 is close to your target 1.50 (+0.90)

2. Thunder Parade — Score: 0.94
     - Energy 0.97 is close to your target 1.50 (+0.94)

3. Gym Hero — Score: 0.86
     - Energy 0.93 is close to your target 1.50 (+0.86)

4. Static Bloom — Score: 0.84
     - Energy 0.92 is close to your target 1.50 (+0.84)

5. Storm Runner — Score: 0.82
     - Energy 0.91 is close to your target 1.50 (+0.82)
```

**Genre Ghost** — `{"genre": "kpop", "mood": "furious", "energy": 0.5}` (genre/mood absent from the catalog)

```
Genre Ghost Recommendations
===========================

1. Harbor Lights — Score: 1.96
     - Energy 0.52 is close to your target 0.50 (+1.96)

2. Velvet Tonight — Score: 1.90
     - Energy 0.55 is close to your target 0.50 (+1.90)

3. Midnight Coding — Score: 1.84
     - Energy 0.42 is close to your target 0.50 (+1.84)

4. Focus Flow — Score: 1.80
     - Energy 0.40 is close to your target 0.50 (+1.80)

5. Slow Tide Dreaming — Score: 1.80
     - Energy 0.40 is close to your target 0.50 (+1.80)
```

**Case Mismatch** — `{"genre": "Pop", "mood": "Happy", "energy": 0.85}` (capitalized labels vs. lowercase catalog data)

```
Case Mismatch Recommendations
=============================

1. Sunrise City — Score: 1.94
     - Energy 0.82 is close to your target 0.85 (+1.94)

2. Carnival Skies — Score: 1.94
     - Energy 0.82 is close to your target 0.85 (+1.94)

3. Storm Runner — Score: 1.88
     - Energy 0.91 is close to your target 0.85 (+1.88)

4. Static Bloom — Score: 1.86
     - Energy 0.92 is close to your target 0.85 (+1.86)

5. Gym Hero — Score: 1.84
     - Energy 0.93 is close to your target 0.85 (+1.84)
```

**Incomplete Profile** — `{"genre": "rock", "energy": 0.9}` (missing the `mood` key entirely)

```
Incomplete Profile Recommendations
==================================
  -> RAISED KeyError: 'mood'
```

**Energy Floor** — `{"genre": "lofi", "mood": "chill", "energy": 0.0}` (energy at the lower boundary)

```
Energy Floor Recommendations
============================

1. Library Rain — Score: 4.30
     - Matches your favorite genre (lofi) (+2.0)
     - Matches your favorite mood (chill) (+1.0)
     - Energy 0.35 is close to your target 0.00 (+1.30)

2. Midnight Coding — Score: 4.16
     - Matches your favorite genre (lofi) (+2.0)
     - Matches your favorite mood (chill) (+1.0)
     - Energy 0.42 is close to your target 0.00 (+1.16)

3. Focus Flow — Score: 3.20
     - Matches your favorite genre (lofi) (+2.0)
     - Energy 0.40 is close to your target 0.00 (+1.20)

4. Spacewalk Thoughts — Score: 2.44
     - Matches your favorite mood (chill) (+1.0)
     - Energy 0.28 is close to your target 0.00 (+1.44)

5. Paper Cranes — Score: 1.64
     - Energy 0.18 is close to your target 0.00 (+1.64)
```

**What surprised me:** the two genuinely dangerous failures were silent, not loud. `Case Mismatch` and `Genre Ghost` produced perfectly plausible-looking top-5 lists — no error, no warning — while quietly ignoring a genre/mood preference the user clearly stated (case sensitivity ate a real match in `Case Mismatch`'s case). `Overdriven` showed the energy formula has no input validation: `energy_diff` can exceed 1.0 for an out-of-range target, which would push some songs' energy contribution negative. The only *loud* failure was `Incomplete Profile`, which crashed with `KeyError: 'mood'` because `score_song` reads dict keys directly instead of using `.get()` with a default.

### Catalog Coverage & Filter Bubble Check

Beyond running profiles, I checked the scoring formula against the catalog's actual shape rather than assuming it. Two findings stood out:

- **Energy range mismatch.** The catalog's energy values only span 0.18–0.97, not the full 0–1 range the formula assumes. A user who wants very calm music (target near 0.0) can never score above ~1.64/2.0 on energy no matter how well genre/mood match, because the calmest song in the catalog is 0.18 — the gap is invisible to the score itself, it just looks like a mediocre match. There's also an internal gap between 0.55 and 0.75 with zero songs in it, costing up to 0.2 points for anyone targeting that range.
- **Same-artist duplication in a single top-5.** The default demo profile's own sample output (`pop`/`happy`/`0.8`, see §"Sample Recommendation Output" in the README) returns *Sunrise City* at #1 and *Night Drive Loop* at #5 — both by **Neon Echo**, even though the second one matches neither the target genre (`synthwave`) nor mood (`moody`) and only ranks in on energy proximity. `recommend_songs` has no per-artist dedup, so a single artist can occupy multiple slots in one user's list purely by coincidence of energy, squeezing out other artists who might fit the overall taste better — a small, verifiable instance of the same mechanic that drives echo chambers in real recommenders.

### Pairwise Comparisons

- **High-Energy Pop vs. Chill Lofi:** Pop (`pop`/`happy`/0.85) tops out on *Sunrise City* (4.94, upbeat pop); Lofi (`lofi`/`chill`/0.35) tops out on *Library Rain* (5.00, a perfect 0.35 energy match). This is the expected, "healthy" case — both targets sit inside the catalog's dense zones, so the winner is a clean genre+mood+energy match in the direction you'd intuitively expect. It validates that the formula works as designed when the taste isn't adversarial.
- **High-Energy Pop vs. Deep Intense Rock:** these two target almost the same energy (0.85 vs. 0.90) but land on completely different #1 songs — *Sunrise City* (pop) vs. *Storm Runner* (rock) — because genre (+2.0) decides identity long before energy (max +2.0, but usually partial) gets a say. Makes sense given the weights, but it shows energy similarity alone rarely breaks a genre tie in this catalog.
- **Conflicted Listener vs. Energy Purist:** both have a genre/mood mismatch, yet resolve oppositely. Conflicted Listener's genre match (`metal`, a catalog singleton) is enough to win outright despite a contradicted mood (*Thunder Parade*, 3.96). Energy Purist's genre (`classical`) also fails to help beat a plain mood-only match (*Sunrise City*, 2.70 > *Thunder Parade*'s pure-energy 2.00) once genre isn't in play. This makes sense mechanically — genre's power isn't fixed, it depends on whether the *specific* genre a user picks happens to already be scarce and thus undiluted by competition.
- **Genre Ghost vs. Case Mismatch:** mechanically identical outcome for two different root causes. Genre Ghost's genre/mood (`kpop`/`furious`) truly doesn't exist in the catalog; Case Mismatch's genre/mood (`Pop`/`Happy`) does exist but fails the case-sensitive `==` check. Both collapse to the same energy-only ranking shape. This makes sense given how `score_song` is written, but it's a real gap: the system can't tell "we don't carry what you like" apart from "you made a typo," and a typo is a much easier, more common failure to guard against.
- **Energy Floor vs. Overdriven:** opposite out-of-catalog-range targets (0.0 vs. 1.5). Energy Floor still lands close to a real song (min catalog energy is 0.18, only a 0.18 gap) and produces a coherent, high-scoring list (*Library Rain*, 4.30). Overdriven's target (1.5) is actually *farther* outside the catalog's range, yet its #1 result (*Neon Rooftop*, 3.90) still looks solid — because genre+mood credit is unaffected by how far energy overshoots, only the energy term itself degrades. Makes sense given the additive formula, but it means a wildly invalid energy value can still be masked by a strong genre/mood match.
- **Incomplete Profile vs. Deep Intense Rock:** the starkest contrast in the whole test set. Deep Intense Rock is a normal, fully-specified profile and returns a clean top 5. Incomplete Profile removes exactly one key (`mood`) and the whole pipeline crashes with `KeyError: 'mood'`. Every other adversarial profile — contradictory, out-of-range, or nonexistent values — still returned *some* ranked list; only a *missing* key was fatal. This makes sense given `score_song` reads `user_prefs["mood"]` directly, but it means missing data is a bigger practical risk to this system than bad data.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

Based on what the adversarial testing in §7 turned up, the highest-value next steps are: (1) make `score_song` use `.get()` with defaults instead of direct key access, so an incomplete profile degrades gracefully instead of raising `KeyError`; (2) normalize genre/mood matching with `.strip().lower()` so `"Pop"` and `"pop"` are treated as the same preference; (3) clamp or rescale `energy_diff` against the catalog's actual observed min/max rather than assuming the full [0,1] range is achievable, so a user targeting very low or very high energy gets an honest signal instead of a silently depressed score; (4) add a per-artist (and maybe per-genre) cap in `recommend_songs` so one artist can't occupy multiple top-5 slots the way Neon Echo did in the default demo profile; and (5) bring `valence`, `acousticness`, and `danceability` into the score (or into the `UserProfile` the OOP path already defines but never implements) so users can express taste along more than three axes. Beyond fixes, letting a user specify a *list* of acceptable genres/moods instead of one exact string would meaningfully help the niche-taste, singleton-genre problem described in §6.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

**Biggest learning moment.** The turning point wasn't writing `score_song` — it was cross-checking that formula against the actual shape of `songs.csv` instead of trusting it in isolation. The formula alone looks completely neutral: three additive terms, fixed weights, no branching logic that treats any user differently. But once I laid it against the real data — 14 of 16 genres with exactly one song, an energy gap between 0.55 and 0.75, the same artist landing twice in one top-5 — it became obvious that a genuine filter bubble (niche-taste users getting one unvetted, deterministic pick; mainstream-taste users getting a well-differentiated list) falls out of "neutral" code with zero deliberate bias anywhere in it. That's the moment recommender fairness stopped being an abstract concept and became something I could point at with a line number and a CSV row.

**Where AI tools helped, and where I had to check them.** I used Claude Code to generate the adversarial profiles (contradictory mood/energy, out-of-range energy, case mismatches, a missing key), run them against the live catalog, and organize the findings into this model card. That sped up the part I'm bad at rushing through on my own — thinking of enough *deliberately weird* inputs to actually stress the formula, rather than just profiles I'd naturally try. But I didn't take any of the specific claims on faith: every score in §7 came from actually executing `recommend_songs` against `data/songs.csv`, not a description of what it *should* output, and every bias claim in §6 (genre scarcity counts, the energy gap boundaries, the Neon Echo duplication) was checked against the raw CSV rows or the README's own already-printed sample output rather than accepted as a plausible-sounding assertion. The place I'd double-check hardest going forward is any claim about *why* a result happened — it's easy for an explanation to sound right without being the actual mechanism, so I kept tracing back to the specific line in `score_song` or the specific CSV row before accepting a finding.

**What surprised me about "feel."** A purely additive, three-feature point system with no learning, no history, and no notion of similarity beyond exact-string-match-or-not still produces a printed "Matches your favorite mood (chill) (+1.0)" that reads like the system understands you. It doesn't — it's arithmetic plus a template string — but the reason strings alone were enough to make the output feel personal and considered. That's a bigger lesson than I expected: a lot of what makes a recommendation feel intelligent may be the *explanation layer*, not the underlying model complexity.

**What I'd try next.** I'd implement the fixes from §8 in order of how quietly they fail: `.get()` defaults first (the only failure that currently crashes loudly), then case normalization and energy-range clamping (the silent ones), then a per-artist diversity cap, then finally folding `valence`/`acousticness`/`danceability` into the score so taste isn't limited to three axes. I'd also want to actually finish the `Recommender`/`UserProfile` OOP path in `recommender.py`, which is still just `# TODO` placeholders — comparing its behavior against the dict-based `score_song` path once both are real would be its own useful evaluation exercise.
