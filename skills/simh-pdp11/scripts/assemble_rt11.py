#!/usr/bin/env python3
"""assemble_rt11.py - assemble a MACRO-11 file for RT-11 using macro11 cross-assembler

Usage: assemble_rt11.py prog.mac [--cpu 11/70] [--input "text\\r"] [--timeout 20] [--keep]

This script:
1. Assembles with macro11 (no -rt11 flag - use -m SYSMAC.SML instead)
2. Uses pclink11 to link for RT-11 .SAV format
3. If bare-metal (--bare), links to .LDA with pclink11 /LDA instead
SYSMAC.SML (for .MCALL) is taken from $SYSMAC, the current directory or the project root.

Exit status: 0 success, 1 error
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

def find_sysmac():
    # $SYSMAC, then the current directory, then the project root (4 levels above scripts/)
    here = os.path.dirname(os.path.abspath(__file__))
    for c in (os.environ.get("SYSMAC"), "SYSMAC.SML",
              os.path.join(here, "..", "..", "..", "..", "SYSMAC.SML")):
        if c and os.path.exists(c):
            return os.path.abspath(c)
    return None

def assemble(src, work):
    m11 = find_tool("MACRO11", ["macro11"], ["~/macro11/macro11", "/usr/local/bin/macro11"])
    if not m11:
        print("assemble_rt11: need macro11 (set $MACRO11)", file=sys.stderr)
        sys.exit(1)

    base = os.path.join(work, os.path.splitext(os.path.basename(src))[0])

    # Check if .MCALLs are present
    with open(src) as f:
        content = f.read()
    use_rt11 = '.MCALL' in content

    # Assemble
    cmd = [m11, "-o", base + ".obj", "-l", base + ".lst", src]
    if use_rt11:
        # RT-11 program with .MCALL - include SYSMAC.SML
        sysmac = find_sysmac()
        if not sysmac:
            print("assemble_rt11: .MCALL needs SYSMAC.SML (set $SYSMAC)", file=sys.stderr)
            sys.exit(1)
        cmd += ["-m", sysmac]

    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    errs = [l for l in (r.stdout + r.stderr).splitlines() if "ERROR" in l or "***" in l]
    if errs or r.returncode:
        print("assemble_rt11: assembly failed:\n  " + "\n  ".join(errs or [r.stderr]), file=sys.stderr)
        print("listing: " + base + ".lst", file=sys.stderr)
        sys.exit(1)
    return base + ".obj"

def link(obj, work, bare=False):
    """Link with pclink11: RT-11 .SAV, or with bare=True an absolute-loader .LDA (/LDA)."""
    lnk = find_tool("PCLINK11", ["pclink11"], ["~/macro11/pclink11", "/usr/local/bin/pclink11"])
    if not lnk:
        print("assemble_rt11: need pclink11 (set $PCLINK11)", file=sys.stderr)
        sys.exit(1)

    name = os.path.splitext(os.path.basename(obj))[0] + (".lda" if bare else ".sav")
    out = os.path.join(work, name)
    cmd = [lnk, os.path.basename(obj), "/EXECUTE:" + name] + (["/LDA"] if bare else [])
    r = subprocess.run(cmd, cwd=work, capture_output=True, text=True, timeout=30)
    errs = [l for l in (r.stdout + r.stderr).splitlines() if "ERROR" in l]
    if errs or r.returncode or "SUCCESS" not in r.stdout or not os.path.exists(out):
        print("assemble_rt11: link failed:\n  " + "\n  ".join(errs or [r.stdout[-2000:] + r.stderr]),
              file=sys.stderr)
        sys.exit(1)
    return out

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("program")
    p.add_argument("--cpu", default="11/70")
    p.add_argument("--mem", default=None, help="e.g. 256K")
    p.add_argument("--timeout", type=float, default=20)
    p.add_argument("--input", help="text to type on the console after start (escapes like \\r allowed)")
    p.add_argument("--start", help="octal start address (default: transfer address from the .END)")
    p.add_argument("--sim")
    p.add_argument("--keep", action="store_true", help="keep the work dir (lst, obj, lda)")
    p.add_argument("--bare", action="store_true", help="build bare-metal .LDA instead of RT-11 .SAV")
    a = p.parse_args()

    sim = find_sim(a.sim)
    work = tempfile.mkdtemp(prefix="assemble_rt11_")
    prog = os.path.abspath(a.program)
    
    # Assemble and link (.LDA for bare metal, .SAV for RT-11)
    obj = assemble(prog, work)
    lda = link(obj, work, bare=a.bare)
    
    print(f"Assembled: {obj}")
    print(f"Linked: {lda}")
    
    # Run with simh_run if available and sim provided
    if sim:
        if a.bare:
            ini = os.path.join(work, "run.ini")
            with open(ini, "w") as f:
                f.write(f"set cpu {a.cpu}\n")
                if a.mem:
                    f.write(f"set cpu {a.mem}\n")
                f.write(f"load {lda}\n")
                f.write(f"go{' ' + a.start if a.start else ''}\n")
                f.write("echo ==REGS==\nex r0-r5,sp,pc,psw\nexit\n")
            s = Session(sim, ini, cwd=work, quiet=True, total=a.timeout + 10)
            try:
                if a.input:
                    s.drain(0.5)
                    s.send(a.input.encode("latin-1").decode("unicode_escape"))
                s.expect(r"==REGS==", a.timeout)
                s.expect(r"(?m)^PSW:.*$", 5)
            except (TimeoutError, EOFError):
                print(f"assemble_rt11: program did not halt within {a.timeout}s - stopped it", file=sys.stderr)
                s.send("\x05")
                s.expect(r"==REGS==", 10)
                s.expect(r"(?m)^PSW:.*$", 5)
            finally:
                s.close()
            out = s.buf
        else:
            print("assemble_rt11: RT-11 .SAV execution not yet implemented with simh_run", file=sys.stderr)
            out = ""
    else:
        out = ""
    
    if a.keep:
        print(f"\n(work dir: {work})")
    else:
        shutil.rmtree(work, ignore_errors=True)
    
    if out:
        import re
        out = re.sub(r"(?m)^PDP-11 simulator V.*\n|^Disabling \w+\n|^(sim> )?\x05?exit\n?|^Goodbye\n?|^==REGS==\n", "", out)
        print(out.strip())

if __name__ == "__main__":
    main()
