# E1M6 / E1M7 notes (agent m67)

E1M7 was handed over to the coordinator at about 02:00, so this agent only worked on E1M6.
Final status at 03:06: **no passing E1M6 demo** (nothing written to submit/E1M6.lmp by this agent).
The best runs reach switch L822 at tic ~2210-2300 with 16-17 pain hits, then die in leg Z (switch -> door 37 -> west wing -> exit).
Best prefixes: work/m67/m6_Hb1_b*.json (tic ~1810, 10 hits, back at the blue door) and work/m67/m6_Hb2_b*.json (at the switch).
Resume command, from work/m67: SEED=<n> FAL=Hb2east,Z python3 beam6.py Hb1_b0+Hb1_b1+Hb1_b2 Hb2,Z 10 4
(on success it runs check.py and copies a pass into submit/E1M6.lmp only if it is faster).

## E1M6 route (key order is forced by the map)
1. Start (32,-1376) -> corridor -> nukage walkway -> door 187 -> diamond room 186 -> cross L206 into the red-key area 185.
   * **Trap:** L206 (W1 type 16, tag 9) closes door 187 for 30 s. If a monster stands in door 187 while it closes, the door
     reverses and stays open for good. Search script `work/m67/door6.py`: waiting 25 tics inside 186 before crossing gives that
     result (prefix `work/m67/m6_A2.json`, tic 166). Waiting out the trap instead is deadly with a pistol.
2. Red key (1680,-1344). **Careful pickup:** the key is boxed by four W1 lines (1319-1322, tag 10) that open five monster closets.
   Coming in from the NE corner with the centre at x>1704, y>-1320 picks the key up without crossing those lines
   (`work/m67/key6.py`, prefix `m6_Bsafe.json`).
3. Back through door 187 -> red door 174 (line 951, from the north) -> blue key (-1536,-1728).
4. Blue armour (-1152,-1712) and medikit (-1200,-1760) -> south route through room 157 (invisibility sphere at (-256,-1536))
   -> one-way door 158 (line 121) -> start room -> door 127 (line 935) -> east passage. Crossing L460 here lowers platform 151.
5. Blue door 218 (line 975) -> far-east zone -> medikit (2624,-2176) -> switch L438 (opens door 242).
6. Door 242 -> sector 193 -> diagonal stairs -> yellow key (1088,-608). Room 152, the short way, is packed with ambush
   monsters (3 demons, a spectre, 2 sergeants) and is physically blocked.
7. Back through 242 -> blue door 218 (line 976, from the east) -> east passage -> yellow door 142 (line 890) -> north room ->
   switch L822 (-64,2368, opens door 37).
8. Switch -> door 37 (-648,1280) -> west wing -> green armour (-960,1280), medikit (-1536,1280) -> switch L599 (opens 28) ->
   door 30 (line 614) -> exit switch L627.
The run reaches step 8 at tic ~2200-2300 (about 64 s) with too little health and dies. Two imps (ambush) block door 37.

## How the demos are built
* `tools_m67/` = copy of the shared tools (the coordinator's latest `follow.py`) plus `legs.py`.
* `work/m67/m6.py` holds the leg table (`LEGS`); `work/m67/beam6.py` runs a leg-by-leg beam search. It keeps the
  fewest-pain-hits alive prefixes, applies fire_ahead per leg (env `FAL`), seeds via `SEED`, and on exit check.py's
  the candidates and copies a pass to submit/ only if it is faster.
* Health can't be read from the ghost export. Pain-state entries (frame 6) serve as a damage proxy.

## What I would do with more time
* Pick up the chaingun (1280,-1536) in the red-key room and/or the shotgun (-544,-1376) near the start, and aim at known
  monster spawn points (the `aim` waypoint key) to clear sergeants and imps instead of tanking them.
* Lure the ambush monsters out of room 152 (after L460 lowers 151) to open the short route to the yellow key. This saves the whole east
  loop (~6600 units, ~10 s, and most of the damage).
* Search the door-trick start for fewer early hits. The two sergeants in room 186 cause most of the pre-armour damage.
