#!/bin/bash
# build_hybrid.sh - Build hybrid hello program (defaults to RT-11 mode)
# Usage: ./build_hybrid.sh [--rt11|--bare]

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

TARGET_MODE="${1:-rt11}"

if [[ "$TARGET_MODE" == "--rt11" ]]; then
    SOURCE="hello_hybrid.mac"
    MODE="RT-11"
    OBJ="hello_hybrid.obj"
    LDFLAGS="/EXECUTE:hello_hybrid.sav"
elif [[ "$TARGET_MODE" == "--bare" ]]; then
    # For bare-metal, we need to process the hybrid file to uncomment the bare code
    SOURCE="/tmp/h0hybrid.mac"
    MODE="bare-metal"
    OBJ="hello_hybrid.obj"
    LDFLAGS="/EXECUTE:hello_hybrid.sav"
    
    # Create bare-metal version by uncommenting the bare-metal code
    awk '
    /^START::\.PRINT/ { print "START:: MOV     #MSG,R1"; next }
    /^MSG:/ { print "1$:      MOVB    (R1)+,R0"; print "         TSTB    R0"; print "         BEQ     2$"; next }
    /^        \.END/ { print "         BR      1$"; print "2$:      TTYWAIT 4$"; print "         MOVB    #15,@#DLXBUF"; print "         TTYWAIT 5$"; print "         MOVB    #12,@#DLXBUF"; print "         HALT"; print "MSG:    .ASCIZ  /Hello, world!/"; print "        .EVEN"; print "        .END    START"; exit }
    { print }
    ' "$SCRIPT_DIR/hello_hybrid.mac" > "$SOURCE"
else
    echo "Usage: $0 [--rt11|--bare]"
    exit 1
fi

SYSMAC="$SCRIPT_DIR/SYSMAC.SML"
if [[ ! -f "$SYSMAC" ]]; then
    echo "Error: $SYSMAC not found"
    exit 1
fi

echo "=== Assembling $SOURCE ($MODE) ==="
macro11 -o "$OBJ" -l hello_hybrid.lst "$SOURCE" -m "$SYSMAC"

if [[ "$TARGET_MODE" == "--bare" ]]; then
    echo "=== Converting to LDA (bare-metal loader format) ==="
    obj2bin.pl --rt11 --binary --outfile=hello_hybrid.lda "$OBJ"
    echo "=== Build complete - hello_hybrid.lda ==="
else
    echo "=== Linking for RT-11 ==="
    pclink11 "$OBJ" $LDFLAGS
    echo "=== Build complete - hello_hybrid.sav ==="
fi
