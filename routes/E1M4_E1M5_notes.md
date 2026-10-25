# E1M4 and E1M5 notes (agent m45)

## E1M4: PASS, 13.43 s (submit/E1M4.lmp, backup routes/e1m4_best.lmp)
Older passing versions: routes/e1m4_1471.lmp (14.71 s) and routes/e1m4_1469.lmp (14.69 s).

### Route: no keys, one trick jump
- Start, then door 648 west of the start (used at about tic 12; it is open at about tic 40).
- East room, then the long north room, then the north corridor, down to (-4,1196).
- Loop south-west to (-524,716), then north to (-628,1052) and (-292,1332). This loop is forced by the walls.
- Room 49 (the maze room) via its south entrance, then up the west walkway. Crossing W1 line 807 lowers the maze block (sector 50) to 144.
- Press USE on DR door 469 at about tic 320-350 while passing it heading north.
- Loop back east along y=1888 over the lowered maze to x = -260..-330. Stop there, facing 135 degrees.
- Scripted run-up: one "phase" tic of (f0,-f0), then (50,-50) every tic. This strafe-runs due west through the door (now open), up the stairs (sectors 59..66, top at floor 192) and jumps the 192-unit gap (sector 52, floor 128) to ledge sector 38 (floor 192).
- Door 548 (x=-1456), then the exit switch 554 at x=-1600.

### Jump physics
- In the air there is no thrust and no friction. Gravity gives drops of 0,2,3,4,5,6,7... per tic.
- A step-up needs z >= 168 when the box first touches line 521 (x=-1216, so center x < -1200).
- The box leaves sector 66 when center x < -1040. That leaves 6 airborne XY moves after the leaving tic.
- Condition: x_after_leaving_tic - 6v < -1200. This needs v >= ~22.9 (97% of SR50 max 23.57) plus a good sub-tic phase.
- From rest at the door you reach only ~93%, so a run-up of about 700+ units is needed, starting east of the door inside room 49.
- The phase is searched over the first-tic thrust f0 (5..50) and 0..2 idle tics. Each candidate is one engine replay, so this is cheap.
- Speeding up the alternative route (blue key + yellow key + switch 592 raising sector 52) is much longer.

### How the demo was made (work_m45, copies in routes/m45_scripts)
- Stage A: follow() on A* waypoints to the door use (m4e.py / m4opt2.py stageA2, with random waypoint jitter and K jitter).
- Stage B: follow() to (TX,1888) with face=135. Exclude door lines 468/469 here: a re-press closes the DR door.
- Run-up phase search (runup in m4opt.py).
- follow() to the exit (finish).
- m4opt2.py runs the whole pipeline in a random search. The best was seed 41 trial 31: A=316 tics, B=371, TX=-330, total 471 tics.

### With more time
- The room-49 loop costs about 40 tics. Ideas: a shorter run-up with an exact phase, or using the door earlier.
- The stage-A monster stalls cost about 40 tics: the zombie/demon near (856,1650) and the zombie (64,1536). Try routing around them or a smarter detour.
- Human record is 11.97 s.

## E1M5: NOT finished (no submit)
Key logic (from WAD analysis):
- The exit (switch 409, room 113) is behind room 106. Room 106 needs the blue key (blue doors 322/323 or 767).
- The blue key (192,1040, sector 130) is reachable only after S1 switch line 189 opens sector 82 (tag 2). Route from there: 82, 83..89, 123, 125..129, 124, 120, 118, 119, door 122 (line 145), 100, 111, 132, 131, 130.
- Switch 189 is inside box sector 21 in the west nukage pit (sector 19). Stand in the box at (-1150,832) facing east.
- The west is reachable only through the yellow door 157 (from sector 14). Door 52 (line 776) opens only from its west side.
- West route: yellow door, sector 13, lift 12 (WR line 161 lowers it), 18, stairs 47..42, 41, 38, 37 (WR line 519 lowers lift 48), ring 9 (W1 line 192 opens monster closets 32/40), pit 19, box 21.
- Way back: lift 48 (about a 130-tic wait), D1 doors 808 and 820, 51, door 776, 139, east to 82.
- Yellow key (688,800, sector 92): W1 line 271 (x 832..944, y=248, east end of the corridor x424..944, y128..224) raises nukage sector 91 at 0.5 units/tic. It must reach >= 32 (about 112 tics) before the player can step into 92.
  - Path: corridor back west, stairs (204,250), (185,370), (241,462) into sector 79, drop into 91 at x≈448, ride it to (1065,770), then 92 and the key.
- Blockers: spectres at (-64,256) by door 71 and ambush (896,176) in the corridor, plus a sarge and a spectre in box 102 just past line 271. A monster also waits in sector 13 behind the yellow door.
Progress:
- start → green armor (-416,-160) → shotgun (288,352, door 81) is reliable: routes/m45_e1m5_L0_armor_shotgun.lmp.
- Then crossing 271 succeeds about 1 time in 5.
- Back west to the yellow key worked with short-leg beam search (m5beam2.py stage S2): routes/m45_e1m5_yellowkey_prefix.lmp, yellow key at tic 717.
- The yellow door was reached at about tic 937, but the player then had ~8 pain hits and died behind the door.
With more time: pick up health (medikit (-800,1392), stims (-992,1296), (-1280,1216), blue armor (-1248,1104)), use the shotgun with aimed fire at the spectres, and continue stages S4-S7 in m5beam.py.
