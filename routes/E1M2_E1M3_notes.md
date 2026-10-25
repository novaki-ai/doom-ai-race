# E1M2 / E1M3 notes (agent m23)

## E1M2: submit/E1M2.lmp, PASS 0:30.80 (check.py)
Backups: routes/e1m2_best.lmp (= submit), routes/e1m2_v*_*.lmp (older passing runs: 40.37, 39.34, 33.43, 32.40, 31.43, 30.80).

Route (red key needed; exit switch 873 sits in an alcove behind lift 49):
1. Start -> east door 78 (line 325) -> south stairs -> red key corridor (sector 62) -> red key (1136,352).
2. Back east past the 2 zombies -> south stairs -> door 78 (closed by then; re-pressed via line 291 when stuck) -> central room -> red door (line 527, waypoints aligned on the door axis y=384).
3. West corridor -> west stairs -> 3 medikits at (-1504,1456..1520) -> walk-over lift 137 (line 715) -> ride down into room 120.
4. East side of room 120 (threading between the monster formation) -> switch 777 (opens doors 124/129) -> door 129 (NE) -> corridor 123 -> medikit (-1536,2272) -> corridor east.
5. Exit door 55 (line 854), then CAMP: hold at (-722,2312) facing east for 115 tics shooting the room monsters through the door.
6. South side of the room to lift 49 (walk-over lines 870/871 lower it), hold at (-352,2336) on the lift facing east, holding fire for 30 tics. That kills the imp standing in the exit alcove at (-288,2336). The imp blocks the switch, and it can't be shot until the lift is down.
7. Walk into the alcove and press exit line 873.

How it was made: tools_m23/ (my copy of tools/) + routes/e1m2_s2.py (segment search) and routes/e1m2_search.py (older version).
- seg.py: greedy segment-by-segment search. Each segment is a goal list (or a list of alternative goal lists); plan() with A*; follow().
  Variants: goal jitter + waypoint jitter + K in {3,4,5}. Score = tics + 12 * pain-state entries (hit proxy). Best alive result kept; its prefix saved to a pickle.
- follow.py extensions: 'must' (waypoint must be reached by the replayed position), 'hold' (stand at a waypoint for N tics with a fixed facing),
  'firehold' (hold fire = 1 new press), done_stop/need (segment ends only after given use lines were pressed), sweep fire when stuck,
  coordinator's door-sector use fix, monster soft-cost + wall clearance in nav.py, sim retry.
- Env knobs in e1m2_s2.py: CAMP (exit-room camp tics), HOLD (lift hold tics), SEED, T0..T5 (tries per segment), PFX/LOADPFX (pickle chains).

Time sinks left (from the trace of the 30.8 run): about 100 tics fighting the 2 zombies in the key corridor on the way back,
about 30 tics waiting at each door (78, red door, 55), the 115-tic camp, and the 30-tic lift hold.
With more time: kill the key-corridor zombies on entry with accurate taps, press doors from max range, and do a beam search instead of
greedy segments (greedy is myopic: HP at the exit room decides survival). Shotgun/chaingun are not reachable cheaply.

## E1M3: no demo from me (the coordinator took E1M3 over)
Analysis I handed over:
- Normal exit (line 982) needs the blue key (-160,-864) for blue door 61, then walk-over stair line 967 (x=-256).
  The stairs build at 0.25 u/tic: step 13 needs about 256 tics to reach 112 so you can step onto sector 14 (136). That forced wait is the danger zone.
- Secret exit (line 785, room 35): check.py accepts it. Path: switch 535 (-1936,-2104) opens door 121 -> walk-over line 116 lowers lift 165 ->
  line 231 opens door 167 -> 166 -> 154 -> nukage channel 153/157/156 (48-wide gaps, nav can't plan them, use direct waypoints) ->
  159 -> switch 360 raises pit 66 to 64 -> back to the pit -> line 988 opens corridor 51 -> line 54 opens door 53 -> room 32 ->
  line 88 opens doors 33/34 -> ring 31 -> corridor 44 -> door 45 (line 87) -> room 35 -> switch 785. Roughly 10k units.
  My attempt (routes/e1m3_secret.py) reached switch 535 with 6 hits, then died every time near door 121. Not finished.
- tools_m23/openall.py: nav overrides that open every tagged door and lower every tagged lift (for planning).
