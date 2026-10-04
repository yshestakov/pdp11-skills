# PDP-11 "Hello, World!" - PDP-11/MACRO-11 Program Examples

This directory contains PDP-11 MACRO-11 assembly language programs that demonstrate "Hello, world!" output using different approaches.

## Quick Start

### Prerequisites

- **SIMH PDP-11 simulator**: `/opt/local/bin/simh-pdp11` (v3.9)
- **macro11 cross-assembler**: `/usr/local/bin/macro11`
- **pclink11 linker**: `/usr/local/bin/pclink11`
- **obj2bin.pl**: `$HOME/bin/obj2bin.pl` (for bare-metal .LDA conversion)
- **RT-11 V5.3 disk image**: `rt11-work.dsk`

### Files

| File | Description | Size |
|------|-------------|------|
| `h0bare.mac` | Bare-metal version (direct TTY access) | 380 B |
| `h0rt11.mac` | RT-11 version (.PRINT/.EXIT) | 380 B |
| `hello_hybrid.mac` | Hybrid example (both approaches) | 1.0 KB |
| `HELLO.LDA` | Original test file | 512 B |
| `SYSMAC.SML` | RT-11 system macros (30 KB) | 30 KB |

## Available Approaches

### 1. Bare-Metal Direct TTY Access
**File**: `h0bare.mac`

Outputs "Hello, world!" by directly accessing the DL11 console registers without an operating system.

**Advantages:**
- Pure PDP-11 assembly (no OS dependencies)
- Shows low-level hardware control
- Excellent for learning PDP-11 assembly and hardware

**Technical Details:**
- DL11 TTY registers (octal addresses):
  - RCSR: 177560 (Receiver Control/Status - bit 200 = ready)
  - RBUF: 177562 (Receiver Buffer)
  - XCSR: 177564 (Transmitter Control/Status - bit 200 = ready)
  - XBUF: 177566 (Transmitter Buffer)
- Polling loops to wait for transmitter ready
- Code absolute at octal address 1000
- Ends with HALT instruction

**Build (Cross-compile):**
```bash
# Assemble
macro11 -o h0bare.obj -l h0bare.lst h0bare.mac -m SYSMAC.SML

# Convert to LDA (absolute loader format)
obj2bin.pl --rt11 --binary --outfile=h0bare.lda h0bare.obj 2>/dev/null

# Run in SIMH
/opt/local/bin/simh-pdp11 .opencode/skills/simh-pdp11/assets/bare-metal.ini h0bare.lda
```

**Build (In RT-11):**
```bash
# Copy source to disk image
python3 .opencode/skills/simh-pdp11/scripts/rt11fs.py \
    put rt11-work.dsk h0bare.mac

# Assemble and link in RT-11
python3 .opencode/skills/simh-pdp11/scripts/rt11_do.py \
    rt11-rl02.ini \
    "MACRO H0BARE/LIST" \
    "LINK/LDA H0BARE"

# Get the executable
python3 .opencode/skills/simh-pdp11/scripts/rt11fs.py \
    get rt11-work.dsk H0BARE.LDA

# Run in SIMH
/opt/local/bin/simh-pdp11 \
    .opencode/skills/simh-pdp11/assets/bare-metal.ini H0BARE.LDA
```

**Sample Output:**
```
Hello, world!
PDP-11 simulator V3.9-0
Disabling XQ

HALT instruction, PC: 001060 (ADD (R5)+,(R0))
==REGS==
R0:    000000
R1:    001076
R2:    000000
R3:    000000
R4:    000000
R5:    000000
SP:    000000
PC:    001060
PSW:   000340
Goodbye
```

---

### 2. RT-11 Programmed Requests
**File**: `h0rt11.mac`

Uses RT-11 operating system services (programmed requests) for terminal I/O.

**Advantages:**
- Simpler, cleaner code
- Uses established RT-11 conventions
- Works on any RT-11 system
- Proper OS integration

**Technical Details:**
- Uses `.MCALL` macros (.PRINT, .EXIT)
- RT-11 EMT (Emergency Call) instructions for system services
- RT-11 conventions for arguments (source = destination in MOV)
- Proper transfer address (double colon `START::` for global symbol)
- Clean exit via .EXIT

**Build (Cross-compile):**
```bash
# Assemble with RT-11 system macros
macro11 -o h0rt11.obj -l h0rt11.lst h0rt11.mac -m SYSMAC.SML

# Link for RT-11 .SAV format
pclink11 h0rt11.obj /EXECUTE:h0rt11.sav

# Copy to disk image
python3 .opencode/skills/simh-pdp11/scripts/rt11fs.py \
    put rt11-work.dsk h0rt11.mac

# Assemble and link in RT-11
python3 .opencode/skills/simh-pdp11/scripts/rt11_do.py \
    rt11-rl02.ini \
    "MACRO H0RT11/LIST" \
    "LINK H0RT11"
```

**Build & Run (In RT-11):**
```bash
python3 .opencode/skills/simh-pdp11/scripts/rt11_do.py \
    rt11-rl02.ini \
    "MACRO H0RT11/LIST" \
    "LINK H0RT11" \
    "RUN H0RT11"
```

**Sample Output:**
```
Hello, world!

.
```

---

### 3. Hybrid Example
**File**: `hello_hybrid.mac`

A single source file that can be built for either bare-metal or RT-11 by uncommenting the appropriate code sections.

**For RT-11 (default, uncommented):**
- Uses .PRINT/.EXIT system macros
- Proper RT-11 conventions

**For Bare-Metal (comment RT-11, uncomment bare sections):**
- Uses direct DL11 register access
- Polling loops for transmitter ready
- Absolute code at 1000

## Key MACRO-11 Syntax

### Registers
- `R0`-`R5`: General purpose registers
- `SP` (= R6): Stack pointer
- `PC` (= R7): Program counter

### Addressing Modes
```asm
# Immediate    MOV #10,R0        ; R0 = 10 (octal)
# Register     MOV R1,R2         ; R2 = R1
# Memory       MOV X(R1),R0      ; R0 = memory at R1+X
# Autoinc      MOV (R1)+,R0      ; R0 = *R1++, R1 += 2
# Absolute     MOV @#177564,R0   ; R0 = *(uint8_t*)177564
```

### Data Directives
```asm
        .BYTE   0               ; Single byte
        .WORD   1,2,3           ; Words (16-bit)
        .ASCIZ  /Hello/         ; ASCIIZ string (0-terminated)
        .ASCII  /ABC/           ; ASCII (no terminator)
        .RAD50  /ABC/           ; Radix-50 encoding
        .EVEN                   ; Align to even address
```

### Labels
- Single colon `label:` = local symbol
- Double colon `label::` = global symbol
- Only first 6 characters significant

### Numbers
- **Default is octal**: `MOV #10,R0` loads octal 10 (decimal 8)
- **Decimal suffix**: `10.` for decimal 10
- **Explicit radix**: `^D10`, `^O12`, `^B1010`

## TTY Register Reference (DL11 Console)

```
         Octal   Function
         ------  --------
177560   RCSR    Receiver Control/Status (bit 200 = ready)
177562   RBUF    Receiver Buffer (read for character)
177564   XCSR    Transmitter Control/Status (bit 200 = ready)
177566   XBUF    Transmitter Buffer (write to send)

Ready bit = 200 octal (bit 7, 128 decimal)
```

**Polling loop pattern:**
```asm
L:  TSTB    @#177564      ; Check ready bit
    BPL     L             ; Branch if positive (not ready)
    MOVB    R0,@#177566   ; Output character
```

## Key Differences: Bare-Metal vs RT-11

| Feature | Bare-Metal | RT-11 |
|---------|------------|-------|
| OS Required | No | Yes |
| Code Location | Absolute at 1000 | relocated by LINK |
| I/O Method | Direct register access | System macros (EMT) |
| Register Preservation | All registers preserved | R0 destroyed, R1-R5 preserved |
| Code Size | Larger (polling loops) | Smaller (macros) |
| Portability | Hardware-specific | RT-11 systems only |
| Debugging | More complex | Easier (system facilities) |

## Build Commands Reference

### Cross-Compile Workflow
```bash
# Set up working directory
cd $HOME/Documents/work/ai/macro11-oc-qcn/work
cp .opencode/skills/rt11-prog/rt11-prog/assets/SYSMAC.SML .

# Build bare-metal
macro11 -o h0bare.obj -l h0bare.lst h0bare.mac -m SYSMAC.SML
obj2bin.pl --rt11 --binary --outfile=h0bare.lda h0bare.obj 2>/dev/null
/opt/local/bin/simh-pdp11 .opencode/skills/simh-pdp11/assets/bare-metal.ini h0bare.lda

# Build RT-11
macro11 -o h0rt11.obj -l h0rt11.lst h0rt11.mac -m SYSMAC.SML
pclink11 h0rt11.obj /EXECUTE:h0rt11.sav
```

### In-Simulation Workflow
```bash
# Copy source
python3 .opencode/skills/simh-pdp11/scripts/rt11fs.py \
    put rt11-work.dsk h0bare.mac

# Build and run in RT-11
python3 .opencode/skills/simh-pdp11/scripts/rt11_do.py \
    rt11-rl02.ini \
    "MACRO H0BARE/LIST" \
    "LINK/LDA H0BARE" \
    "COPY H0BARE.LDA RL0:"

# Get listing back
python3 .opencode/skills/simh-pdp11/scripts/rt11fs.py \
    get rt11-work.dsk H0BARE.LST
```

## Technical Notes

### System Communication Area (RT-11)
```
Address (octal)  Name  Description
---------------  ----  ----------------------------------
40               -     Program start address (from .END)
42               -     Initial stack pointer
44               JSW   Job Status Word (bit flags)
50               -     Program high limit
52               ERRBYT Error byte from EMT requests
53               USERRB User error severity
54               -     RMON base address
```

### Commonly Used JSW Bits
```
10000 (TTSPC$) - Terminal special mode (no line buffer)
40000 (TTLC$)  - Enable lower-case input
100 (TCBIT$)   - Inhibit terminal wait
```

### RT-11 Error Handling
```asm
EMT requests set Carry flag on error
Error code in byte 52 (ERRBYT)

Example:
    .LOOKUP #AREA,#0,#FILENAME
    BCS     ERROR              ; Branch if carry set
    ; Success path
ERROR:
    MOVB    @#52,R0            ; Get error code
```

## References

- **MACRO-11 Language Reference Manual** (AA-5075A-TC, Aug 1977)
- **RT-11 Programmer's Reference Manual** (AA-H378C-TC, July 1984)
- **SIMH PDP-11 Simulator** (v3.9-0)
- **RT-11 System Macro Library** (SYSMAC.SML)

## Examples in Other Directories

- `$HOME/Documents/macro11-oc-qcn/work/` - This directory
- `.opencode/skills/rt11-prog/rt11-prog/references/examples/tested/` - tested examples (ttyt.mac, nx.mac, timer.mac)

## License

None - public domain for educational purposes.

---

**Author**: PDP-11 Retro Computing Project  
**Last Updated**: October 2026  
**Platform**: macOS, SIMH PDP-11 V3.9-0, RT-11 V5.3
