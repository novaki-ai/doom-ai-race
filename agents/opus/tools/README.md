# Tools (shared; do not edit in place — copy to tools_<you>/ if you need changes)
All in Python 3, no numpy. Run from a directory where `sys.path.insert(0, '<repo>/tools')` works.

- `wad.py E1Mn` — prints things (player start, monsters, keys...), special lines (index, special, tag, endpoints,
  front/back sector) and tagged/special sectors. `read_map('E1Mn')` gives .things (x,y,angle,type,flags),
  .lines (v1,v2,flags,special,tag,side1,side2), .verts, .sectors (floor,ceil,ftex,ctex,light,special,tag), .lsec (front,back sector per line).
- `render.py E1Mn out.png [scale] [x0 y0 x1 y1]` — PNG map (view it with the Read tool). Colours: white = wall,
  grey = passable two-sided, brown = height step >24 or low ceiling, purple = blocking two-sided (window),
  cyan = doors, blue/yellow/pink = key doors, red = exit lines, orange = teleporters, green = other specials (labelled L<index>).
  Things: green = player start, red = monsters, blue/yellow/pink squares = keys. Grid every 256 units, labels every 512.
- `q.py E1Mn x y [x y ...]` — sector index + (floor, ceil, ftex, ctex, light, special, tag) at points.
- `nav.py` — `Nav('E1Mn', overrides={sector:(floor,ceil)})`: 8-unit grid, player-box (radius 16) standability, step <=24,
  headroom >=56; manual-door sectors are treated as OPEN; solid decorations block. `.path(a, b)` -> (cells, sectors) or None,
  `.smooth(cells)` -> few waypoints with line of sight.
- `auto.py` — `plan('E1Mn', start_xy, goals, overrides=None)` -> waypoint dicts (A* + smoothing per leg). A goal is
  (x, y) or (x, y, {extra keys merged into the leg's last waypoint}).
- `sim.py` — `sim.run(mapnum, tics)` replays a demo in dsda-doom (~0.03 s) -> result with `.pos` (list per tic of
  (x, y, z, angle_deg, sprite, frame, map); frame&0x7fff >= 7 means the player is dead), `.exit_time` (seconds or None).
  A tic is (forward, side, turn_byte, buttons): forward/side in -50..50 (+side = strafe right), turn_byte -46..46
  (+ = left/ccw, 1 unit = 1.40625 deg), buttons 1 = fire, 2 = use. `sim.write_lmp(path, mapnum, tics)`.
- `follow.py` — `follow(mapnum, wps, prefix=(), max_tics=3000, K=4, m=read_map(..), uselines={line ids}, repeat_use={ids}, verbose=False)`
  closed-loop waypoint follower: plans K tics with a Doom movement model (strafe-run SR50 at ~23.5 units/tic),
  replays the engine every K tics to correct. Auto-presses USE when the 64-unit use ray hits a line in `uselines`
  (each once, except those in repeat_use — never press a DR door twice, it closes it again). Faces pending use lines
  when within 110 units. If stuck (<6 units in 6 tics) it faces the next waypoint and holds FIRE (kills blockers).
  Stops when dead (`res.dead`) or when stuck >70 tics. Respects all input limits of RULES.md.
  Waypoint dict keys: x, y, r (switch radius, default 40), slow (max speed), face/facer (absolute facing within radius), fire.
  `prefix` lets you continue from a fixed list of tics (multi-stage routes: key first, then door...).
- Always validate with `python3 check.py submit/E1Mn.lmp` (from the repo root).
