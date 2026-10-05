#!/usr/bin/env python3
"""simh_run.py - run SIMH PDP-11 (v3.x) unattended under a pseudo-terminal, with
expect/send scripting, a hard timeout, and a clean shutdown.

Why: SIMH 3.9 has no EXPECT/SEND commands, and when its stdin is a pipe the
console read() blocks the whole simulator (and EOF at the sim> prompt loops
forever). Running it on a pty avoids both problems and lets a script type at
RT-11 and wait for prompts.

Usage:
  simh_run.py [options] CONFIG.ini [STEPS ...]
  simh_run.py [options] CONFIG.ini --steps steps.txt

Steps (given as arguments or one per line in a file; '#' starts a comment line):
  expect REGEX     wait until REGEX (Python re, MULTILINE) appears in new console output.
                   Anchor prompts on both ends, e.g. 'expect ^\\.$' for RT-11 (a match at
                   the very end of output is accepted only after 0.3 s of silence)
  line TEXT        type TEXT followed by CR   (RT-11 and most DEC OSes want CR, not LF)
  send TEXT        type TEXT exactly; escapes \\r \\n \\t \\e \\xNN are honoured
  wru              type ^E (the SIMH interrupt char) and wait for the sim> prompt
  sim CMD          ^E, then run SIMH command CMD at sim> (simulation stays stopped;
                   follow with 'sim cont' to resume)
  sleep SECONDS    pause
  timeout SECONDS  per-step timeout for following expects (default 30)
  exit             stop the simulator (^E + EXIT) - done automatically at the end

Options:
  --sim PATH       simulator binary (default: $SIMH_PDP11, else simh-pdp11, pdp11 on PATH,
                   /opt/local/bin/simh-pdp11, /usr/local/bin/pdp11)
  --timeout N      overall wall-clock limit in seconds (default 300)
  --log FILE       write the full transcript to FILE
  --char-delay S   delay between typed characters (default 0.01; raise if the guest drops input)
  --quiet          don't echo the transcript to stdout
  --cwd DIR        run the simulator in DIR (relative paths in the .ini resolve there)

Exit status: 0 ok, 1 an expect timed out / overall timeout, 2 simulator not found,\n4 an ASSERT in the command file failed.
The transcript has CRs stripped so it reads cleanly.
"""
import argparse, os, re, select, shutil, signal, subprocess, sys, time

SIM_PROMPT = re.compile(r"(?m)^sim> ?$|sim> $")


def find_sim(explicit=None):
    cands = [explicit, os.environ.get("SIMH_PDP11"), shutil.which("simh-pdp11"), shutil.which("pdp11"),
             "/opt/local/bin/simh-pdp11", "/usr/local/bin/simh-pdp11", "/usr/local/bin/pdp11", "/usr/bin/pdp11"]
    for c in cands:
        if c and os.path.isfile(c) and os.access(c, os.X_OK):
            return c
    return None


def unescape(s):
    return (s.encode("latin-1").decode("unicode_escape")
            .replace("\\e", "\x1b"))


class Session:
    def __init__(self, sim, ini, cwd=None, log=None, quiet=False, char_delay=0.01, total=300):
        import pty
        self.master, slave = pty.openpty()
        def make_ctty():
            # New session with the pty as controlling terminal, so SIMH's ^E (it sets
            # VINTR=^E) is delivered as SIGINT and actually stops the simulation.
            import fcntl, termios
            os.setsid()
            fcntl.ioctl(0, termios.TIOCSCTTY, 0)
        self.proc = subprocess.Popen([sim, ini], stdin=slave, stdout=slave, stderr=slave,
                                     cwd=cwd, close_fds=True, preexec_fn=make_ctty)
        os.close(slave)
        self.buf = ""          # all output
        self.mark = 0          # position after last successful expect
        self.log = open(log, "w") if log else None
        self.quiet = quiet
        self.char_delay = char_delay
        self.deadline = time.time() + total
        self.step_timeout = 30

    def _pump(self, wait):
        r, _, _ = select.select([self.master], [], [], wait)
        if not r:
            return True
        try:
            data = os.read(self.master, 65536)
        except OSError:
            return False
        if not data:
            return False
        txt = data.decode("latin-1").replace("\r", "")
        self.buf += txt
        if self.log:
            self.log.write(txt); self.log.flush()
        if not self.quiet:
            sys.stdout.write(txt); sys.stdout.flush()
        return True

    def alive(self):
        return self.proc.poll() is None

    def expect(self, pattern, timeout=None, settle=0.3):
        """Wait for pattern in output produced since the last expect.

        A match that ends exactly at the end of the buffer (e.g. a prompt '^\\.$') is
        only accepted once no further output has arrived for `settle` seconds: the
        guest sends text in arbitrary chunks, so '.' may be the start of '.TYPE ...'.
        """
        rx = re.compile(pattern, re.M) if isinstance(pattern, str) else pattern
        end = min(time.time() + (timeout or self.step_timeout), self.deadline)
        while True:
            m = rx.search(self.buf, self.mark)
            if m and m.end() == len(self.buf) and settle and self.alive():
                quiet_until = time.time() + settle
                n = len(self.buf)
                while time.time() < quiet_until and len(self.buf) == n:
                    if not self._pump(0.05):
                        break
                if len(self.buf) != n:
                    continue          # more output arrived - re-evaluate
            if m:
                self.mark = m.end()
                return m
            if time.time() > end:
                raise TimeoutError("timed out waiting for %r" % rx.pattern)
            if not self._pump(0.05) and not self.alive():
                m = rx.search(self.buf, self.mark)
                if m:
                    self.mark = m.end(); return m
                raise EOFError("simulator exited while waiting for %r" % rx.pattern)

    def send(self, text):
        for ch in text:
            os.write(self.master, ch.encode("latin-1"))
            if self.char_delay:
                time.sleep(self.char_delay)
            self._pump(0)

    def line(self, text):
        self.send(text + "\r")

    def wru(self):
        self.send("\x05")
        self.expect(SIM_PROMPT, 10)

    def sim(self, cmd):
        if not SIM_PROMPT.search(self.buf[-12:]):
            self.wru()
        self.line(cmd)
        if cmd.strip().lower().split()[:1] in (["cont"], ["co"], ["go"], ["run"], ["boot"], ["bo"], ["ru"]):
            return
        if cmd.strip().lower() in ("exit", "quit", "bye"):
            return
        self.expect(SIM_PROMPT, 30)

    def drain(self, secs=0.3):
        end = time.time() + secs
        while time.time() < end and self._pump(0.05):
            pass

    def at_prompt(self):
        return self.buf.rstrip(" ").endswith("sim>")

    def _kill(self, sig):
        # killpg fails with EPERM (macOS) or ESRCH when the group leader is exiting or a
        # zombie; the process is then gone or going, so signal it directly as a fallback
        try:
            os.killpg(self.proc.pid, sig)
        except (PermissionError, ProcessLookupError):
            try:
                self.proc.send_signal(sig)
            except OSError:
                pass

    def close(self):
        self.drain(0.3)
        if self.alive() and "Goodbye" not in self.buf[-40:]:
            try:
                self.drain(0.2)
                if not self.at_prompt():
                    self.send("\x05")
                    for _ in range(20):
                        self._pump(0.05)
                        if self.at_prompt():
                            break
                self.send("exit\r")
                for _ in range(40):
                    if not self.alive():
                        break
                    self._pump(0.05)
            except OSError:
                pass
        # after "Goodbye" SIMH is already on its way out - give it a moment to be reaped
        for _ in range(20):
            if not self.alive():
                break
            self._pump(0.05)
        if self.alive():
            self._kill(signal.SIGTERM)
            time.sleep(0.5)
            if self.alive():
                self._kill(signal.SIGKILL)
        self.drain(0.2)
        if self.log:
            self.log.close()


def parse_steps(args):
    steps = []
    for raw in args:
        raw = raw.rstrip("\n")
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        verb, _, rest = raw.strip().partition(" ")
        steps.append((verb.lower(), rest))
    return steps


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("ini")
    p.add_argument("steps", nargs="*")
    p.add_argument("--steps", dest="stepfile")
    p.add_argument("--sim")
    p.add_argument("--timeout", type=float, default=300)
    p.add_argument("--log")
    p.add_argument("--char-delay", type=float, default=0.01)
    p.add_argument("--quiet", action="store_true")
    p.add_argument("--cwd")
    a = p.parse_args()
    sim = find_sim(a.sim)
    if not sim:
        print("simh_run: no PDP-11 simulator found (set --sim or $SIMH_PDP11)", file=sys.stderr)
        sys.exit(2)
    lines = list(a.steps)
    if a.stepfile:
        lines += open(a.stepfile).read().splitlines()
    steps = parse_steps(lines)
    s = Session(sim, a.ini, cwd=a.cwd, log=a.log, quiet=a.quiet, char_delay=a.char_delay, total=a.timeout)
    rc = 0
    try:
        for verb, arg in steps:
            if verb == "expect":
                s.expect(arg)
            elif verb == "line":
                s.line(unescape(arg))
            elif verb == "send":
                s.send(unescape(arg))
            elif verb == "wru":
                s.wru()
            elif verb == "sim":
                s.sim(arg)
            elif verb == "sleep":
                end = time.time() + float(arg)
                while time.time() < end:
                    s._pump(0.05)
            elif verb == "timeout":
                s.step_timeout = float(arg)
            elif verb == "exit":
                break
            else:
                raise SystemExit("unknown step: %s %s" % (verb, arg))
        if not steps:   # no script: run until SIMH exits, drops to sim> (ini finished
                        # without EXIT, or ASSERT failed), or the overall timeout
            while s.alive() and time.time() < s.deadline:
                s._pump(0.1)
                if s.at_prompt():
                    s.drain(0.3)
                    if s.at_prompt():
                        print("\nsimh_run: SIMH is at the sim> prompt (command file ended without EXIT,"
                              " or a command aborted it) - exiting", file=sys.stderr)
                        break
            else:
                if s.alive():
                    print("\nsimh_run: overall timeout reached", file=sys.stderr)
                    rc = 1
        if "Assertion failed" in s.buf:
            print("simh_run: an ASSERT failed", file=sys.stderr)
            rc = rc or 4
    except (TimeoutError, EOFError) as e:
        print("\nsimh_run: %s" % e, file=sys.stderr)
        print("simh_run: last output was:\n" + s.buf[-600:], file=sys.stderr)
        rc = 1
    finally:
        s.close()
    sys.exit(rc)


if __name__ == "__main__":
    main()
