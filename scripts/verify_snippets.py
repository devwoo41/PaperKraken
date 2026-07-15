#!/usr/bin/env python3
"""PaperKraken runnable-snippet verifier.

The report's "Run it yourself" appendix pairs each code snippet with its
printed output:

    <pre class="runnable"><code>...python...</code></pre>
    <pre class="run-output">...expected stdout...</pre>

This script executes every snippet and fails if any snippet errors or its
stdout does not match the printed expectation — so a numeric example can
never ship unverified. Run BEFORE rendering:

  uv run --with numpy python verify_snippets.py <report.html>

Exit 0 = all snippets PASS (or none present). Exit 1 = any mismatch/error.
"""
import contextlib
import html as htmllib
import io
import re
import sys

PAIR_RE = re.compile(
    r'<pre class="runnable"><code>(.*?)</code></pre>\s*'
    r'<pre class="run-output">(.*?)</pre>',
    re.DOTALL,
)


def norm(text):
    """Collapse whitespace per line so cosmetic spacing can't fail a match."""
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in text.strip().splitlines()]
    return "\n".join(ln for ln in lines if ln)


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: verify_snippets.py <report.html>")
    src = open(sys.argv[1], encoding="utf-8").read()

    pairs = PAIR_RE.findall(src)
    orphans = len(re.findall(r'<pre class="runnable">', src)) - len(pairs)
    if orphans:
        print(f"FAIL: {orphans} runnable block(s) missing a run-output pair")
        sys.exit(1)
    if not pairs:
        print("no runnable snippets found (nothing to verify)")
        return

    failed = 0
    for i, (code, expected) in enumerate(pairs, 1):
        code = htmllib.unescape(code)
        expected = htmllib.unescape(expected)
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                exec(compile(code, f"<snippet {i}>", "exec"), {"__name__": "__main__"})
        except Exception as e:
            print(f"FAIL snippet {i}: raised {type(e).__name__}: {e}")
            failed += 1
            continue
        actual = buf.getvalue()
        if norm(actual) == norm(expected):
            print(f"PASS snippet {i}")
        else:
            print(f"FAIL snippet {i}: output mismatch")
            print(f"  expected: {norm(expected)!r}")
            print(f"  actual:   {norm(actual)!r}")
            failed += 1

    if failed:
        print(f"\n{failed}/{len(pairs)} snippet(s) FAILED — fix the code or the "
              f"printed output before rendering.")
        sys.exit(1)
    print(f"\nall {len(pairs)} snippets verified.")


if __name__ == "__main__":
    main()
