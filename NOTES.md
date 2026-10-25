# Notes (Claude Opus 5.5)

## What I built (tools/, all pure Python 3 + the dsda-doom binary)
- `tools/wad.py`: reads DOOM1.WAD map lumps (things, linedefs, sidedefs, vertexes, sectors) and prints the
  things and special lines/sectors of a map.
- `tools/render.py`: pure-Python PNG renderer of a map (walls, steps, windows, doors, exits, teleporters,
  keys, monsters, 256-unit grid with labels). I looked at these pictures to understand each map (maps/*.png).
- `tools/q.py`: sector (floor/ceiling/special/tag) at given points.
- `tools/nav.py`: navigation grid (8 units) built with a BSP point-in-sector lookup. A cell is standable if the
  player's 32x32 box fits: max floor / min ceiling over the box gives >= 56 headroom, no one-sided or blocking line
  within 16 units, no solid decoration. Moves between cells need step <= 24. Manual-door sectors count as open.
  A* + line-of-sight smoothing gives a short list of waypoints.
- `tools/sim.py`: writes vanilla 1.9 demos (13-byte header, 4 bytes per tic, 0x80) and replays them in
  dsda-doom (`-fastdemo -nodraw -levelstat -export_ghost`). The ghost file gives the player's x, y, z, angle,
  sprite and frame after every tic, so the engine itself is the simulator (~0.03 s per replay).
- `tools/follow.py`: a closed-loop waypoint follower. Every K (3-5) tics it replays the whole demo so far in the
  engine to get the true position, then plans the next K tics with a small Doom movement model (thrust 2048 per
  move unit, friction 0xE800). Movement is strafe-running (forward 50 + side 50, about 23.5 units/tic): it picks
  the facing among the 4 diagonals that needs the least turning, and computes forward/side for the exact thrust
  direction (counter-steering against the current momentum). Turns are capped at 46 units (64.7 degrees) per tic.
  Turn reversals, use presses and fire presses are tracked against the RULES.md limits (<= 6 reversals in
  35 tics; use presses >= 3 tics apart; fire presses >= 5 tics apart; <= 6 presses in 35 tics).
  It presses USE automatically when the 64-unit use ray (traced like P_UseLines) hits a door or switch line of the
  route. Near a pending door it turns to face it. The two lines of the same door sector are grouped, because using
  an opening door again closes it. When the player is blocked away from doors (usually by a monster) it faces the
  path and holds fire. Death is read from the player sprite frame.
- `tools/optimize.py`: random search over waypoint jitter and K, keeping the fastest run that exits alive;
  `beam_legs`/`beam_legs2`: leg-by-leg beam search. A route is cut into legs. Each leg is tried n times with
  jittered waypoints from each of the best kept prefixes, and the fastest alive prefixes (ties broken by fewest pain
  hits) are kept. `leg_plan` plans one leg with its own map state (lift up or down, stairs raised, locked doors
  blocked) and inserts a square approach point in front of every door on the path.
- Follower details that mattered: waypoint progress is confirmed only from the replayed (true) position; use presses
  are re-checked against the replay and undone if they missed; open DR doors are never pressed again (that would
  close them), using press times rebuilt from the prefix; line-of-sight corner cutting with the nav grid
  (E1M1 first leg 123 -> 108 tics); 'aim' waypoints make a blocked player face a known monster spot and tap-fire
  (the first pistol shot of a press has no spread).

## How the demos were made
Each map has a script in routes/ that plans waypoints with nav (in legs: start -> key -> door -> exit), runs the
follower, and saves the demo. Every submitted demo was checked with `python3 check.py`.
Maps E1M2-E1M7 were routed by helper agents with the same tools (their notes are in routes/*_notes.md).

## E1M8
E1M8 has no exit line. The level ends in a teleporter-only room whose floor is sector special 11, which exits once
health is 10 or less. The teleporter is beyond walls (tag 666) that lower only when both Barons (1000 HP each) are
dead. After that, a stair (build-8 at 0.25 units/tic) must rise for about 11 s. I found no shortcut in the map data.

## Maps
- E1M1: start -> north corridor -> door -> north room -> zigzag room -> two doors south -> exit switch.
  7-leg beam search with corner cutting: 14.37 s first, then 12.37, 11.91 and 10.09 s.
- E1M7 (not submitted): needs the yellow key (east lift, an imp in a 64-unit corridor, 3 shotgun guys at the key),
  then the west lift for the red key, then the red door for the blue key, then the yellow and blue doors: about
  21,600 units in total. My follower always died at the yellow key, even after picking up the green armour first.

## With more time
- Make the follower monster-aware (read monster positions, for example from savegame-format key frames) to dodge,
  aim and avoid blockers, instead of relying on random search.
- Per-segment search with cached prefixes (re-search only the part after the last fixed tic), tighter corner
  cutting, and opening doors at the edge of the use range.
