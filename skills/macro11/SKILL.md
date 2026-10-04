---
name: macro11
description: Write, read, explain, debug, and port PDP-11 MACRO-11 assembly language, with RT-11 as the default target OS. Bundles the DEC MACRO-11 Language Reference Manual (AA-5075A-TC) split by chapter plus RT-11 programmed-request notes. Use whenever the user mentions MACRO-11, PDP-11 assembly, .MAC files, RT-11 / RSX / RSTS programs, SIMH pdp11, octal opcodes, assembly listings with error letters, DEC directives (.PSECT, .MCALL, .ASCIZ, .RAD50, .IRP…), or wants PDP-11 code translated to/from C or another assembly — even if they just paste PDP-11 code without naming the language.
---

# MACRO-11 (PDP-11 assembler)

MACRO-11 is DEC's assembler for the 16-bit PDP-11. Its syntax has several traps that modern-assembler habits get wrong (octal by default, no operator precedence, 6-character symbols, odd-address errors). This skill gives a compact cheat sheet for the common cases and points to the full manual text for the rest.

## How to use this skill

1. Decide the task type: **write**, **read/explain/review**, **port**, or **answer a manual question**.
2. Use the cheat sheet below for routine work. Open a reference file when the question touches its topic, when you're unsure of an exact rule, or when the user wants a citation. Cite as "MACRO-11 manual §6.3.4" so the user can find it.
3. Default target is **RT-11** unless the user says RSX-11M, RSTS/E, or bare metal. For RT-11 system calls (`.PRINT`, `.TTYOUT`, `.LOOKUP`, …), read `references/rt11.md` — those macros are not in the MACRO-11 manual.

### Reference files (in `references/`)

| File | Covers | Read when |
| --- | --- | --- |
| `01-format-symbols-expressions.md` | Statement format, labels, character set, symbols, `=` assignment, registers, local symbols `n$`, `.`, numbers, expressions | Syntax questions, expression evaluation, local-symbol scope |
| `02-relocation-addressing-modes.md` | Relocation/linking flags (`'`, `G`, `C`), all 12 addressing modes, branch range, traps | Any addressing-mode question; explaining listing flags |
| `03-directives-listing-data-radix.md` | `.LIST/.NLIST`, `.TITLE/.SBTTL/.IDENT`, `.ENABL/.DSABL` options, `.BYTE/.WORD/.ASCII/.ASCIZ/.RAD50/^R`, `.RADIX`, `^D ^O ^B ^C ^F`, `.FLT2/.FLT4` (OCR lost part of this section), `.EVEN/.ODD/.BLKB/.BLKW` | Data definitions, listing control, numeric operators |
| `04-directives-psect-globl-conditionals.md` | `.END`, `.EOT`, `.LIMIT`, `.PSECT/.ASECT/.CSECT` attributes, `.GLOBL`, `.IF/.IFF/.IFT/.IFTF/.ENDC/.IIF` | Multi-module programs, sections, conditional assembly |
| `05-macros.md` | `.MACRO/.ENDM/.MEXIT`, argument passing (`<>`, `^/…/`, `\` value, `?` generated locals, keyword args), `.NARG/.NCHR/.NTYPE`, `.ERROR/.PRINT`, `.IRP/.IRPC/.REPT`, `.MCALL` | Writing or decoding macros |
| `06-ascii-radix50-syntax-summary.md` | ASCII and Radix-50 tables, special characters, addressing syntax summary, alphabetical directive summary | Quick lookups, RAD50 encoding |
| `07-opcodes-and-error-codes.md` | Every op code with octal value; error letters A–Z | Hand-assembling/disassembling, decoding listing errors |
| `08-coding-standard.md` | DEC's house coding standard (layout, naming, module header, forbidden practices) | Code review, "make this idiomatic" |
| `09-memory-and-pic.md` | Assembler memory tips, position-independent code rules | PIC questions, `@#` vs relative |
| `10-sample-listing.md` | A real DEC module with listing | Seeing idiomatic production style |
| `rt11.md` | RT-11 program skeleton, build commands, programmed requests, file I/O, ERRBYT, JSW, device registers | Any RT-11 program |

Files over 300 lines start with a contents list; grep for the directive name (e.g. `grep -n '\.PSECT' references/*.md`) rather than reading whole files.

## Cheat sheet

### Line format
`label: operator operands ;comment` — fields separated by spaces/tabs. Global label: `NAME::`. Direct assignment: `SYM = expr` (global: `SYM == expr`). DEC style is tab-separated columns, upper case.

### Numbers and constants — the #1 source of bugs
- **Default radix is octal.** `MOV #10,R0` loads 8. Write decimal with a trailing dot: `10.`. A digit 8 or 9 without the dot is an **N** error.
- Explicit radix: `^D100`, `^O144`, `^B1100100`. `.RADIX 10` changes the default (avoid in shared code; it confuses readers).
- Characters: `'A` = one ASCII char (value 101), `"AB` = two chars packed into a word (low byte A). `^RABC` = Radix-50 word.
- `^C expr` = one's complement, `^F 1.5` = one-word float.
- Numbers are 16-bit; anything over 177777 is truncated (**T**).

### Symbols
- Characters A–Z, 0–9, `$`, `.`; must not start with a digit. **Only the first 6 characters are significant** — `COUNTER1` and `COUNTER2` collide (**M** error). Choose ≤6-char names.
- Names with `$` and `.` are by convention reserved for DEC system software — avoid them in user symbols.
- Registers: `R0`–`R5`, `SP` (=R6), `PC` (=R7); `%n` is register n.
- Local labels `1$`–`65535$` live between two ordinary labels (or within `.ENABL LSB` … `.DSABL LSB`). Use `1$`–`63$` by hand; `64$`–`127$` are reserved for macro-generated (`?`) locals.

### Expressions — no precedence
Evaluated strictly **left to right**: `2+3*4` = 20, not 14. Use angle brackets for grouping: `2+<3*4>`. Operators: `+ - * /`, `&` (AND), `!` (inclusive OR). Unary: `-`, `^C`, `^B ^O ^D ^F ^R`. Division is integer.

### Addressing modes (mode/register field)
| Syntax | Mode | Notes |
| --- | --- | --- |
| `R` | 0 register | |
| `(R)` or `@R` | 1 register deferred | |
| `(R)+` | 2 autoincrement | by 1 for byte ops, 2 for word — always 2 for SP/PC |
| `@(R)+` | 3 autoincrement deferred | |
| `-(R)` | 4 autodecrement | push: `MOV X,-(SP)` |
| `@-(R)` | 5 autodecrement deferred | |
| `X(R)` | 6 index | |
| `@X(R)` | 7 index deferred | |
| `#n` | 2 on PC: immediate | |
| `@#A` | 3 on PC: absolute | use for device registers / fixed addresses |
| `A` | 6 on PC: relative | default for labels; position-independent |
| `@A` | 7 on PC: relative deferred | |

Branches (`BR`, `BEQ`, …, `SOB`) reach only −128…+127 words (SOB: backwards 0–63 words). Out of range → **A** error; invert the condition and use `JMP`.

### Common idioms
```asm
        MOV     R1,-(SP)        ; push
        MOV     (SP)+,R1        ; pop
        JSR     PC,SUB          ; call  (= CALL SUB)
        RTS     PC              ; return (= RETURN)
        CLR     R0              ; zero
        TST     R0              ; set N/Z from R0
        MOVB    (R1)+,R0        ; MOVB to a register SIGN-EXTENDS to 16 bits
        BIC     #^C377,R0       ; ...so mask to get an unsigned byte
        SOB     R2,LOOP         ; dec R2, branch if non-zero (backwards only)
```
- Signed compares: `BGT BGE BLT BLE`. Unsigned/address compares: `BHI BHIS BLO BLOS`.
- `CMP A,B` sets flags from A−B (source minus destination — the opposite of `SUB`'s operand roles, where `SUB A,B` computes B−A).
- `MUL`/`DIV`/`ASH`/`ASHC` (EIS) and `XOR`/`SXT`/`SOB`/`MARK` don't exist on the smallest models (11/04, 11/05, 11/20); `MUL Rn` with even Rn gives a 32-bit product in Rn:Rn+1. If the user's target is unknown, mention the dependency when you use them.
- Word data and instructions must be at even addresses: put `.EVEN` after `.ASCII`/`.ASCIZ`/`.BYTE`/`.BLKB` blocks (else **B** error).
- `.END START` — names the entry point; required to get a runnable program.

### Data
```asm
TABLE:  .WORD   1,2,3           ; words
FLAGS:  .BYTE   0,377           ; bytes
MSG:    .ASCIZ  /Hello/         ; delimiter can be any char not in string
        .ASCII  <15><12>/Next/  ; <n> embeds a byte value
        .EVEN
BUF:    .BLKW   64.             ; reserve 64 decimal words
NAME:   .RAD50  /ABCDEF/        ; 3 chars per word
```

### Macros (minimal)
```asm
        .MACRO  PUSH    REG
        MOV     REG,-(SP)
        .ENDM   PUSH

        .MACRO  WAITRDY CSR,?L          ; ?L => unique generated local (64$..)
L:      TSTB    @#CSR
        BPL     L
        .ENDM
```
Pass an expression's *value* as text with `\` (`FOO \N`). Test blank args with `.IF B <ARG>` / `.IF NB`. Details: `05-macros.md`.

### Conditional assembly
`.IF EQ expr` … `.IFF` … `.ENDC`. Conditions: `EQ NE GT LE LT GE` (on value), `DF NDF` (symbol defined), `B NB IDN DIF` (macro args). One-line form: `.IIF NE DEBUG, JSR PC,TRACE`.

## Task guidance

### Writing code
- Produce a complete, assemblable source unless asked for a fragment: `.TITLE`, `.MCALL` (RT-11), code, data, `.EVEN`, `.END entry`.
- Comment every non-obvious line (`;` comments in column 33 / after the 4th tab is DEC style). Comments are expected in assembly — the reader can't see types.
- State register usage at the top of each subroutine (inputs, outputs, clobbered), DEC style. RT-11 programmed requests clobber R0.
- Write decimal literals with `.` whenever a human would think in decimal (counts, ASCII lengths); keep masks and addresses octal.
- After writing, mentally assemble it once: check every symbol ≤6 unique chars, every decimal constant has a dot, branches are in range, `.EVEN` after byte data, the stack is balanced on every path, and the C bit is tested right after any RT-11 request that can fail.
- If a `macro11` cross-assembler is on PATH (or you can build it — see `rt11.md`), actually assemble the file and fix every reported error before handing it over.
- If a `pclink11` linker is on PATH (or you can build it — see `rt11.md`), actually link .OBJ file produced by `macro11` cross-compiler and fix every reported error before handing it over.
- If the user can run it, give the build/run commands (see `rt11.md`).

### Reading / explaining / reviewing
- Convert octal constants to decimal in your explanation where it helps (`#15` → 13 = CR).
- For listings: column order is error letter(s), line number, location, generated word(s), source. Flags: `'` relocatable, `G` global (resolved at link), `C` complex relocatable. Error letters are in `07-opcodes-and-error-codes.md`.
- When disassembling octal words: top bits pick the opcode family (see `07-…`); for double-operand instructions the format is `ooSSDD` where each operand is 3 bits mode + 3 bits register.
- In reviews, look especially for: decimal intended but octal written, MOVB sign extension, signed vs unsigned branch, missing `.EVEN`, unbalanced stack, unchecked C bit after RT-11 requests, 6-char symbol collisions, relying on operator precedence.

### Porting
- Model the PDP-11 precisely: 16-bit words, little-endian bytes, two's complement, byte ops on registers sign-extend, condition codes N Z V C.
- MACRO-11 → C: use `uint16_t`/`int16_t`/`uint8_t` so wraparound and sign behave the same; keep octal literals as `0`-prefixed C octal or convert with a comment; turn `JSR PC` subroutines into functions and document which registers were inputs/outputs; replace RT-11 requests with stdio equivalents and note any semantic differences (e.g. `.PRINT` 0 vs 200 terminator, `.TTYIN` line buffering).
- C/other asm → MACRO-11: decide register allocation explicitly, use the stack for locals, and watch for 32-bit arithmetic (needs `ADC`/`SBC` chains or `ASHC`/`MUL`/`DIV`).
- Flag anything that can't be ported faithfully rather than silently approximating it.

### Answering manual questions
Look the rule up in the relevant reference file instead of relying on memory, quote or paraphrase it, and cite the section number. The source manual is the August 1977 edition; later MACRO-11 versions (V5.x) added features (e.g. `.ENABL MCL`, `.INCLUDE`, `.LIBRARY`) — mention when something is version-dependent. The manual text is OCR output: tables and code alignment can be imperfect, and a few headings/rows were lost (the error-code table has a supplement at the end of `07-…`).
