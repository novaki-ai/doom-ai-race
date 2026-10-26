# Doom AI race: four AIs, eight maps, two hours

Four AI agents got the same one-message brief: make the fastest Ultra-Violence speedrun demos of the eight maps of
Doom's first episode (shareware `DOOM1.WAD`, E1M1 to E1M8) in two hours, with no human help after that message, and
never faster than a human can press. This repository holds everything needed to replay and check the result yourself.

Video: https://www.youtube.com/@Novaki_ai

| Agent | Tool | Model | Effort |
|---|---|---|---|
| `opus` | Claude Code | Claude Opus 5.5 | max |
| `astra` | Codex | GPT-6 Astra | ultra |
| `argon` | Antigravity | Gemini 4 Argon | high |
| `kimi` | Kimi Code | Kimi K3.1 Pro | max |

## Result (official checker, `results/official.json`)

| Map | GPT-6 Astra | Claude Opus 5.5 | Kimi K3.1 Pro | Human record |
|---|---|---|---|---|
| E1M1 | 0:11.29 | **0:10.06** | 0:19.77 | 0:08.74 |
| E1M2 | 0:48.06 | **0:30.80** | invalid (no exit) | 0:21.94 |
| E1M3 | **1:23.09** | – | – | 0:36.89 |
| E1M4 | 0:16.63 | **0:13.43** | – | 0:11.97 |
| E1M5 | **1:42.37** | – | invalid (no exit) | 0:53.80 |
| E1M6 | **2:35.89** | – | – | 0:55.17 |
| E1M7 | **2:22.40** | – | – | 1:13.49 |
| E1M8 | **1:42.37** | – | invalid (no exit) | 0:17.00 |
| **Total** | **8/8 · 11:02.10** | 3/8 · 0:54.29 | 1/8 · 0:19.77 | 4:39.00 |

Ranking: most maps with a valid demo, then the lowest total time. Gemini 4 Argon submitted no demo (see below).
No agent beat a human record; the race was between the agents.

## Replay a demo

You need DSDA-Doom 0.29.4 (https://github.com/kraflab/dsda-doom) and the shareware `DOOM1.WAD` v1.9
(MD5 `f0cefca49926d00903cf57551d901abe`; freely distributable, not included here).

```bash
dsda-doom -iwad DOOM1.WAD -complevel 2 -playdemo results/demos/astra/E1M8.lmp
```

To check a demo the way the race did (header, human input limits, then a replay that must reach the exit alive):

```bash
RACE_DSDA=$(command -v dsda-doom) RACE_IWAD=/path/to/DOOM1.WAD python3 rules/check.py results/demos/opus/E1M1.lmp
```

## What is here

- `rules/`
  - `BRIEF.md`: the exact message every agent got, word for word.
  - `RULES.md`: the rules and the human input limits.
  - `check.py` and `lmp.py`: the official checker the agents also had.
  - `insan_olc.py` and `olcum.json`: how the human limits were measured from the eight record demos (dsdarchive.com; the
    demos themselves are not included, download them there).
  - `KILIT.sha256`: hashes of the rules, checker, measurements, WAD and engine, taken before the start.
- `results/official.json` and `results/demos/<agent>/`: the demos in each agent's `submit/` when its two hours ended,
  and the checker's verdict on each. `category` is DSDA-Doom's own `-analysis` label (Pacifist means nothing was shot).
- `verification/`: after the race, each agent got another agent's demos without being told whose, 30 minutes and no
  `check.py` (`VERIFY-brief.md`). Opus checked Astra, Astra checked Kimi, Kimi checked Opus. All 15 verdicts matched the
  official checker.
- `agents/<agent>/`: each agent's working folder with its own git history: its tools, notes (`NOTES.md`) and every
  commit it made during the race.
- `gemini/`: the three Antigravity sessions of Gemini 4 Argon, unedited.

## Gemini 4 Argon

Gemini never handed in a demo. Three times it decided to disassemble the engine binary (`objdump -d dsda-doom`) to find
the player's position in memory, and three times, after about seven minutes, Antigravity answered "This request was
blocked by Gemini's filters. They can occasionally trigger by mistake on safe coding, security, or biology-related
queries." and the session ended:

1. the first session;
2. the same conversation resumed with the single message "Continue.";
3. a fresh session with the same brief and no hints.

Telling it to avoid disassembly would have been human help, so it was not told. About 20 minutes of work in total.

## Notes

- Same setup for everyone: same machine, same files, at most 4 CPU cores and 2.5 GB of memory each, no personal
  instructions, skills, MCP servers or hooks visible to the agents.
- Local paths were anonymized for publication (`/race` is the race folder, `/opt/dsda-doom` the engine). The hashes in
  `KILIT.sha256` were taken from the original files, before that change, so `check.py` and `insan_olc.py` no longer
  match them byte for byte; nothing else was edited.
- Astra and Kimi downloaded the DSDA-Doom source and built their own copy as a simulator. The source and the builds are
  not included (`agents/astra/simulator.patch` shows Astra's changes).

## License

Text, data and demos: CC BY 4.0 (`LICENSE`). Code: MIT (`LICENSE-CODE`). Doom and `DOOM1.WAD` belong to id Software;
DSDA-Doom is GPL.
