---
name: rt11-prog
description: RT-11 system programming reference and workflow - programmed requests (.LOOKUP .ENTER .READW .CSIGEN .GTLIN .TTYIN .MRKT .TWAIT .QSET .SETTOP .CHAIN, completion routines, F/B messaging, XM regions/windows), SYSLIB subroutines (FORTRAN-callable, or from MACRO via R5 argument lists), device handlers (.DRDEF/.DRBEG/.DRAST/.FORK/.DRFIN/.DREND) and the VT11 display file handler, built from DEC's RT-11 Programmer's Reference Manual (AA-H378C-TC) plus the real V5.3 SYSMAC.SML. Use whenever someone writes, reviews, explains or debugs an RT-11 program or handler, asks what a programmed request does / which EMT / what error code / which JSW bit, calls SYSLIB, or ports code to or from RT-11 - even if they only say "PDP-11 program that reads a file" or paste code containing .MCALL.
---

# RT-11 programming (programmed requests, SYSLIB, handlers)

Source of truth: DEC **RT-11 Programmer's Reference Manual AA-H378C-TC (July 1984, RT-11 V5.1)**,
split into `references/`, plus the actual **V5.3 SYSMAC.SML** (`references/sysmac_v53.mac` as
text, `assets/SYSMAC.SML` as the binary library). The user's running system is RT-11 V5.3 FB
under SIMH; V5.3 is a superset of V5.1 (it adds e.g. `.DRPTR`, `.DREST`, `.MODULE`).

Related skills, if available: **macro11** for assembler syntax, **simh-pdp11** for building and
running programs inside RT-11 (`rt11fs.py`, `rt11_do.py`, `simh_run.py`).

## How to look things up

1. `references/00-index.md` lists every request (Ch.2, §2.1–2.104), SYSLIB routine (Ch.3,
   §3.1–3.113) and display macro (App. A) with the file that holds it. Grep that file for
   `## 2.46` or for the name (`\.LOOKUP`); a few headings were lost in OCR.
2. Each entry gives macro form, argument meanings, the errors returned in byte 52, notes and an
   example. Read the whole entry before using a request you haven't used in this conversation:
   argument order differs between requests, and several have FB/XM-only behavior.
3. When the exact expansion matters (what goes in R0, which EMT, argument-block layout, which
   arguments are optional), read the macro in `references/sysmac_v53.mac`. Names there are
   truncated to 6 characters (`.PROTE` = `.PROTECT`), and most expand through the
   `...CMn` helper macros defined at the top of the file.
4. Concepts (EMT formats, channels, USR swapping, completion routines, F/B, XM, handlers,
   version conversion): `01-programmed-request-concepts.md`; SYSLIB conventions and the
   FORTRAN/MACRO interface: `02-syslib-concepts.md`.

OCR noise in the manual text: `,MCALL` means `.MCALL`, `RO` means `R0`, `\*`/`*` sometimes means
`#`. Example code in the manual is a guide, not a source to copy blind; the tested programs in
`references/examples/tested/` and the DEC sources in `references/examples/` are reliable.

## Conventions that cause most bugs (each checked on RT-11 V5.3 FB)

- **R0 is not preserved by programmed requests. R1-R5 are.** That includes the "harmless" ones:
  `.TTYOUT #'[` loads R0, so a character you just got from `.TTYIN` is gone; `.PRINT` puts
  its address in R0. Keep values in R1-R5 across requests.
- **Error reporting**: the request returns with the C bit set and a code in byte 52 (`ERRBYT`).
  Test `BCS` immediately after the request. Codes are request-specific (look them up). For
  example `.LOOKUP` file not found = 1 (channel already open = 0); `.READW` past end of file
  = C set with code 0. Fatal monitor errors (`?MON-F-…`) abort the job unless `.SERR` is in
  effect.
- **Arguments are source operands of a MOV**: `#4` means the value 4, `4` means "the contents
  of location 4". The manual calls this the most common mistake. The same goes for
  `#AREA` vs `AREA`, `#BUF` vs `BUF`. A memory operand like `IBLK` (no #) is right when you
  want its current contents, as with a block number that changes in a loop.
- **Argument blocks (`area`)**: EMT 375 requests take an area block; allocate enough words
  (`.BLKW 10.` covers every request). A blank argument means "already in the block", which is
  handy in loops but stale data in the block is a classic bug.
- **Channels**: 0-15 by default (`.CDFN` for up to 255); 15 is used by the overlay handler and
  255 is the system's. A channel must be free for `.LOOKUP`/`.ENTER`. Release it with `.CLOSE`
  (makes an `.ENTER`ed file permanent) or `.PURGE` (discards it).
- **Device blocks** are 4 words of Radix-50: `.RAD50 /DK FILNAMTYP/` with each field
  left-justified and space-filled, and no `:` or `.`.
- **Handlers must be in memory** before `.LOOKUP`/`.ENTER`/I/O on a non-resident device: `.FETCH`
  it first (`.CSIGEN` does this for you). The system device and `LOAD`ed handlers are resident.
- **`.ENTER` length**: 0 = the larger of half the largest free area and the second-largest
  area, -1 = the largest area, n = exactly n blocks. The file stays tentative until `.CLOSE`.
- **`.READW`/`.WRITW`** count in **words** and address 512-byte **blocks**; `.READW` returns
  the number of words actually read in R0. RT-11 files have no byte length, so text ends at
  NULs or ^Z in the last block.
- **`.CSIGEN`** prompts `*` (or takes a string), opens outputs on channels 0-2 and inputs on
  3-8, loads handlers at `devspc`, and returns the first free address in R0. On a syntax or
  file error it prints `?CSI-F-…` and prompts again itself: your program never sees the error.
  `.CSISPC` only parses, so use it when you want to handle errors.
- **Terminal**: `.TTYIN` waits for a whole line unless JSW bit 10000 (TTSPC$, special mode:
  no echo, one character at a time, CR comes through as 015) is set. Bit 40000 (TTLC$) lets lower
  case through. Under FB/XM, `.TTINR`/`.TTOUTR` block like `.TTYIN`/`.TTYOUT` unless JSW bit 100
  is set, and only then return with C set when nothing is ready. Clear the bits before exiting. `.PRINT` strings end with 0 (adds CR/LF) or 200 (no CR/LF).
  `.GTLIN buf,prompt` returns an ASCIZ line of up to 80 characters and also reads indirect
  command files.
- **Asynchronous requests** (`.MRKT`, `.TWAIT`, `.READC`/`.WRITC`, `.READ` + `.WAIT`, `.SDAT`
  etc.) each need a free queue element. Add elements with `.QSET` (7 words each under SJ/FB,
  10 under XM) early in the program, or concurrent requests will block.
- **Completion routines** are entered by `JSR PC` with R0/R1 set (for I/O: R0 = channel status
  word, R1 = channel; for `.MRKT`: R0 = the id). They must exit with `RTS PC` (never `.EXIT`),
  save anything except R0/R1, never issue USR requests (`.LOOKUP`, `.ENTER`, `.CLOSE`…), and
  must not live where the USR swaps. Under SJ they can interrupt one another; under FB/XM they
  run one at a time.
- **Monitor differences**: each entry's title says *(FB and XM Only)*, *(XM Only)*,
  *(Special Feature)* or *(SYSGEN option)*. Check it before using such a request on an SJ
  system. V5.3 here boots RT11FB.
- **System communication area** (low memory): 40 start address, 42 initial SP, 44 JSW,
  46 USR swap address, 50 high limit, 52 ERRBYT, 53 USERRB, 54 RMON base. `.GVAL` reads
  monitor fixed offsets portably. Prefer it to `@#54` arithmetic.

## Calling SYSLIB from MACRO

SYSLIB.OBJ uses the FORTRAN convention: `MOV #ARGS,R5` / `JSR PC,routine`, where `ARGS: .WORD n,
addr1, addr2…` holds the argument count followed by the **addresses** of the arguments (even for
constants). Integer function results come back in R0 (INTEGER*4 in R0/R1). Declare the names
`.GLOBL`. RT-11 `LINK` searches `SY:SYSLIB.OBJ` automatically (verified), so `LINK PROG` is
enough. The routine may use all registers, so save what you need. An omitted optional argument is
written as address `-1` in the list (see §1.2.3).

FORTRAN programs: `CALL IGETC()`, `ICSI`, `LOOKUP`, `IREADW`… in Chapter 3. No FORTRAN IV
compiler is installed on the user's V5.3 disk, so FORTRAN can't be tested there. Say so if asked
to run FORTRAN.

## Device handlers

Structure (§1.1.3.12, §2.20-2.28, §2.35, §2.91, §2.92):
`.DRDEF name,code,stat,size,csr,vec` (preamble: defines symbols, `.MCALL`s the rest) →
`.DRBEG name` (header) → I/O initiation (pick up the current queue element `nameCQE`, start
the device) → `.DRAST name,pri` interrupt entry (often with `.FORK`) → `.DRFIN name` (return
the element to the monitor) → optional `.DRBOT` boot code → `.DREND name`. V5.3 sources also use
`.DRPTR`, `.DREST`, `.MODULE`, which aren't in the V5.1 manual. Copy their use from the DEC
handlers in `references/examples/` (NL = simplest, PC = paper tape, LP = printer, RK = disk).

Build and load sequence for FB, verified with a renamed copy of NL (`examples/tested/nx.mac`):
```
.MACRO NX
.LINK/EXECUTE:NX.SYS NX
.INSTALL NX        ! adds it to the device tables (until reboot)
.LOAD NX           ! optional: make it resident
.COPY HELLO.MAC NX:
.UNLOAD NX
```
For XM the convention is to assemble with the XM.MAC prefix file (`MMG$T=1`):
`MACRO XM+NX/OBJECT:NXX`, then `LINK/EXECUTE:NXX.SYS NXX`. This was not tested here, so say so.
Use a device code that isn't taken (the second `.DRDEF` argument).

## Display file handler (Appendix A)

`10-display-file-handler.md` and `examples/VTMAC.MAC` cover the VT11/VS60 graphics macros. SIMH
v3.9's PDP-11 has **no VT11 emulation**, so display programs can be written and assembled but not
run here. Say so instead of claiming they work.

## Verifying programs

Assemble and run what you write rather than presenting untested code:

1. Quick syntax check on the host (if `macro11` is available):
   `macro11 -m <skill>/assets/SYSMAC.SML -o /dev/null -l prog.lst prog.mac` resolves the
   real V5.3 programmed-request macros.
2. Real run in RT-11 under SIMH (simh-pdp11 skill): `rt11fs.py put disk.dsk prog.mac`, then
   `rt11_do.py sys.ini "MACRO PROG" "LINK PROG" "RUN PROG"`. For programs that prompt (`*` from
   `.CSIGEN`, `.GTLIN`), drive them with `simh_run.py` steps (`expect ^\*` / `line OUT=IN`).
3. If you can't run it, say what you checked and what you didn't.

`references/examples/tested/` holds programs that ran on V5.3 FB: `upcase.mac` (`.CSIGEN`,
`.READW`/`.WRITW` loop, EOF via ERRBYT, `.CLOSE`), `timer.mac` (`.QSET`, `.MRKT` completion
routine, `.TWAIT`, `.GTIM`), `ttyt.mac` (`.GTLIN` with prompt, JSW special mode, `.LOOKUP` error
code), `slib.mac` (SYSLIB `IPEEK`/`IRAD50` from MACRO), `nx.mac` (minimal handler). Start from
the closest one.

## Answering questions

Cite the section (`PRM §2.46 .LOOKUP`) and quote the relevant rule or error-code table. Note when
behavior depends on the monitor (SJ/FB/XM), on the version (V5.1 manual vs V5.3 system), or on a
SYSGEN option.
