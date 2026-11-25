#!/usr/bin/env python3
"""WCAG 2.x contrast ratio checker (Python 3 standard library only).

Usage:
  contrast.py FG BG [--large]            check one pair
  contrast.py --pairs FILE [--min 4.5]   check many; each line: "[min=N] FG BG optional label"
                                         (min=3 for UI boundaries / focus rings / large text)

Colors: #rgb, #rrggbb, or rgba(r,g,b,a). Alpha is composited over BG.
Exit code is 1 if any pair is below the threshold
(default 4.5; 3.0 with --large; or whatever --min says).

This measures color math only. It does not prove that a design is accessible.
"""
import argparse
import re
import sys

COLOR = r"(?:rgba?\([^)]*\)|#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3})"


def parse(c):
    c = c.strip()
    m = re.fullmatch(r"#([0-9a-fA-F]{3})", c)
    if m:
        return tuple(int(ch * 2, 16) for ch in m.group(1)) + (1.0,)
    m = re.fullmatch(r"#([0-9a-fA-F]{6})", c)
    if m:
        h = m.group(1)
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 1.0)
    m = re.fullmatch(
        r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*([\d.]+)\s*)?\)", c
    )
    if m:
        a = float(m.group(4)) if m.group(4) is not None else 1.0
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)), a)
    raise ValueError("unsupported color: %r" % c)


def composite(fg, bg):
    r, g, b, a = fg
    return tuple(round(a * f + (1 - a) * k) for f, k in zip((r, g, b), bg[:3]))


def luminance(rgb):
    def channel(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg_s, bg_s):
    bg = parse(bg_s)
    fg = composite(parse(fg_s), bg)
    l1, l2 = luminance(fg), luminance(bg[:3])
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def describe(r):
    return "%5.2f:1  text(4.5) %s  large/UI(3) %s  AAA(7) %s" % (
        r,
        "pass" if r >= 4.5 else "FAIL",
        "pass" if r >= 3 else "FAIL",
        "pass" if r >= 7 else "-",
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fg", nargs="?")
    ap.add_argument("bg", nargs="?")
    ap.add_argument("--large", action="store_true", help="threshold 3.0 instead of 4.5")
    ap.add_argument("--pairs", help="file with lines: FG BG [label]")
    ap.add_argument("--min", type=float, help="override threshold")
    a = ap.parse_args()

    threshold = a.min if a.min is not None else (3.0 if a.large else 4.5)
    rows = []
    if a.pairs:
        pat = re.compile(r"(?:min=([\d.]+)\s+)?(%s)\s+(%s)\s*(.*)" % (COLOR, COLOR))
        with open(a.pairs) as fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("//") or line.startswith("# "):
                    continue
                m = pat.match(line)
                if not m:
                    print("skip (unparsed): " + line)
                    continue
                rows.append((m.group(2), m.group(3), m.group(4), float(m.group(1)) if m.group(1) else None))
    elif a.fg and a.bg:
        rows.append((a.fg, a.bg, "", None))
    else:
        ap.error("give FG BG, or --pairs FILE")

    failures = 0
    for fg, bg, label, own in rows:
        r = ratio(fg, bg)
        t = own if own is not None else threshold
        low = r < t
        failures += low
        print("%s  %s on %s  %s%s" % (describe(r), fg, bg, label, "  <-- below %.1f" % t if low else ""))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
