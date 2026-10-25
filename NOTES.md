# Race log

Start: 2026-10-25 22:29:57 UTC. Deadline: 00:29:57 UTC.

All routes and inputs are constructed here from WAD geometry. No existing demos, TAS files, or external route descriptions are used. The installed engine, checker, and IWAD remain unchanged.

Tools: `wad.py` extracts and draws map geometry. `run.py` writes vanilla tic commands and observes official-engine ghost exports. A separate source checkout of DSDA-Doom v0.29.4 is built locally as a simulator, with an observational IPC interface (position, health, monsters, sectors) and direct ticcmd input. Every submitted demo must independently pass the untouched official checker. Build parallelism is capped at four jobs.

23:03 UTC: E1M1 18.03, E1M2 1:07.74, E1M4 31.69 and E1M8 3:58.66 have passed the official checker. The E1M8 baseline is deliberately conservative and contains long combat loops; improving it is a later priority. Observation now includes monster visibility and line-of-fire probes; these do not consume RNG or change world simulation. Every actual input remains a normal legal vanilla tic command. Searches vary route waypoints, short delays, targeting and obstacle avoidance. E1M3/E1M5 are in progress. All work remains single-agent.
