# Race log

Start: 2026-10-25 22:29:57 UTC. Deadline: 00:29:57 UTC.

All routes and inputs are constructed here from WAD geometry. No existing demos, TAS files, or external route descriptions are used. The installed engine, checker, and IWAD remain unchanged.

Tools: `wad.py` extracts and draws map geometry. `run.py` writes vanilla tic commands and observes official-engine ghost exports. A separate source checkout of DSDA-Doom v0.29.4 is built locally as a simulator, with an observational IPC interface (position, health, monsters, sectors) and direct ticcmd input. Every submitted demo must independently pass the untouched official checker. Build parallelism is capped at four jobs.

23:03 UTC: E1M1 18.03, E1M2 1:07.74, E1M4 31.69 and E1M8 3:58.66 have passed the official checker. The E1M8 baseline is deliberately conservative and contains long combat loops; improving it is a later priority. Observation now includes monster visibility and line-of-fire probes; these do not consume RNG or change world simulation. Every actual input remains a normal legal vanilla tic command. Searches vary route waypoints, short delays, targeting and obstacle avoidance. E1M3/E1M5 are in progress. All work remains single-agent.

23:29 UTC progress: E1M5 (2:06.49) and E1M6 (2:55.09) now also pass. Six submitted maps total. E1M3 has the blue key and has returned through the blue door; E1M7 now has all three keys. Major navigation pitfalls found: barrels and decorations occupy space omitted from the map-wall raster; sector heights must include player radius near raised edges; newly triggered doors need opening time. Searches and the local simulator are now pinned to CPUs 4–7 so aggregate execution is capped at four cores. Added explicit aimed fire for individual blockers. The blue E1M7 key is collected by touching the edge of its raised platform.

23:36 UTC: All eight maps now have independently verified demos. E1M3 1:32.97 and E1M7 2:48.40 complete the baseline set. Circling the lower arena during the E1M3 stair rise worked; stopping on the stairs exposed the player to too much fire. E1M7 required routing around a solid floor lamp in the final hall. Optimization now begins while retaining each passing baseline.

23:42 UTC improvements: E1M1 13.63 and E1M4 26.29 pass. E1M8 improved to a much shorter fight by collecting the upper ammunition after clearing spectres, then circling around the baron platforms via the low southern steps. Static floor elevations explain many failed attempts: moving directly across the side of a 40/56-unit platform traps the player despite an apparently open overhead map.

23:50 UTC: E1M1 improved further to 11.54; E1M2 58.31; E1M7 2:41.71. E1M6 now takes a shorter, healthier return from the yellow key. At the western alcove, explicitly shooting the blocking demon before entering was essential; trying to walk past it caused repeated deaths. All replacement submissions are checked before copying over the prior valid demo.
