#!/bin/bash
# build_h0bare.sh - Build bare-metal hello program for PDP-11
# Uses cross-compiler tools on the host

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

SYSMAC="SYSMAC.SML"
if [[ ! -f "$SYSMAC" ]]; then
    echo "Error: $SYSMAC not found in working directory"
    echo "Run: cp .opencode/skills/rt11-prog/rt11-prog/assets/$SYSMAC ."
    exit 1
fi

echo "=== Assembling h0bare.mac (bare-metal) ==="
macro11 -o h0bare.obj -l h0bare.lst h0bare.mac -m "$SYSMAC"

echo "=== Converting to LDA (bare-metal loader format) ==="
obj2bin.pl --rt11 --binary --outfile=h0bare.lda h0bare.obj

echo "=== Build complete ==="
ls -lh h0bare.*
