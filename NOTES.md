# Notes

## Tooling
- `tools/race.py` writes vanilla 109 demos and replays them with DSDA's ghost export for exact per-tic coordinates, angles, and player animation frames.
- `tools/nav.py` parses the shareware WAD directly and provides collision-aware grid paths and line-of-sight smoothing. No external demos or route data are used.
- `tools/routes.py` contains the feedback router. It measures displacement, compensates for momentum, and fires when obstructed. `tools/resume1.py` completes E1M1 with direct fixed-input legs.
- The checker is authoritative for every submission. Generated inputs stay within movement, turning, attack, and use limits.

## Submitted runs
- E1M1: PASS, 0:19.77. A five-tic initial delay was selected by replaying 71 original-input timing variants through the official checker. No other run's demo or frame data was used.

## In progress
- Independent local workers are building E1M2, E1M3, and E1M4 from the same WAD-derived tooling. E1M5-E1M8 are next. With more time, replace cautious feedback segments with direct SR50 legs and search only verified timing/movement variants.
