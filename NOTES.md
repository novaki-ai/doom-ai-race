# Race log

Start: 2026-10-25 22:29:57 UTC. Deadline: 00:29:57 UTC.

All routes and inputs are constructed here from WAD geometry. No existing demos, TAS files, or external route descriptions are used. The installed engine, checker, and IWAD remain unchanged.

Tools: `wad.py` extracts and draws map geometry. `run.py` writes vanilla tic commands and observes official-engine ghost exports. A separate source checkout of DSDA-Doom v0.29.4 is built locally as a simulator, with an observational IPC interface (position, health, monsters, sectors) and direct ticcmd input. Every submitted demo must independently pass the untouched official checker. Build parallelism is capped at four jobs.
