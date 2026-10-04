#!/usr/bin/env python3
"""rt11_do.py - boot RT-11 in SIMH, run keyboard-monitor commands, shut down.

  rt11_do.py CONFIG.ini "MACRO HELLO/LIST" "LINK HELLO" "RUN HELLO"
  rt11_do.py CONFIG.ini --date 02-OCT-99 --commands cmds.txt --log run.log

CONFIG.ini must attach the system disk and end with BOOT (no EXIT after it).
Each command is typed after the RT-11 '.' prompt; the script waits for the next
'.' prompt (per-command timeout --cmd-timeout, default 120 s), then exits SIMH
cleanly with ^E / EXIT so the disk image is consistent.

Exit status: 0 all commands finished; 1 timeout / unexpected stop (the tail of
the transcript is printed to stderr); 2 simulator not found; 3 the disk is an
untouched RT-11 distribution disk sitting in its auto-install dialogue (run the
first-boot procedure in references/rt11-on-simh.md once to make it a working disk).

Output: the transcript (CRs removed) on stdout unless --quiet; with --log also
to a file. RT-11 error messages (?xxx-F-, ?xxx-E-, ?xxx-W-) are summarized at
the end on stderr, so callers can grep for '^?' cheaply.
"""
import argparse, os, re, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simh_run import Session, find_sim  # noqa: E402

PROMPT = re.compile(r"(?m)^\.$")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("ini")
    p.add_argument("commands", nargs="*")
    p.add_argument("--commands", dest="cmdfile", help="file with one RT-11 command per line")
    p.add_argument("--date", help="set RT-11 date first, e.g. 02-OCT-99 (V5.3 cannot take years > 1999)")
    p.add_argument("--sim")
    p.add_argument("--boot-timeout", type=float, default=120)
    p.add_argument("--cmd-timeout", type=float, default=120)
    p.add_argument("--timeout", type=float, default=1800, help="overall limit")
    p.add_argument("--log")
    p.add_argument("--quiet", action="store_true")
    p.add_argument("--char-delay", type=float, default=0.01)
    p.add_argument("--cwd")
    a = p.parse_args()

    sim = find_sim(a.sim)
    if not sim:
        print("rt11_do: no PDP-11 simulator found (set --sim or $SIMH_PDP11)", file=sys.stderr)
        sys.exit(2)
    cmds = list(a.commands)
    if a.cmdfile:
        cmds += [l.rstrip("\n") for l in open(a.cmdfile) if l.strip() and not l.startswith("#")]
    if a.date:
        cmds.insert(0, "DATE " + a.date)

    s = Session(sim, a.ini, cwd=a.cwd, log=a.log, quiet=a.quiet, char_delay=a.char_delay, total=a.timeout)
    rc = 0
    try:
        m = s.expect(re.compile(r'(?m)^\.$|Press the "RETURN" key when ready'), a.boot_timeout)
        if m.group(0) != ".":
            print("\nrt11_do: this is an RT-11 distribution disk waiting in the auto-install dialogue.\n"
                  "Do the one-time first-boot procedure (references/rt11-on-simh.md) on a COPY of the image.",
                  file=sys.stderr)
            rc = 3
        else:
            for c in cmds:
                s.line(c)
                s.expect(PROMPT, a.cmd_timeout)
    except (TimeoutError, EOFError) as e:
        print("\nrt11_do: %s" % e, file=sys.stderr)
        print("rt11_do: last output:\n" + s.buf[-800:], file=sys.stderr)
        rc = 1
    finally:
        s.close()
    errs = re.findall(r"(?m)^\?[A-Z0-9]+-[FEWU]-.*$", s.buf)
    if errs:
        print("rt11_do: RT-11 reported:\n  " + "\n  ".join(errs), file=sys.stderr)
    sys.exit(rc)


if __name__ == "__main__":
    main()
