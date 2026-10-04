---
name: simh-pdp11
description: Configure and drive the SIMH v3.9 PDP-11 simulator (simh-pdp11 / pdp11) - write .ini machine configurations, boot and script RT-11 (assemble, link, run, move files in/out of RT-11 disk images), and run stand-alone MACRO-11 programs with captured console output and register dumps. Use whenever the user mentions SIMH, simh-pdp11, a PDP-11 emulator/simulator, .ini/.dsk/.lda/.rl02/.rk05 images, booting RT-11/RSX/RSTS, or wants PDP-11 code actually executed - even if they only say "run this on the PDP-11" or "try it in the emulator".
---

# SIMH PDP-11 (v3.9)

The user's simulator is **SIMH V3.9-0**, installed as `/opt/local/bin/simh-pdp11` (MacPorts).
Other installs call it `pdp11`. The bundled scripts find it automatically (`$SIMH_PDP11`,
then `simh-pdp11`/`pdp11` on PATH, then common locations); pass `--sim PATH` if not.

v3.9 is older than the "SIMH v4 / open-simh" most web examples assume. In particular it has
**no EXPECT, SEND, GOTO, IF, SET ENVIRONMENT, RUNLIMIT** — don't write them into .ini files.
Its scripting is limited to DO files with `%1..%9`, ECHO, ASSERT and `!` (host shell).
Interaction with a running guest is done from outside, by `scripts/simh_run.py`.

## Scripts (in `scripts/`, Python 3 stdlib only, macOS + Linux)

| Script | Use it to |
| --- | --- |
| `simh_run.py CONFIG.ini [steps…]` | Run SIMH under a pty with a hard timeout; `expect REGEX` / `line TEXT` / `send TEXT` / `wru` / `sim CMD` / `sleep N` steps; transcript to stdout and `--log`; always shuts SIMH down cleanly. Exit 0 ok, 1 timeout, 2 no simulator, 4 an ASSERT failed. |
| `rt11_do.py CONFIG.ini "CMD" "CMD"…` | Boot RT-11, type each keyboard-monitor command at the `.` prompt, wait for the next prompt, exit. `--date 02-OCT-99`, `--commands file`, `--log`. Summarizes `?xxx-E-` messages on stderr. Exit 3 = distribution disk still in its install dialogue. |
| `rt11fs.py ls/get/put/rm/init/info IMAGE …` | Read and write files on RT-11 disk images from the host (no PUTR needed); create empty RT-11 data volumes. |
| `bare_run.py prog.mac\|prog.lda` | Stand-alone program: assemble (macro11 + obj2bin.pl), LOAD, GO, print console output and R0–R5/SP/PC/PSW at HALT. `--input "text\r"`, `--cpu`, `--timeout`. |

Run any script with `-h` for full options.

## Why the scripts exist (don't run SIMH bare from a tool call)

These are real v3.9 behaviors, verified in its source:
- With stdin **not a terminal**, the console `read()` blocks: the simulated machine freezes
  waiting for input whenever stdin is an open pipe.
- At the `sim>` prompt, **EOF on stdin is ignored and re-prompts forever** — a config that
  doesn't end in `EXIT`, or a failed `ASSERT` (which aborts *all* nested command files), spins
  printing `sim> ` endlessly.
- `^E` (the WRU character) only stops the simulation when SIMH's terminal is its *controlling
  tty*, because SIMH maps it to SIGINT.

`simh_run.py` handles all three (pty as controlling tty, timeouts, detection of a stray `sim>`).
If you must run SIMH directly, use `simh-pdp11 file.ini < /dev/null` with `timeout`, and make
sure the .ini ends with `exit`.

## Writing .ini files

An .ini is just SIMH commands executed in order (`simh-pdp11 my.ini [args]` runs it as
`DO my.ini args`; with no argument SIMH looks for `<program-name>.ini` in the current
directory). Lines starting with `;` are comments. Typical shape:

```ini
set cpu 11/40            ; model: 11/03 04 05 20 23 23+ 24 34 40 44 45 53 60 70 73 73B 83 84 93 94
set cpu 256K             ; memory (default 256K); see Qbus/18-bit note below
set rq disabled          ; disable what you don't use: fewer surprises, faster boot
set rl0 rl02             ; drive type BEFORE attach
attach rl0 rt11-work.dsk ; paths are relative to SIMH's working directory
attach lpt printer.txt   ; printer output -> host file
boot rl0                 ; or: load prog.lda / go
exit                     ; only after a program that halts; omit after an OS boot
```

For testing small bare-only programs it makes sense to use following `bare.ini` file, where `load HELLO.LDA`
should be replaced by proper file name of the executable file in LDA format:

```ini
set cpu 11/05 64K idle
set console wru=035
set tto 8b
sh cpu
load HELLO.LDA
e pc
e -m 001000:01100
g
e sp
bye
```

Rules that bite:
- **Set types before attaching** (`set rl0 rl02`, `set rq0 rd54`, `set rk0 …`); type changes are
  refused while attached. RL defaults to AUTOSIZE.
- **Bus/memory**: Qbus CPUs (11/03, 23, 53, 73, 83, 93) disable Unibus-only devices, and 18-bit
  Qbus DMA devices (RK, HK, TM, RY) are disabled once memory exceeds 256K. RK05 kits →
  `set cpu 11/70` or 11/40. `show cpu iospace` shows what's actually configured.
- **Default build state** here: CPU 11/23, 56K, TTI 7-bit, TTO 8-bit RL autosize, CLK 60 Hz,
  XQ (Ethernet) unsupported in this build ("Disabling XQ" on a Unibus model is normal).
- **Odd devices clash**: TM11 and TS11 share addresses — enable one. Setting an explicit
  `ADDRESS` turns off autoconfiguration for the whole system.
- `attach` of an existing output file (LPT, PTP) rewrites from byte 0 **without truncating** —
  put `! rm -f printer.txt` before it.
- **Idle**: `set cpu idle` doesn't recognize RT-11's or UNIX's idle loop; for long interactive
  sessions use `set throttle 50%`, never in scripted runs.
- For an interactive session over telnet: `set console telnet=2323` (it listens immediately; the
  console I/O goes to whoever connects).

Templates (tested):
- `assets/rt11-rl02.ini` (RT-11 on RL02 + data drive + printer),
- `assets/bare-metal.ini` (LOAD %1 / GO / dump registers / EXIT),
- `assets/pdp11-05.ini` (PDP-11/05, LOAD %1 / GO / BYE ).

Full command syntax: `references/simh-v39-commands.md`. Every PDP-11 device, its SET options,
registers and boot support: `references/pdp11-simulator.md` (grep for the device, e.g. `RQ`).

## Running RT-11

Read `references/rt11-on-simh.md` before working with RT-11 — it has the tested recipes. Short
version:

1. Work on a **copy** of the image. A distribution disk (e.g. RT-11 V5.3 `rtv53_rl.dsk`)
   first needs the one-time first boot: `simh_run.py --timeout 180 rt11-rl02.ini --steps assets/rt11v53-firstboot.steps`.
2. `rt11fs.py put rt11-work.dsk prog.mac` — **only while SIMH is not running** with that image
   attached.
3. `rt11_do.py --date 02-OCT-99 rt11-rl02.ini "MACRO PROG/LIST" "LINK PROG" "RUN PROG"`
4. `rt11fs.py get rt11-work.dsk PROG.LST` and read the listing for errors.

RT-11 V5.3 rejects dates after 1999 (`?KMON-F-Invalid date`). For programs that prompt for
input, use `simh_run.py` steps (`expect`, `line`) instead of `rt11_do.py`.
For writing the MACRO-11 code itself (syntax, RT-11 programmed requests), use the **macro11**
skill if it's available.

## Running stand-alone (bare-metal) programs

No OS: the program talks to the DL11 console registers (RCSR 177560, RBUF 177562,
XCSR 177564, XBUF 177566; ready = bit 7) and ends with `HALT`. Use absolute code
(`.ASECT` + `.=1000`, or code linked at 1000) and give `.END START`.

```sh
python3 scripts/bare_run.py prog.mac --cpu 11/05 [--input 'abc\r'] [--timeout 20]
```
Needs `macro11`, `pclink11` and `obj2bin.pl`:
- github.com/andpp/macro11; `make` builds macro11;
- github.com/andpp/pclink11; `make` builds pclink11;
- obj2bin is Perl.
Without them, build the .lda inside RT-11 with `MACRO X` + `LINK/LDA X`, copy it out with
`rt11fs.py get`, and pass the .lda. SIMH's `LOAD` takes only the absolute-loader (paper-tape)
format, sets PC from the end block, and does not start the program — `GO` does.

Check presence of `macro11`, `pclink11`, `obj2bin.pl` in `PATH` env or/and in `/usr/local/bin`

When a program doesn't halt, `^E` stops it and SIMH continues with the next line of the .ini
(that's how `bare_run.py` still gets its register dump after a timeout).

## Debugging at the sim> level

```ini
break 1012                 ; execution breakpoint (BREAK 1012;EX R0 runs actions on hit)
go                         ; stops with "Breakpoint, PC: 001012 (...)"
ex r0-r5,sp,pc,psw         ; registers
ex -m 1000-1030            ; disassemble; -a ASCII bytes, -c 2-char words, -d decimal
step 3                     ; single-step
d 1000 012700              ; deposit (octal)
d -m 1000 MOV #1,R0        ; symbolic deposit (assembles in place, here 2 words)
eval MOV #1,R0             ; assemble one instruction -> octal words
set cpu history=64         ; minimum 64; then: show cpu history=20
nobreak 1012
```
`ex` output goes to a file with `ex @file.txt …`. Register names and stop conditions (trap
stops, `STOP_TRAPS`, WAIT with no I/O) are in `references/pdp11-simulator.md` §2.1.

## Reporting back

When you run something for the user, show the relevant part of the console transcript (not the
whole boot banner), the exact .ini you used, and any RT-11 `?…-E-` / `?…-F-` messages. If you
changed a disk image, say which one and what files you put/got.
