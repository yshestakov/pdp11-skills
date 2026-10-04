---
name: rt11-utils
description: Use RT-11 system utilities correctly - PIP, DUP, DIR, LINK, LIBR, MACRO/CREF, SRCCOM, BINCOM, SLP, SIPP, PAT, DUMP, FILEX, FORMAT, BUP, LD logical disks, RESORC/SHOW, ODT debugging, QUEUE/SPOOL, VTCOM, error logging and BATCH - including CSI command-string syntax (out=in/opt), every utility option letter and its keyboard-monitor (KMON) equivalent. Built from DEC's RT-11 System Utilities Manual (AA-M239B-TC) and checked on RT-11 V5.3 under SIMH. Use whenever someone asks how to copy/rename/delete/squeeze/initialize/back up RT-11 files or volumes, build or link programs and libraries, compare or patch files, debug with ODT, or asks what a utility option like PIP /U or LINK /R means - even if they only say "on the PDP-11" or paste a `*` command line.
---

# RT-11 system utilities

Source: DEC **RT-11 System Utilities Manual AA-M239B-TC (July 1984, RT-11 V5.1)**, split by
chapter into `references/`. The user's system is **RT-11 V5.3 FB** under SIMH. The behaviors
marked *(verified)* below were run there.

Related skills, if available: **simh-pdp11** to actually run commands in RT-11 (`rt11_do.py`,
`simh_run.py`, `rt11fs.py`); **rt11-prog** for programmed requests; **macro11** for assembler
syntax.

## Finding the answer

| Utility | What it does | KMON commands that call it | Reference |
| --- | --- | --- | --- |
| CSI | command-string syntax shared by all utilities | – | `00-overview-and-csi.md` |
| (all) | option letter → KMON command/option table | – | `01-options-to-kmon-commands.md` |
| BINCOM | binary compare | DIFFERENCES/BINARY | `02-bincom.md` |
| BUP | back up a big volume onto several small ones | BACKUP, DIR/BACKUP, INIT/BACKUP | `03-bup.md` |
| DIR | directory listings | DIRECTORY | `04-dir.md` |
| DUMP | octal/ASCII/RAD50 dump of files and devices | DUMP | `05-dump.md` |
| DUP | INIT, SQUEEZE, BOOT, image copy, CREATE, bad blocks, volume ID | INITIALIZE, SQUEEZE, BOOT, COPY/DEVICE, CREATE, DIR/BADBLOCKS | `06-dup.md` |
| FILEX | DOS-11, interchange (IBM-format RX01) and TOPS-10 DECtape volumes | COPY/DOS, /INTERCHANGE, /TOPS | `07-filex.md` |
| FORMAT | format/verify volumes | FORMAT | `08-format.md` |
| LD | logical disks (files used as disks) | MOUNT, DISMOUNT, SET LD, SHOW SUBSET | `09-ld-logical-disks.md` |
| LIBR | object and macro libraries | LIBRARY | `10-libr.md` |
| LINK | linker: .SAV/.REL/.LDA/.SYS, maps, overlays, XM | LINK | `11-link.md` (largest; grep it) |
| MACRO/CREF | assembler command line, listings, cross reference | MACRO | `12-macro.md` |
| PIP | copy, rename, delete, protect, dates, concatenate | COPY, RENAME, DELETE, TYPE, PRINT, PROTECT | `13-pip.md` |
| RESORC | system resources | SHOW (CONFIG, MEMORY, DEVICES, JOBS…) | `14-resorc.md` |
| SRCCOM | source compare; makes SLP patch files | DIFFERENCES | `15-srccom.md` |
| ERRLOG | error logging (ELINIT, ELTASK, ERROUT) | – | `16-error-logging.md` |
| QUEUE/QUEMAN | print/output queue | PRINT, QUEUE | `17-queue.md` |
| SPOOL | transparent line-printer spooler | – | `18-spool.md` |
| VTCOM | talk to a host system | – | `19-vtcom.md` |
| ODT | on-line debugger | LINK/DEBUG | `20-odt.md` |
| PAT | patch object modules | – | `21-pat.md` |
| SIPP | patch .SAV images interactively | – | `22-sipp.md` |
| SLP | patch source files from a command file | – | `23-slp.md` |
| BATCH | batch control language ($JOB, $MACRO, $RUN…): compiler + BA run-time handler | `LOAD BA:`, ASSIGN LOG/LST, then `R BATCH` (A.7) | `24-batch.md` |

Read the relevant chapter before giving exact syntax; option letters differ between utilities
(`/D` is delete in PIP, `/D` restore in DUP, `/D` change bars in SRCCOM). Each file starts with a
contents list; grep for `## 13.4` or for an option like `/U`. The text is OCR: `,` can stand
for `.`, `O`/`0` and `l`/`1` get confused (`DLO:` = `DL0:`), and `RET` marks a RETURN keypress.

## Two ways to run a utility

1. **KMON command** (`COPY A.MAC DL1:`, `SQUEEZE DK:`, `LINK/MAP:TT: X`). KMON translates it
   into a utility command line. This is easiest for users; Appendix B
   (`01-options-to-kmon-commands.md`) gives the mapping.
2. **`R utility`** then a CSI line at the `*` prompt:
   `output1,output2,output3=input1,…,input6/option/option:value`. You can enter as many
   command lines as you like; each prints its results and prompts `*` again. Exit with
   **^C** *(verified)*. A bare RETURN prints the utility's version for most utilities.
   - Device defaults to DK:. Each utility has its own default file types (MACRO input .MAC,
     LINK .OBJ, LIBR .OBJ, SLP output = input name…).
   - Numeric option values are **octal** unless followed by `.` (`/K:3.`).
   - `TT:` as an output sends that output to the terminal (`HELLO,TT:=HELLO` = .SAV plus a
     map on the screen).
   - Messages are `?UTIL-S-text`, where S is the severity: I info, W warning, E error, F fatal.

## Verified cookbook (RT-11 V5.3 FB under SIMH)

```
.R PIP
*C.TXT=A.TXT                 copy
*D.TXT=C.TXT/R               rename
*D.TXT/D                     delete
*DL1:*.*=A.TXT,B.TXT/W       copy several files to a device; /W logs each one
*DL1:AB.TXT=A.TXT,B.TXT/U    concatenate into one file
^C
```
- `DL1:=A.TXT,B.TXT` (no `*.*` in the output) gives `?CSI-F-Invalid command`. Several inputs need
  a wildcard output, or /U to concatenate.

```
.R DIR            *TT:=*.TXT/E           full listing incl. <UNUSED> areas;  *DL1:/F  fast
.R DUMP           *TT:=A.TXT/O:0         block 0 in octal words + ASCII
.R SRCCOM         *TT:=A.TXT,B.TXT       same as DIFFERENCES A.TXT B.TXT
.R BINCOM         *TT:=HELLO.SAV,BAD.SAV
.R RESORC         */X                    = SHOW MEMORY  (/Z = SHOW CONFIGURATION)
```

Libraries and linking:
```
.R LIBR
*MYLIB=MODA,MODB             create MYLIB.OBJ from MODA.OBJ, MODB.OBJ
*,TT:=MYLIB                  list modules and their globals
.LINK MAIN,MYLIB/MAP:TT:     link against it, map on the terminal
```
- LIBR refuses modules with no global symbols: `?LIBR-F-Null library`. The linker finds
  library modules only through `.GLOBL` references.
- `LINK` also searches `SY:SYSLIB.OBJ` automatically.
- In the load map, `. ABS.` is 0–1000 (vectors and stack) and code starts at 1000. The map
  shows the transfer address and high limit.

Volumes (DUP):
```
.R DUP           *DL1:/Z/Y          initialize with no query  (= INITIALIZE/NOQUERY DL1:)
.SQUEEZE/NOQUERY DK:
```
- **Squeezing the system device reboots the monitor**, so the startup command file runs again.
  Scripts must expect the boot banner and the `.` prompt again.
- **New RL01/RL02 image under SIMH** *(verified)*: RT-11 needs a DEC bad-block table on the last
  track, or DUP /Z fails with `?DUP-F-Bad block in system area`.
  - If SIMH creates the file (ATTACH of a file that doesn't exist yet), SIMH 3.9 asks
    `Overwrite last track? [N]`. Answer `y` (an `expect`/`line y` step when scripted).
  - For an image made some other way (a host tool, `truncate`), run `set rl1 badblock` once
    after attaching and answer `y`. Don't leave that line in the .ini, or it asks on every boot.
  - After `INITIALIZE`, an RL02 shows 20381–20382 free blocks.
- Initializing and changing a volume ID (`/V`) ask "Are you sure?". Answer `Y` in a
  `simh_run.py` step, or add `/Y` (no query, §6.3.12) where the option allows it.

Details that trip people up *(verified)*:
- **File names are at most 6 characters plus a 3-character type**, using only Radix-50 characters
  (A–Z, 0–9, $). `PATCHED.MAC` gives `?CSI-F-Invalid command` or `?KMON-F-Error in file spec`.
- **Dates**: KMON options take `dd:mmm:yy`, e.g. `COPY/SINCE:1:JAN:84`. `/SINCE:1-JAN-84` gives
  `?KMON-F-Invalid command`. In CSI options, put decimal points on the numbers: `/I:1.:JAN:84.`.
  PIP `/C:date` matches exactly that date, `/I` means on or after it (SINCE), and `/J` means
  before it.
- **DUP**: the directory segment count is `/N:n` (`INITIALIZE/SEGMENTS:n`). `/Z:n` means n *extra
  words per directory entry*, not segments.
- **LIBR**: the MODULE column of a listing is filled only if the library was built with `/N`
  (`*UTLIB/N=MODA,MODB`); KMON LIBRARY has no option for that.
- **KMON `DELETE`** accepts at most 6 file specifications per command (`?KMON-F-Too many files`).
- KMON can produce an SLP file directly: `DIFFERENCES/SLP:PATCH.SLP OLD.MAC NEW.MAC`.

Patching sources with SRCCOM + SLP:
```
.R SRCCOM   *,PATCH.SLP=OLD.TXT,NEW.TXT     note the leading comma (no listing file)
.R SLP      *OUT.TXT=OLD.TXT,PATCH.SLP/A    /A = no audit trail
```
- Without /A, SLP appends `;**NEW**` / `;**-1` audit-trail comments to changed lines, so the
  result is not identical to NEW. With /A, `DIFFERENCES OUT.TXT NEW.TXT` reports
  `?SRCCOM-I-No differences found` *(verified)*.
- SRCCOM needs old and new in that order when it writes an SLP file. Wildcards don't work there.

Debugging with ODT:
```
.LINK/DEBUG MAIN,MODA,MODB      links ODT in; RUN starts in ODT
.RUN MAIN
 ODT V05.08
*1000;B                         breakpoint at 1000
*1000;G                         go from 1000  ->  "B0;001000"
*$0/007216                      examine R0 ($0..$7 = R0..PC, $S = PS); RETURN closes
*;P                             proceed
```
`20-odt.md` covers the rest: single-instruction mode (`;1S` on, then `n;P` steps n
instructions, `;S` off), word/byte open `/` and `\`, searches `r;W` (word) and `r;E` (effective
address), offsets `r;O`, relocation registers.

Logical disks:
```
.CREATE LDISK.DSK/ALLOCATE:200
.MOUNT LD0: DK:LDISK.DSK        ->  SHOW SUBSET: "LD0 is DL0:LDISK.DSK[200.]"
.INITIALIZE/NOQUERY LD0:
.COPY A.TXT LD0:   /  .DIR LD0:  /  .DISMOUNT LD0:
```
In one test, `LOAD LD` before `MOUNT` followed by `INITIALIZE LD0:` **halted the system**
(SIMH `HALT instruction`). The same sequence without `LOAD LD` worked. Don't `LOAD LD` in
scripts unless you need it.

## Working style

- Prefer KMON commands when explaining to a user. Give the `R util` / CSI form when they're in
  a utility, writing an indirect command file, or the option has no KMON equivalent (marked `*`
  in the Appendix B table).
- When you have a simulator available, run the command (simh-pdp11's `rt11_do.py` for KMON
  commands; `simh_run.py` steps `line R PIP` / `expect ^\*` / `line …` / `send \x03` for CSI
  sessions) instead of predicting its output. Work on copies of disk images.
- Cite the chapter/section (`SUM §13.4.3 PIP /U`). Point out V5.1-manual vs V5.3-system
  differences when something doesn't match (the V5.3 utilities report V05.03 versions, LINK
  V08.10, ODT V05.08).
