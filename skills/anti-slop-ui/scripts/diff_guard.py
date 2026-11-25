#!/usr/bin/env python3
"""diff_guard.py - flag possible NON-VISUAL changes in a git diff.

Anti-Slop UI promises to change how an interface looks, not how it behaves.
This script reviews the working tree (staged + unstaged + untracked) against a
base ref and lists changes to behaviour-bearing code: event handlers, hooks,
state setters, data fetching, routing, form attributes, validation, auth/env/
storage access, component prop contracts, async code, imports, and
non-visual files (package.json, API routes, config, migrations ...).

It is a HEURISTIC line-token comparison, not a parser. It will miss some
things and will occasionally flag harmless reformatting. A clean report is
NOT proof that behaviour is unchanged. Always read the diff and run the
project's own tests and build.

Usage:
  python3 scripts/diff_guard.py [--base REF] [--repo PATH] [--json]

  --base REF   compare the working tree against REF (default HEAD).
               For a feature branch use:  --base "$(git merge-base main HEAD)"
  --repo PATH  repository root (default: current directory)
  --json       machine-readable output

Exit codes: 0 nothing flagged (INFO only) | 1 any HIGH finding | 2 REVIEW findings only | 64 usage/git error
Python 3.8+, standard library only.
"""
import argparse
import collections
import json
import os
import re
import subprocess
import sys

HIGH, REVIEW, INFO = "HIGH", "REVIEW", "INFO"
SEV_ORDER = {HIGH: 0, REVIEW: 1, INFO: 2}

STYLE_EXT = {".css", ".scss", ".sass", ".less", ".styl", ".pcss"}
ASSET_EXT = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".ico", ".woff", ".woff2", ".ttf", ".otf", ".svg", ".md", ".mdx", ".txt"}
SOURCE_EXT = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".astro", ".html", ".htm", ".php", ".erb", ".hbs", ".njk", ".liquid", ".py", ".rb", ".go", ".rs", ".java", ".kt", ".swift", ".dart"}

STYLE_CONFIG_RE = re.compile(r"(^|/)(tailwind\.config\.\w+|postcss\.config\.\w+|components\.json|uno\.config\.\w+|panda\.config\.\w+)$")
NONVISUAL_PATH_RE = re.compile(
    r"(^|/)(package\.json|package-lock\.json|pnpm-lock\.yaml|yarn\.lock|bun\.lockb?|tsconfig[\w.]*\.json|"
    r"next\.config\.\w+|vite\.config\.\w+|webpack\.config\.\w+|nuxt\.config\.\w+|svelte\.config\.\w+|astro\.config\.\w+|"
    r"\.env[\w.]*|Dockerfile|docker-compose[\w.]*\.ya?ml|middleware\.\w+|schema\.prisma|\.babelrc[\w.]*|babel\.config\.\w+|"
    r"jest\.config\.\w+|vitest\.config\.\w+|playwright\.config\.\w+)$"
    r"|(^|/)(api|server|backend|routes?|migrations?|prisma|db|database|\.github/workflows|functions|lambda|graphql|trpc|actions)/"
    r"|(^|/)pages/api/|(^|/)app/api/|\.sql$"
)
# hooks that are about presentation only -> REVIEW instead of HIGH
VISUAL_HOOKS = {
    "useReducedMotion", "useTheme", "useMediaQuery", "useInView", "useScroll", "useTransform", "useSpring",
    "useMotionValue", "useMotionTemplate", "useAnimation", "useAnimate", "useAnimationControls", "useVelocity",
    "useIsomorphicLayoutEffect", "useId", "useWindowSize", "useBreakpoint",
}
VISUAL_IMPORTS_RE = re.compile(
    r"(\.css$|\.scss$|\.sass$|\.less$|^framer-motion$|^motion(/|$)|^lucide-react$|^@radix-ui/|^clsx$|^tailwind-merge$|"
    r"^class-variance-authority$|^@fontsource|^next/font|^@heroicons/|^react-icons|^@phosphor-icons/|^@tabler/icons|"
    r"^tailwindcss-animate$|^geist(/|$)|\.(png|jpe?g|svg|webp|avif|woff2?)$)"
)

CLASS_ATTR_RE = re.compile(r"""\bclass(?:Name)?\s*=\s*(?:"[^"]*"|'[^']*'|\{`[^`]*`\}|\{[^{}]*\})""")
HIDE_CLASS_RE = re.compile(r"(?<![\w-])((?:[a-z0-9\[\]=-]+:)*)(hidden|invisible|pointer-events-none|opacity-0)(?![\w-])")
HIDE_CSS_RE = re.compile(r"\b(display\s*:\s*none|visibility\s*:\s*hidden|pointer-events\s*:\s*none|opacity\s*:\s*0)\b")

HANDLER_RE = re.compile(r"\b(on[A-Z][A-Za-z0-9]*)\s*=\s*")
VUE_EVT_RE = re.compile(r"(@[\w.:-]+|v-on:[\w.:-]+|\bon:[\w.:-]+|\([a-z][\w.]*\))\s*=\s*(\"[^\"]*\"|'[^']*'|\{[^}]*\})")
HOOK_RE = re.compile(r"\b(use[A-Z][A-Za-z0-9]*)\s*\(")
SETTER_RE = re.compile(r"\b(set[A-Z][A-Za-z0-9]*|dispatch)\s*\(")
DATA_RE = re.compile(r"\b(fetch|axios(?:\.\w+)?|XMLHttpRequest|WebSocket|EventSource|trpc\.[\w.]+|supabase\.[\w.]+|prisma\.[\w.]+|firebase\.[\w.]+|apollo\.[\w.]+|gql|graphql)\s*[(`]")
ROUTE_FN_RE = re.compile(r"\b(navigate|redirect|permanentRedirect|notFound|useNavigate|useRouter|usePathname|useParams|useSearchParams|router\.\w+|history\.\w+)\s*\(")
ROUTE_TAG_RE = re.compile(r"<(Link|NavLink|Route|Routes|Navigate|Redirect|Outlet)\b")
ROUTE_ATTR_RE = re.compile(r"\b(href|to|action|method|formAction)\s*=\s*(\{[^}]*\}|\"[^\"]*\"|'[^']*')")
FORM_ATTR_RE = re.compile(
    r"\b(name|type|required|pattern|minLength|maxLength|min|max|step|autoComplete|inputMode|multiple|accept|"
    r"checked|defaultChecked|defaultValue|value|disabled|readOnly|htmlFor|for|form|enctype|noValidate)\s*=\s*(\{[^}]*\}|\"[^\"]*\"|'[^']*')"
)
FORM_BARE_RE = re.compile(r"(?<![\w-])(required|disabled|readOnly|multiple|noValidate)(?=[\s/>]|$)")
FORM_TAG_RE = re.compile(r"<(form|input|select|textarea|option|fieldset)\b")
VALID_RE = re.compile(r"\b(z\.\w+|yup\.\w+|zodResolver|yupResolver|valibotResolver|useForm|register|handleSubmit|validate\w*|checkValidity|reportValidity|preventDefault|stopPropagation)\b\s*\(?")
AUTH_RE = re.compile(r"\b(process\.env\.\w+|import\.meta\.env\.\w+|signIn|signOut|useSession|getSession|useAuth|useUser|csrf\w*|document\.cookie|localStorage|sessionStorage|Authorization|Bearer|jwt\w*|password|passwd|secret|apiKey|api_key)\b")
ASYNC_RE = re.compile(r"\b(await|async)\b|\.then\(|\.catch\(|\.finally\(|new Promise|setTimeout\(|setInterval\(")
CONTRACT_RE = re.compile(
    r"\b(?:interface|type)\s+\w*Props\b|\bexport\s+(?:default\s+)?(?:async\s+)?function\s+[A-Z]\w*\s*\(|"
    r"\bconst\s+[A-Z]\w*\s*(?::[^=]+)?=\s*(?:React\.)?(?:memo|forwardRef)?\(?\s*(?:async\s*)?\(?\s*[{(\w]|"
    r"\bon[A-Z]\w*\??\s*:\s*[(\w]|\bProps\b"
)
# property signature that looks like a TYPE (not an object-literal value): "name?: string | null;"
PROP_SIG_RE = re.compile(
    r"^\s*(?:readonly\s+)?[\w$]+\??\s*:\s*(?=.*(?:\b(?:string|number|boolean|void|unknown|any|never|null|undefined|"
    r"ReactNode|ReactElement|Record<|Array<|Promise<|React\.\w+)\b|=>|\s\|\s|\[\]))[^=]*?[;,]?\s*$"
)
INTERACTIVE_TAG_RE = re.compile(r"<(button|a|input|select|textarea|form|dialog|details|summary|label)\b")
ARIA_RE = re.compile(r"\b(aria-[a-z]+|role|tabIndex|tabindex)\s*=\s*(\{[^}]*\}|\"[^\"]*\"|'[^']*')")
IMPORT_RE = re.compile(r"^\s*import\s+(?:[^'\"]*?\s+from\s+)?['\"]([^'\"]+)['\"]|\brequire\(\s*['\"]([^'\"]+)['\"]\s*\)|^\s*from\s+([\w.]+)\s+import\b")


def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if p.returncode != 0:
        sys.stderr.write("git error: %s\n" % p.stderr.strip())
        sys.exit(64)
    return p.stdout


def balanced(s, i):
    """Return s[i:j] where s[i] opens {, ( or [ and j is just past the match (or end of line)."""
    pairs = {"{": "}", "(": ")", "[": "]"}
    if i >= len(s) or s[i] not in pairs:
        return ""
    depth = 0
    for j in range(i, len(s)):
        if s[j] in pairs:
            depth += 1
        elif s[j] in pairs.values():
            depth -= 1
            if depth == 0:
                return s[i:j + 1]
    return s[i:]


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def classify_path(path):
    ext = os.path.splitext(path)[1].lower()
    if STYLE_CONFIG_RE.search(path):
        return "style"
    if NONVISUAL_PATH_RE.search(path):
        return "nonvisual"
    if ext in STYLE_EXT:
        return "style"
    if ext in SOURCE_EXT:
        return "source"
    if ext in ASSET_EXT:
        return "asset"
    return "other"


def line_tokens(line, kind, path_hint=""):
    """Return list of (severity, category, token) for one changed line."""
    out = []
    if kind == "style":
        for m in HIDE_CSS_RE.finditer(line):
            out.append((REVIEW, "hides-ui", "css:" + norm(m.group(1))))
        return out

    raw = line
    # hide-class detection works on class strings, before they are stripped
    if re.search(r"\bclass(Name)?\b|\bcn\(|\bclsx\(|\bcva\(|\btwMerge\(", raw):
        for m in HIDE_CLASS_RE.finditer(raw):
            out.append((REVIEW, "hides-ui", "class:" + m.group(1) + m.group(2)))
    code = CLASS_ATTR_RE.sub("className=<classes>", raw)

    for m in HANDLER_RE.finditer(code):
        rest = code[m.end():]
        if rest[:1] == "{":
            val = balanced(rest, 0)
        elif rest[:1] in ("'", '"'):
            mm = re.match(r"\"[^\"]*\"|'[^']*'", rest)
            val = mm.group(0) if mm else ""
        else:
            val = ""
        out.append((HIGH, "event-handler", norm(m.group(1) + "=" + val)))
    for m in VUE_EVT_RE.finditer(code):
        out.append((HIGH, "event-handler", norm(m.group(0))))
    for m in HOOK_RE.finditer(code):
        arg = balanced(code, m.end() - 1)
        name = m.group(1)
        sev = REVIEW if name in VISUAL_HOOKS else HIGH
        cat = "visual-hook" if name in VISUAL_HOOKS else "hook"
        out.append((sev, cat, norm(name + arg)))
    for m in SETTER_RE.finditer(code):
        out.append((HIGH, "state-update", norm(m.group(1) + balanced(code, m.end() - 1))))
    for m in DATA_RE.finditer(code):
        out.append((HIGH, "data-access", norm(code[m.start():m.end() + 60])))
    for m in ROUTE_FN_RE.finditer(code):
        out.append((HIGH, "routing", norm(m.group(1) + balanced(code, m.end() - 1))))
    for m in ROUTE_TAG_RE.finditer(code):
        out.append((HIGH, "routing", "<" + m.group(1)))
    for m in ROUTE_ATTR_RE.finditer(code):
        out.append((HIGH, "routing/form-target", norm(m.group(1) + "=" + m.group(2))))
    for m in FORM_TAG_RE.finditer(code):
        out.append((HIGH, "form", "<" + m.group(1)))
    for m in FORM_ATTR_RE.finditer(code):
        out.append((HIGH, "form-attr", norm(m.group(1) + "=" + m.group(2))))
    for m in FORM_BARE_RE.finditer(code):
        if "=" not in code[m.end():m.end() + 1]:
            out.append((HIGH, "form-attr", m.group(1)))
    for m in VALID_RE.finditer(code):
        out.append((HIGH, "validation", norm(m.group(0))))
    for m in AUTH_RE.finditer(code):
        out.append((HIGH, "auth/env/storage", m.group(1)))
    for m in ASYNC_RE.finditer(code):
        out.append((HIGH, "async", norm(m.group(0))))
    for m in CONTRACT_RE.finditer(code):
        out.append((HIGH, "component-contract", norm(code[m.start():m.start() + 80])))
    if PROP_SIG_RE.match(code) and os.path.splitext(path_hint)[1].lower() in (".ts", ".tsx", ".vue", ".svelte"):
        out.append((HIGH, "component-contract", norm(code)))
    for m in INTERACTIVE_TAG_RE.finditer(code):
        out.append((REVIEW, "interactive-element", "<" + m.group(1)))
    for m in ARIA_RE.finditer(code):
        out.append((INFO, "a11y-attr", norm(m.group(1) + "=" + m.group(2))))
    m = IMPORT_RE.search(code)
    if m:
        mod = next(g for g in m.groups() if g)
        if VISUAL_IMPORTS_RE.search(mod):
            out.append((INFO, "visual-import", "import:" + mod))
        else:
            out.append((REVIEW, "import-change", "import:" + mod))
    return out


def parse_diff(text):
    """Yield dicts: path, old_path, status, removed[(lineno, line)], added[(lineno, line)]."""
    files, cur = [], None
    old_ln = new_ln = 0
    for raw in text.splitlines():
        if raw.startswith("diff --git "):
            m = re.match(r"diff --git a/(.*) b/(.*)$", raw)
            cur = {"path": m.group(2) if m else raw, "old_path": m.group(1) if m else raw, "status": "modified", "removed": [], "added": [], "binary": False}
            files.append(cur)
        elif cur is None:
            continue
        elif raw.startswith("new file mode"):
            cur["status"] = "added"
        elif raw.startswith("deleted file mode"):
            cur["status"] = "deleted"
        elif raw.startswith("rename from"):
            cur["status"] = "renamed"
        elif raw.startswith("Binary files"):
            cur["binary"] = True
        elif raw.startswith("@@"):
            m = re.match(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", raw)
            old_ln, new_ln = int(m.group(1)), int(m.group(2))
        elif raw.startswith("---") or raw.startswith("+++"):
            continue
        elif raw.startswith("-"):
            cur["removed"].append((old_ln, raw[1:]))
            old_ln += 1
        elif raw.startswith("+"):
            cur["added"].append((new_ln, raw[1:]))
            new_ln += 1
    return files


def analyze(files):
    findings = []
    for f in files:
        path, kind = f["path"], classify_path(f["path"])
        if f["binary"] or not (f["removed"] or f["added"] or f["status"] in ("deleted", "renamed")):
            continue
        if kind == "nonvisual":
            findings.append({"severity": REVIEW, "category": "non-visual-file", "file": path, "line": 0,
                             "change": "touched", "detail": "%s (%s). Visual work should not need this file." % (path, f["status"])})
        if f["status"] == "deleted" and kind == "source":
            findings.append({"severity": HIGH, "category": "file-deleted", "file": path, "line": 0,
                             "change": "removed", "detail": "source file deleted"})
        if f["status"] == "renamed" and kind == "source":
            findings.append({"severity": REVIEW, "category": "file-renamed", "file": path, "line": 0,
                             "change": "changed", "detail": "renamed from %s - check all imports/routes" % f["old_path"]})
        if kind not in ("source", "style"):
            continue
        rem = collections.defaultdict(list)
        add = collections.defaultdict(list)
        for ln, text in f["removed"]:
            for sev, cat, tok in line_tokens(text, kind, path):
                rem[(sev, cat, tok)].append(ln)
        for ln, text in f["added"]:
            for sev, cat, tok in line_tokens(text, kind, path):
                add[(sev, cat, tok)].append(ln)
        for key in set(rem) | set(add):
            sev, cat, tok = key
            nr, na = len(rem.get(key, [])), len(add.get(key, []))
            if nr == na:
                continue  # same token count before/after: moved or reformatted
            if nr > na:
                change, line = "removed/changed", rem[key][0]
                detail = "%s  (x%d before, x%d after; old line %d)" % (tok, nr, na, line)
            else:
                change, line = "added/changed", add[key][0]
                detail = "%s  (x%d before, x%d after; new line %d)" % (tok, nr, na, line)
            # additions of purely informational a11y attrs / visual imports stay INFO
            findings.append({"severity": sev, "category": cat, "file": path, "line": line, "change": change, "detail": detail})
    findings.sort(key=lambda x: (SEV_ORDER[x["severity"]], x["file"], x["line"]))
    return findings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default="HEAD")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    run(["git", "rev-parse", "--git-dir"], a.repo)
    diff = run(["git", "diff", "--no-color", "--no-ext-diff", "-U0", "-M", a.base, "--"], a.repo)
    files = parse_diff(diff)
    untracked = [p for p in run(["git", "ls-files", "--others", "--exclude-standard"], a.repo).splitlines() if p]
    for p in untracked:
        full = os.path.join(a.repo, p)
        try:
            with open(full, "r", encoding="utf-8") as fh:
                lines = fh.read().splitlines()
        except (UnicodeDecodeError, OSError):
            continue
        files.append({"path": p, "old_path": p, "status": "added", "removed": [],
                      "added": [(i + 1, l) for i, l in enumerate(lines)], "binary": False})

    findings = analyze(files)
    counts = collections.Counter(f["severity"] for f in findings)

    if a.json:
        print(json.dumps({"base": a.base, "files_in_diff": [f["path"] for f in files], "counts": counts, "findings": findings}, indent=2))
    else:
        print("diff_guard: base=%s, %d file(s) in diff (incl. untracked)" % (a.base, len(files)))
        if not findings:
            print("No behaviour-bearing changes detected by the heuristics.")
        cur = None
        for f in findings:
            if f["severity"] != cur:
                cur = f["severity"]
                print("\n[%s]" % cur)
            loc = "%s:%s" % (f["file"], f["line"]) if f["line"] else f["file"]
            print("  %-22s %s  %s" % (f["category"], loc, f["detail"]))
        print("\nSummary: HIGH=%d REVIEW=%d INFO=%d" % (counts[HIGH], counts[REVIEW], counts[INFO]))
        print("HIGH = likely behaviour change: revert it or get explicit permission.")
        print("REVIEW = could be visual or functional: justify each one in the report.")
        print("INFO = informational (e.g. aria attributes, styling imports): check that nothing was removed.")
        print("Heuristic only: a clean result is NOT proof behaviour is unchanged. Read the diff; run tests and build.")

    sys.exit(1 if counts[HIGH] else (2 if counts[REVIEW] else 0))


if __name__ == "__main__":
    main()
