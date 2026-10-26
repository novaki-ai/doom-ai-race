#!/usr/bin/env bash
# Check every submitted demo with the official checker; print a summary.
cd "$(dirname "$0")/.." || exit 1
for f in submit/E1M*.lmp; do python3 check.py "$f"; done
