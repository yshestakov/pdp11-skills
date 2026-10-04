# RT-11 on SIMH PDP-11 v3.9 — tested recipes

Everything here was run end-to-end on SIMH V3.9-0 with the RT-11 V5.3 RL02
distribution image (`rtv53_rl.dsk`, from the SIMH hobbyist kit `rtv53swre.tar.Z`;
10,475,520 bytes = RL02 minus its last track). Commands use the bundled scripts;
`$S` = this skill's `scripts/` directory.

## Contents
- Images you'll meet
- One-time first boot of a distribution disk
- Edit → assemble → link → run cycle
- Getting files in and out
- Data disks
- Bare-metal programs built by RT-11 (LINK/LDA)
- RT-11 + SIMH gotchas

## Images you'll meet

| Image | Device | SIMH size | Notes |
| --- | --- | --- | --- |
| `rtv53_rl.dsk` | RL02 | 10,475,520 B | RT-11 V5.3 distribution; boots RT11AI (auto-install) |
| RK05 packs | RK | 2,494,464 B | `set cpu 11/40` or similar Unibus; RK is disabled on Qbus > 256K |
| RX01/RX02 | RX/RY | 256,256 / 512,512 B | slow but common for old kits |
| MSCP (RD/RA) | RQ | any | needs DU.SYS; boot `boot rq0` |

`rt11fs.py info IMAGE` and `rt11fs.py ls IMAGE` identify a volume without booting it.
Keep the pristine distribution read-only and always work on a copy.

## One-time first boot of a distribution disk

A V5.3 distribution disk boots into an IND dialogue ("Press the RETURN key…",
"Do you want to use the automatic installation procedure?"). Answering **NO** makes
it copy the RT11FB bootstrap onto the disk and reboot to the normal `.` prompt;
from then on that copy boots straight to RT11FB (which runs STARTF.COM, which just
types V5USER.TXT). ^C does not escape the dialogue.

```sh
cp rtv53_rl.dsk rt11-work.dsk && chmod u+w rt11-work.dsk
cp $S/../assets/rt11-rl02.ini $S/../assets/rt11v53-firstboot.steps .
python3 $S/simh_run.py --timeout 180 rt11-rl02.ini --steps rt11v53-firstboot.steps
```

`rt11_do.py` exits with status 3 and says so if it finds a disk still in this
dialogue. Other RT-11 versions/kits have different first-boot dialogues: boot once
with `simh_run.py rt11-rl02.ini 'sleep 20'` (or interactively), read the prompts,
and write a steps file the same way.

## Edit → assemble → link → run cycle

```sh
python3 $S/rt11fs.py put rt11-work.dsk hello.mac            # host -> RT-11 (LF->CRLF)
python3 $S/rt11_do.py --date 02-OCT-99 rt11-rl02.ini \
    "MACRO HELLO/LIST" "LINK HELLO/MAP" "RUN HELLO"
python3 $S/rt11fs.py get rt11-work.dsk HELLO.LST            # listing back to host
```

`rt11_do.py` waits for the `.` prompt after every command, exits SIMH cleanly, and
lists any `?MACRO-E-…` / `?LINK-W-…` style messages on stderr. Under the keyboard
monitor: `MACRO X/LIST` → X.OBJ + X.LST; `LINK X/MAP` → X.SAV + X.MAP;
`LINK/LDA X` → X.LDA (absolute loader image for bare-metal SIMH LOAD);
`MACRO X/LIST:TT:` shows the listing on the console. `R MACRO` then
`*X,X=X` is the CSI form.

Programs that read the terminal: pass their input as further commands only if they
read whole lines; for prompts use `simh_run.py` steps (`expect Name\? ` / `line Bob`).

## Getting files in and out

1. **`rt11fs.py`** (preferred) — reads/writes the image directly. SIMH must not
   have the image attached while you modify it (RT-11 keeps the directory in
   memory and will write it back over your change). Text files get CRLF/LF
   conversion by extension; `--binary` / `--text` override. Files have no byte
   length in RT-11, so binary gets come back padded to 512-byte blocks.
   File dates: undated by default because V5.3 shows years after 1999 as `-BAD-`;
   use `--date 02-OCT-99` (V5.5+ handles 2000–2099 via the age bits: `--date today`).
2. **Line printer** — `attach lpt printer.txt` in the .ini, then `PRINT X.LST` or
   `COPY X.MAC LP:` in RT-11. Do `SET LP LC` first or the handler upper-cases.
   Delete the host file before attaching (`! rm -f printer.txt` in the .ini):
   SIMH re-opens an existing file and overwrites from byte 0 *without truncating*.
3. **Paper tape** — `attach ptr in.txt` + RT-11 `COPY PC: X.MAC` (needs PC.SYS,
   reads until end of tape); `attach ptp out.txt` + `COPY X.MAC PC:`.
4. **Console capture** — `simh_run.py --log` or `SET CONSOLE LOG=file`; `TYPE X.MAC`.

## Data disks

```sh
python3 $S/rt11fs.py init data.dsk --type rl02     # empty RT-11 volume (not bootable)
python3 $S/rt11fs.py put data.dsk prog.mac
# in the .ini, before BOOT:   set rl1 rl02   /   attach rl1 data.dsk
python3 $S/rt11_do.py rt11-rl02.ini "DIR DL1:" "MACRO DL1:PROG/LIST:DL1:"
```
Types: rl01 rl02 rk05 rx01 rx02 rd51–rd54, or a block count. RT-11's own
`INIT DL1:` works too but asks for confirmation (use `INIT/NOQUERY DL1:`).

## Bare-metal programs built by RT-11 (LINK/LDA)

```sh
python3 $S/rt11_do.py rt11-rl02.ini "MACRO BARE" "LINK/LDA BARE"
python3 $S/rt11fs.py get rt11-work.dsk BARE.LDA bare.lda
python3 $S/bare_run.py bare.lda
```
Works when no cross-assembler is installed on the host.

## RT-11 + SIMH gotchas

- **Date**: RT-11 V5.3 has no TOY clock under SIMH and asks nothing at boot;
  `DATE` gives `?KMON-W-No date`. Set one (`--date 02-OCT-99`); V5.3 rejects years
  after 1999.
- **CPU choice**: 11/73 with 256K is the safe default for RL/RQ systems. Unibus
  18-bit devices (RK, HK, TM, RY) are disabled automatically on a Qbus CPU with
  more than 256K memory — use `set cpu 11/70` (Unibus) for RK05-based kits.
- **Idle**: `SET CPU IDLE` doesn't detect RT-11's idle loop (doc §2.1.1), so SIMH
  burns 100% CPU while RT-11 waits at the prompt. Use `SET THROTTLE 50%` for
  long-lived interactive sessions; leave it off for scripted runs (faster).
- **Never leave a session hanging**: always end with `^E` + `EXIT`
  (`simh_run.py`/`rt11_do.py` do this). Killing SIMH mid-write can leave the RT-11
  directory half-updated.
- **Console mode**: TTI defaults to 7B in this build; `SET TTI UC` (and TTO UC)
  makes SIMH upper-case everything, which some old programs expect.
- **Lower-case input** in your own programs needs JSW bit 40000 (TTLC$) — see
  the macro11 skill's rt11.md.
