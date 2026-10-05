#!/usr/bin/env python3
"""bare_run.py - assemble (optional) and run a stand-alone PDP-11 program in SIMH,
no operating system. Prints the console output and the registers when it halts.

  bare_run.py prog.mac  [--cpu 11/70] [--timeout 20] [--input "text\\r"] [--keep]
  bare_run.py prog.lda  ...          (absolute-loader / paper-tape image, e.g. from RT-11 LINK/LDA)

Program requirements: absolute code (.ASECT, or relocatable code linked/loaded at
1000), a transfer address on .END, and a HALT when done (otherwise --timeout stops it).
Console I/O must be done directly on the DL11 registers (177560-177566) - there is
no OS, so no .PRINT/.TTYOUT.

.mac -> .lda needs the macro11 cross-assembler and a pclink11 linker with the /LDA
option (absolute-loader output). Located via
$MACRO11 / $PCLINK11, then PATH. If they're missing, assemble inside RT-11 instead
(MACRO X / LINK/LDA X, see references/rt11-on-simh.md) and pass the .lda here.

Exit status: 0 halted normally, 1 timeout or error, 2 tools/simulator missing.
"""
import argparse, os, re, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from simh_run import Session, find_sim  # noqa: E402


def find_tool(env, names, extra):
    c = os.environ.get(env)
    if c and os.path.exists(c):
        return c
    for n in names:
        w = shutil.which(n)
        if w:
            return w
    for e in extra:
        e = os.path.expanduser(e)
        if os.path.exists(e):
            return e
    return None


def assemble(src, work):
    m11 = find_tool("MACRO11", ["macro11"], ["~/macro11/macro11", "/usr/local/bin/macro11"])
    lnk = find_tool("PCLINK11", ["pclink11"], ["/usr/local/bin/pclink11"])
    if not m11 or not lnk:
        print("bare_run: need macro11 and pclink11 (set $MACRO11 / $PCLINK11), or build the .lda in RT-11 "
              "(MACRO X then LINK/LDA X) and pass it here", file=sys.stderr)
        sys.exit(2)
    base = os.path.join(work, os.path.splitext(os.path.basename(src))[0])
    r = subprocess.run([m11, "-o", base + ".obj", "-l", base + ".lst", src],
                       capture_output=True, text=True, timeout=30)
    errs = [l for l in (r.stdout + r.stderr).splitlines() if "ERROR" in l]
    if errs or r.returncode:
        print("bare_run: assembly failed:\n  " + "\n  ".join(errs or [r.stderr]), file=sys.stderr)
        print("listing: " + base + ".lst", file=sys.stderr)
        sys.exit(1)
    # /LDA writes absolute-loader blocks for the loaded bytes plus the transfer-address block
    lda = base + ".lda"
    r = subprocess.run([lnk, os.path.basename(base) + ".obj", "/LDA", "/EXECUTE:" + os.path.basename(lda)],
                       cwd=work, capture_output=True, text=True, timeout=30)
    if r.returncode or "SUCCESS" not in r.stdout or not os.path.exists(lda):
        print("bare_run: pclink11 /LDA failed (needs a pclink11 with the /LDA option):\n"
              + r.stdout[-2000:] + r.stderr, file=sys.stderr)
        sys.exit(1)
    return lda


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("program")
    p.add_argument("--cpu", default="11/70")
    p.add_argument("--mem", default=None, help="e.g. 256K")
    p.add_argument("--timeout", type=float, default=20)
    p.add_argument("--input", help="text to type on the console after start (escapes like \\r allowed)")
    p.add_argument("--start", help="octal start address (default: transfer address from the .END)")
    p.add_argument("--sim")
    p.add_argument("--keep", action="store_true", help="keep the work dir (lst, obj, lda, ini)")
    a = p.parse_args()

    sim = find_sim(a.sim)
    if not sim:
        print("bare_run: no PDP-11 simulator found (set --sim or $SIMH_PDP11)", file=sys.stderr)
        sys.exit(2)
    work = tempfile.mkdtemp(prefix="bare_run_")
    prog = os.path.abspath(a.program)
    lda = assemble(prog, work) if prog.lower().endswith(".mac") else prog
    ini = os.path.join(work, "run.ini")
    with open(ini, "w") as f:
        f.write("set cpu %s\n" % a.cpu)
        if a.mem:
            f.write("set cpu %s\n" % a.mem)
        f.write("load %s\n" % lda)
        f.write("go%s\n" % (" " + a.start if a.start else ""))
        f.write("echo ==REGS==\nex r0-r5,sp,pc,psw\nexit\n")
    s = Session(sim, ini, cwd=work, quiet=True, total=a.timeout + 10)
    rc = 0
    try:
        if a.input:
            s.drain(0.5)
            s.send(a.input.encode("latin-1").decode("unicode_escape"))
        try:
            s.expect(r"==REGS==", a.timeout)
            s.expect(r"(?m)^PSW:.*$", 5)
        except (TimeoutError, EOFError):
            print("bare_run: program did not halt within %ss - stopped it" % a.timeout, file=sys.stderr)
            rc = 1
            # ^E stops the GO; SIMH then carries on with the rest of run.ini (echo/ex/exit)
            s.send("\x05")
            s.expect(r"==REGS==", 10)
            s.expect(r"(?m)^PSW:.*$", 5)
    finally:
        s.close()
    out = s.buf
    out = re.sub(r"(?m)^PDP-11 simulator V.*\n|^Disabling \w+\n|^(sim> )?\x05?exit\n?|^Goodbye\n?|^==REGS==\n", "", out)
    print(out.strip())
    if a.keep:
        print("\n(work dir: %s)" % work)
    else:
        shutil.rmtree(work, ignore_errors=True)
    if re.search(r"(?m)^(Trap stack push abort|Trap vector abort|Stack|Odd address|Nonexistent memory|Wait state)", out):
        rc = rc or 1
    sys.exit(rc)


if __name__ == "__main__":
    main()
