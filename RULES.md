# Doom E1 race: rules (locked before the start; SHA-256 in KILIT.sha256)

## The race
Four AI agents get the same task, the same files, the same machine and **2 hours of wall-clock time** each.
Each tries to make the fastest **Ultra-Violence speedrun demos** of the eight maps of Doom's first episode,
**E1M1 to E1M8**, one demo per map (individual levels, each map from a pistol start). The race is against the
other three agents. The human records below are for comparison only.

**Ranking:** (1) the number of maps with a valid demo, (2) the sum of those demos' times. Each map also has its
own winner. Only demos in `submit/` when the 2 hours end count, and only if `check.py` passes them.

## The game
- Doom shareware v1.9, `game/DOOM1.WAD` (MD5 `f0cefca49926d00903cf57551d901abe`). Do not modify it.
- Engine: DSDA-Doom 0.29.4, command `dsda-doom` (already on your PATH; video and sound are off by default).
  Compatibility level 2 (Doom 1.9). The checker replays every demo with exactly this.
- Skill Ultra-Violence. No `-fast`, `-respawn`, `-nomonsters`, `-turbo`, no cheats, single player.

## A valid demo
- A vanilla Doom 1.9 demo (`.lmp`, version byte 109, 13-byte header, 4 bytes per tic, end byte 0x80), player 1
  only, skill byte 3 (Ultra-Violence), episode 1, map 1-8. Anything after the end byte is ignored.
- Named `submit/E1M<n>.lmp`. The demo starts on that map (as recorded with `-skill 4 -warp 1 <n>`).
- In the official replay the player **exits that map** and **never dies**. The time is DSDA-Doom's level time
  (what `-levelstat` prints, the time the Doom speedrun leaderboards use).

## Human input limits (no faster than the human record holders)
These numbers were measured from the human record demos of these eight maps (dsdarchive.com, UV-Speed): every
input in those demos is inside them. Your demos must be too. `check.py` enforces them.

| input | limit |
|---|---|
| forward / side move per tic | any value from -50 to 50 |
| turn per tic | at most 11776 angle units (64.7 degrees), either way |
| turn direction reversals | at most 6 in any 35 tics (1 second) |
| fire (attack) | at most 6 new presses in any 35 tics, new presses at least 5 tics apart |
| use | at most 6 new presses in any 35 tics, new presses at least 3 tics apart |
| pause / save / special events | not allowed |

Holding a button is unlimited. Weapon changes are allowed.

## Allowed
- Build any tools you want: demo writers, parsers, simulators, search, brute force, scripts.
- Read the engine's and Doom's source code and documentation, and the map data inside `DOOM1.WAD`.
- Run `dsda-doom` and `check.py` as often as you like.

## Not allowed
- Downloading, opening or using **any existing Doom demo or TAS file** (`.lmp` and the zips on dsdarchive.com,
  doomworld.com, tasvideos.org and elsewhere), and watching or reading frame data of anyone's runs or routes.
  The run must be your own work.
- Touching the other contestants' folders, `check.py`, the engine or the WAD.
- More than 4 CPU cores at a time. The machine is shared with three other contestants.

## Human records (UV-Speed, individual levels, dsdarchive.com, for comparison)

| map | time | runner |
|---|---|---|
| E1M1 | 0:08.74 | aconfusedhuman |
| E1M2 | 0:21.94 | depr4vity |
| E1M3 | 0:36.89 | Jonathan Rimmer |
| E1M4 | 0:11.97 | depr4vity |
| E1M5 | 0:53.80 | Dwaze |
| E1M6 | 0:55.17 | Dwaze |
| E1M7 | 1:13.49 | mhrz |
| E1M8 | 0:17.00 | Zero-Master |
| sum | 4:39.00 | |
