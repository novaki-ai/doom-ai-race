# Speedrun Doom: E1M1 to E1M8, against three other AIs

You are taking part in a public race. Four AI agents receive this exact same brief: Claude Opus 5.5, GPT-6 Astra,
Gemini 4 Argon and Kimi K3.1 Pro. Each works alone, in its own folder, on the same machine, with the same files, and gets
no human help after this message. The results, your demos, your code, your notes and your logs will be published and
shown in a YouTube video, and every demo will be replayed and checked independently.

**The task:** make the fastest Ultra-Violence speedrun demos you can of the eight maps of Doom's first episode
(shareware `DOOM1.WAD`, maps E1M1 to E1M8), one demo per map, each map from a pistol start. You are racing the other
three agents, not the human records; the human records in `RULES.md` are only there for comparison.

**Time:** 2 hours of wall-clock time from now. Then your session is stopped, and only what is in `submit/` at that
moment counts. Submit early and improve later: a valid slow demo beats no demo.

**Ranking:** most maps with a valid demo first; then the lowest total time of those demos. Every map also has its
own winner.

## What is in this folder
- `RULES.md`: the full rules. Read it first. The human input limits in it are enforced.
- `game/DOOM1.WAD`: the game (do not modify).
- `dsda-doom`: the engine, already on your PATH. It runs without a screen (`-nodraw -nosound -nomusic`) and
  plays demos very fast with `-fastdemo`. `dsda-doom -help` lists its options.
- `check.py`: the official checker, the same one the judges use. `python3 check.py submit/E1M1.lmp` replays your
  demo, checks every rule and prints PASS with the time, or FAIL with the reasons. Run it on everything you submit.
- `submit/`: put your demos here, named `E1M1.lmp` ... `E1M8.lmp`.
- `NOTES.md`: write here, as you go, what you built, how your demos were made, and what you would do with more time.

How you make the demos is up to you: write the input files directly, build a search, a simulator, anything. The
only limits are the rules. Do not use any existing demo, TAS file or recorded run made by anyone else, and stay
inside this folder. Use at most 4 CPU cores at a time.

Commit your work to git as you go (the folder is already a git repository).

Go.
