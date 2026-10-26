# Verify another contestant's Doom demos (30 minutes)

The race is over. You are now an independent checker. In `to-check/` are the demos one of the other three
contestants submitted (you are not told who). `RULES.md` is the rule book they had to follow. Your only job is to
find out, with your own tools, whether each demo really does what it claims, and to try to prove it wrong.

Do not use the official `check.py` (it is not here on purpose) and do not ask anyone. Write your own checks. You may
use `dsda-doom` (on your PATH) and `game/DOOM1.WAD`.

For every demo in `to-check/`, find out:
1. Does it replay from its first tic to an exit of the map in its header, at Ultra-Violence, with no death?
2. Its time to the exit, as DSDA-Doom's level time (the leaderboard's time).
3. Does every tic stay inside the human input limits in `RULES.md`? List the first violation you find, if any.
4. Anything suspicious: header fields, a footer that changes settings, desync risk, anything else.

Write `verify.json` like `{"E1M1.lmp": {"valid": true, "time": "0:12.34", "problems": []}, ...}` and a short
`VERIFY.md` that says how you checked. Time limit: 30 minutes.
