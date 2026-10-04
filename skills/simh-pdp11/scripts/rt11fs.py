#!/usr/bin/env python3
"""rt11fs.py - read/write files on an RT-11 file-structured disk image (SIMH .dsk).

Lets you move files between the host and an RT-11 volume without running RT-11
(no PUTR, no paper tape). Works on any RT-11 volume image whose block 0 is at
file offset 0: SIMH RK05, RL01/RL02, RX01/RX02 (block-mode images), RK06/07,
RP, MSCP (RQ) images.

Usage:
  rt11fs.py ls     IMAGE                         list directory (like DIR)
  rt11fs.py get    IMAGE NAME.EXT [HOSTFILE]     copy file out (text files: CRLF->LF, trailing NUL/^Z stripped)
  rt11fs.py put    IMAGE HOSTFILE [NAME.EXT] [--date DD-MMM-YY|today]
                                                 copy file in (replaces existing; text: LF->CRLF)
  rt11fs.py rm     IMAGE NAME.EXT                delete file
  rt11fs.py init   IMAGE --type rl02|rl01|rk05|rx01|rx02|rd51|rd52|rd53|rd54|BLOCKS [--segments N]
                                                 create an empty RT-11 volume (data disk, not bootable)
  rt11fs.py info   IMAGE                         show home-block / directory summary

Options for get/put: --binary or --text override the automatic choice. Text mode is
the default for source-like extensions (.MAC .TXT .COM .CTL .LST .MAP .FOR .BAS .C .H
.DAT .INI .HLP .ANS .MEM .SML .DOC ...); .SAV .OBJ .SYS .LDA .REL etc. are binary.

RT-11 files have no byte length: `get --binary` returns whole 512-byte blocks.

IMPORTANT: never modify an image that a running simulator has ATTACHed - detach
it first (or exit SIMH). The simulator caches nothing, but RT-11 caches the
directory in memory and will overwrite your changes / corrupt the volume.
"""
import argparse, datetime, os, struct, sys

BLK = 512
R50 = " ABCDEFGHIJKLMNOPQRSTUVWXYZ$.%0123456789"   # % = RT-11 "unused" (code 035)
TEXT_EXT = {"MAC", "TXT", "COM", "CTL", "LST", "MAP", "FOR", "BAS", "C", "H",
            "DAT", "INI", "HLP", "ANS", "MEM", "SML", "DOC", "README", "CND", "SOU", "PAS", "DIR"}
E_TENT, E_MPTY, E_PERM, E_EOS, E_PROT = 0o400, 0o1000, 0o2000, 0o4000, 0o100000

SIZES = {"rk05": 4800, "rl01": 10220, "rl02": 20460, "rx01": 494, "rx02": 988,
         "rd51": 21600, "rd52": 60480, "rd53": 138672, "rd54": 311200}
# image file sizes SIMH expects (bytes) when we create a new one
IMG_BYTES = {"rk05": 2494464, "rl01": 5242880, "rl02": 10485760, "rx01": 256256, "rx02": 512512}


def r50enc(s):
    s = (s.upper() + "   ")[:3]
    v = 0
    for ch in s:
        if ch not in R50:
            raise ValueError("character %r not valid in RAD50" % ch)
        v = v * 40 + R50.index(ch)
    return v


def r50dec(w):
    return R50[w // 1600 % 40] + R50[w // 40 % 40] + R50[w % 40]


def split_name(name):
    name = os.path.basename(name).upper()
    base, _, ext = name.partition(".")
    if not base or len(base) > 6 or len(ext) > 3:
        raise ValueError("RT-11 names are 1-6 chars + up to 3-char extension: %r" % name)
    return base, ext


def enc_name(name):
    base, ext = split_name(name)
    base = base.ljust(6)
    return [r50enc(base[:3]), r50enc(base[3:]), r50enc(ext)]


def dec_name(w):
    base = (r50dec(w[0]) + r50dec(w[1])).rstrip()
    ext = r50dec(w[2]).rstrip()
    return base + "." + ext


def rt_date(spec=None):
    """RT-11 date word. spec: None -> undated (0), 'today', or DD-MMM-YY / DD-MMM-YYYY.
    Pre-V5.5 RT-11 shows years after 1999 as -BAD-, hence the undated default."""
    if not spec:
        return 0
    if spec.lower() == "today":
        d = datetime.date.today()
    else:
        dd, mon, yy = spec.upper().split("-")
        y = int(yy)
        y = y + (1900 if y >= 72 else 2000) if y < 100 else y
        d = datetime.date(y, "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split().index(mon) + 1, int(dd))
    y = d.year - 1972
    age, y = divmod(y, 32)
    return (age << 14) | (d.month << 10) | (d.day << 5) | y


def dec_date(w):
    if w == 0:
        return ""
    m, dd, y = (w >> 10) & 0o17, (w >> 5) & 0o37, (w & 0o37) + 1972 + 32 * (w >> 14)
    if not (1 <= m <= 12 and 1 <= dd <= 31):
        return "?"
    mon = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()[m - 1]
    return "%02d-%s-%d" % (dd, mon, y)


class Volume:
    def __init__(self, path, write=False):
        self.path = path
        self.f = open(path, "r+b" if write else "rb")
        hb = self.block(1)
        w = struct.unpack("<256H", hb)
        self.home = w
        self.dir_start = w[0o724 // 2] or 6
        if not (2 <= self.dir_start < 100):
            raise SystemExit("%s: home block does not look like RT-11 (dir start=%d)" % (path, self.dir_start))
        seg1 = self.read_seg(1)
        self.nsegs = seg1[0]
        self.extra = seg1[3]
        if not (1 <= self.nsegs <= 31) or self.extra % 2:
            raise SystemExit("%s: not an RT-11 directory (segments=%d extra=%d)" % (path, self.nsegs, self.extra))
        self.esize = 7 + self.extra // 2  # entry size in words

    def block(self, n, count=1):
        self.f.seek(n * BLK)
        data = self.f.read(BLK * count)
        return data.ljust(BLK * count, b"\0")

    def write_block(self, n, data):
        self.f.seek(n * BLK)
        self.f.write(data)

    def read_seg(self, s):
        return list(struct.unpack("<512H", self.block(self.dir_start + (s - 1) * 2, 2)))

    def write_seg(self, s, words):
        self.write_block(self.dir_start + (s - 1) * 2, struct.pack("<512H", *words))

    def segments(self):
        """yield (segno, words, entries) where entries = list of dicts in order"""
        s = 1
        seen = set()
        while s and s not in seen:
            seen.add(s)
            w = self.read_seg(s)
            ents, i, blk = [], 5, w[4]
            while i + self.esize <= 512:
                st = w[i]
                if st & E_EOS:
                    break
                e = {"status": st, "name": w[i + 1:i + 4], "len": w[i + 4], "job": w[i + 5],
                     "date": w[i + 6], "extra": w[i + 7:i + self.esize], "start": blk}
                ents.append(e)
                blk += e["len"]
                i += self.esize
            yield s, w, ents
            s = w[1]

    def entries(self):
        for s, w, ents in self.segments():
            for e in ents:
                yield s, e

    def find(self, name):
        target = enc_name(name)
        for s, e in self.entries():
            if e["status"] & E_PERM and list(e["name"]) == target:
                return s, e
        return None, None

    def pack_seg(self, s, w, ents):
        out = w[:5]
        for e in ents:
            out += [e["status"]] + list(e["name"]) + [e["len"], e["job"], e["date"]] + \
                   list(e["extra"] or [0] * (self.esize - 7))
        out.append(E_EOS)
        if len(out) > 512:
            raise SystemExit("directory segment %d is full - run SQUEEZE in RT-11 or use a fresh volume" % s)
        out += [0] * (512 - len(out))
        self.write_seg(s, out)

    @staticmethod
    def merge_empties(ents):
        out = []
        for e in ents:
            if out and e["status"] & E_MPTY and out[-1]["status"] & E_MPTY:
                out[-1]["len"] += e["len"]
            else:
                out.append(e)
        return out


def cmd_ls(a):
    v = Volume(a.image)
    nfiles = nblocks = free = 0
    for s, e in v.entries():
        st = e["status"]
        if st & E_PERM:
            nfiles += 1
            nblocks += e["len"]
            prot = "P" if st & E_PROT else " "
            print("%-10s %6d %s %-11s  @%d" % (dec_name(e["name"]), e["len"], prot, dec_date(e["date"]), e["start"]))
        elif st & E_MPTY:
            free += e["len"]
        elif st & E_TENT:
            print("%-10s %6d   (tentative - open/unclosed file)" % (dec_name(e["name"]), e["len"]))
    print("\n %d files, %d blocks\n %d free blocks" % (nfiles, nblocks, free))


def cmd_info(a):
    v = Volume(a.image)
    w = v.home
    vol = struct.pack("<6H", *w[0o730 // 2:0o744 // 2]).decode("ascii", "replace")
    own = struct.pack("<6H", *w[0o744 // 2:0o760 // 2]).decode("ascii", "replace")
    sysid = struct.pack("<6H", *w[0o760 // 2:0o774 // 2]).decode("ascii", "replace")
    used = sum(1 for _ in v.segments())
    print("image        %s (%d blocks)" % (a.image, os.path.getsize(a.image) // BLK))
    print("volume id    %r  owner %r  system %r" % (vol, own, sysid))
    print("dir start    block %d, %d segments (%d in use), %d extra bytes/entry" % (v.dir_start, v.nsegs, used, v.extra))


def is_text(name, a):
    if getattr(a, "binary", False):
        return False
    if getattr(a, "text", False):
        return True
    return split_name(name)[1] in TEXT_EXT


def cmd_get(a):
    v = Volume(a.image)
    s, e = v.find(a.name)
    if not e:
        raise SystemExit("%s: not found" % a.name)
    data = v.block(e["start"], e["len"]) if e["len"] else b""
    if is_text(a.name, a):
        data = data.split(b"\x1a")[0].rstrip(b"\0").replace(b"\r\n", b"\n").replace(b"\0", b"")
    out = a.hostfile or split_name(a.name)[0] + ("." + split_name(a.name)[1] if split_name(a.name)[1] else "")
    if out == "-":
        sys.stdout.buffer.write(data)
    else:
        open(out, "wb").write(data)
        print("%s -> %s (%d bytes)" % (a.name.upper(), out, len(data)))


def delete(v, name):
    s, e = v.find(name)
    if not e:
        return False
    for seg, w, ents in v.segments():
        if seg == s:
            for x in ents:
                if x["start"] == e["start"] and x["status"] & E_PERM:
                    x["status"] = E_MPTY
                    x["name"] = [0, 0, 0]
            v.pack_seg(seg, w, v.merge_empties(ents))
            return True
    return False


def cmd_rm(a):
    v = Volume(a.image, write=True)
    if not delete(v, a.name):
        raise SystemExit("%s: not found" % a.name)
    print("deleted", a.name.upper())


def cmd_put(a):
    name = (a.name or os.path.basename(a.hostfile)).upper()
    split_name(name)
    data = open(a.hostfile, "rb").read()
    if is_text(name, a):
        data = data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    nblk = (len(data) + BLK - 1) // BLK
    v = Volume(a.image, write=True)
    delete(v, name)
    for seg, w, ents in v.segments():
        for i, e in enumerate(ents):
            if e["status"] & E_MPTY and e["len"] >= nblk:
                new = {"status": E_PERM, "name": enc_name(name), "len": nblk, "job": 0,
                       "date": rt_date(a.date), "extra": [0] * (v.esize - 7), "start": e["start"]}
                e["len"] -= nblk
                e["start"] += nblk
                ents.insert(i, new)
                if e["len"] == 0 and any(x["status"] & E_MPTY for x in ents if x is not e):
                    ents.remove(e)   # keep at least one empty entry per segment
                v.pack_seg(seg, w, ents)
                v.write_block(new["start"], data.ljust(nblk * BLK, b"\0"))
                print("%s -> %s (%d blocks at %d)" % (a.hostfile, name, nblk, new["start"]))
                return
    raise SystemExit("no free area of %d blocks (volume full or fragmented - SQUEEZE in RT-11)" % nblk)


def cmd_init(a):
    t = a.type.lower()
    total = SIZES.get(t) or int(t)
    nseg = a.segments or (1 if total < 1000 else 4 if total < 12000 else 16 if total < 40000 else 31)
    ibytes = IMG_BYTES.get(t, total * BLK)
    if os.path.exists(a.image) and not a.force:
        raise SystemExit("%s exists; use --force to overwrite" % a.image)
    with open(a.image, "wb") as f:
        f.truncate(ibytes)
    hb = [0] * 256
    hb[0o700 // 2] = 0o177777
    hb[0o722 // 2] = 1
    hb[0o724 // 2] = 6
    hb[0o726 // 2] = r50enc("V3A")

    def put_ascii(off, s):
        b = s.ljust(12)[:12].encode()
        for k in range(6):
            hb[off // 2 + k] = b[2 * k] | (b[2 * k + 1] << 8)
    put_ascii(0o730, "RT11A")
    put_ascii(0o744, "")
    put_ascii(0o760, "DECRT11A")
    hb[255] = sum(hb[:255]) & 0xFFFF
    v_first = 6 + nseg * 2
    seg = [nseg, 0, 1, 0, v_first, E_MPTY, 0, 0, 0, total - v_first, 0, 0, E_EOS]
    seg += [0] * (512 - len(seg))
    with open(a.image, "r+b") as f:
        f.seek(BLK)
        f.write(struct.pack("<256H", *hb))
        f.seek(6 * BLK)
        f.write(struct.pack("<512H", *seg))
    print("initialized %s: %d blocks, %d directory segments, %d free" % (a.image, total, nseg, total - v_first))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    for n in ("ls", "info"):
        x = sp.add_parser(n); x.add_argument("image")
    x = sp.add_parser("get"); x.add_argument("image"); x.add_argument("name"); x.add_argument("hostfile", nargs="?")
    x.add_argument("--binary", action="store_true"); x.add_argument("--text", action="store_true")
    x = sp.add_parser("put"); x.add_argument("image"); x.add_argument("hostfile"); x.add_argument("name", nargs="?")
    x.add_argument("--date", help="file date: DD-MMM-YY or 'today' (default: undated; RT-11 < V5.5 shows years > 1999 as -BAD-)")
    x.add_argument("--binary", action="store_true"); x.add_argument("--text", action="store_true")
    x = sp.add_parser("rm"); x.add_argument("image"); x.add_argument("name")
    x = sp.add_parser("init"); x.add_argument("image"); x.add_argument("--type", required=True)
    x.add_argument("--segments", type=int); x.add_argument("--force", action="store_true")
    a = p.parse_args()
    {"ls": cmd_ls, "info": cmd_info, "get": cmd_get, "put": cmd_put, "rm": cmd_rm, "init": cmd_init}[a.cmd](a)


if __name__ == "__main__":
    main()
