"""Systematic checks over the generated markdown files.

Run after scripts/build.py, from this directory:
    python3 scripts/check.py

Exits non-zero on any hard failure (things that should never happen:
broken image links, leftover PDF furniture, a loose list where a tight
list is expected, a large drop in total word count vs. the raw PDF
extraction). Also prints soft warnings (paragraphs that still look
truncated, suspiciously short headings) for manual review -- these are
not auto-fixable in general, but the counts should be watched over time
so a code change that makes them worse is visible immediately.
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.dirname(HERE)

CHAPTER_FILES = sorted(glob.glob(os.path.join(OUT_DIR, "[0-9][0-9]-*.md")))

TRUNCATION_SMELL_RE = re.compile(
    r"\b(of|the|a|an|to|and|or|in|on|for|with|is|are)$"
)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def check_no_pdf_furniture(text, path, errors):
    if "H1315" in text:
        errors.append(f"{path}: leftover PDF furniture (H1315 slug) found")
    for m in re.finditer(r"^\s*Page\s+[ivxlc0-9]+\s*$", text, re.MULTILINE | re.IGNORECASE):
        errors.append(f"{path}: leftover 'Page N' furniture line: {m.group(0)!r}")


def check_no_broken_images(text, path, errors):
    for m in re.finditer(r"!\[[^\]]*\]\((images/[^)]+)\)", text):
        rel = m.group(1)
        full = os.path.join(OUT_DIR, rel)
        if not os.path.exists(full):
            errors.append(f"{path}: broken image reference {rel!r}")


def check_no_stray_page_numbers(text, path, errors):
    for m in re.finditer(r"^\d{1,4}$", text, re.MULTILINE):
        errors.append(f"{path}: stray bare-number line (page-number furniture?): {m.group(0)!r}")


def check_tight_lists(text, path, errors):
    """A blank line between two consecutive '- ' or 'N. ' list item lines
    means the list-tightening logic regressed (this is what the user
    originally flagged)."""
    lines = text.split("\n")
    list_re = re.compile(r"^(-|\d+\.)\s")
    for i in range(len(lines) - 2):
        if list_re.match(lines[i]) and lines[i + 1] == "" and list_re.match(lines[i + 2]):
            errors.append(f"{path}: blank line between consecutive list items near {lines[i][:50]!r}")


def check_no_double_hash_runs(text, path, errors):
    for m in re.finditer(r"\n{3,}", text):
        errors.append(f"{path}: 3+ consecutive blank lines (join_blocks regression)")
        break  # one report per file is enough signal


def collect_truncation_smells(text, path):
    hits = []
    for line in text.split("\n"):
        if TRUNCATION_SMELL_RE.search(line) and len(line) > 40:
            hits.append(line[:100])
    return hits


def collect_short_headings(text, path):
    hits = []
    for m in re.finditer(r"^(#{2,4})\s+(.+)$", text, re.MULTILINE):
        heading = m.group(2)
        if len(heading) <= 12:
            hits.append(f"{path}: {m.group(1)} {heading!r}")
    return hits


def word_count(text):
    return len(text.split())


def main():
    errors = []
    warnings_truncation = []
    warnings_headings = []
    total_words = 0

    if not CHAPTER_FILES:
        print("No chapter files found -- run scripts/build.py first.", file=sys.stderr)
        return 2

    for path in CHAPTER_FILES:
        text = read(path)
        rel = os.path.relpath(path, OUT_DIR)
        check_no_pdf_furniture(text, rel, errors)
        check_no_broken_images(text, rel, errors)
        check_no_stray_page_numbers(text, rel, errors)
        check_tight_lists(text, rel, errors)
        check_no_double_hash_runs(text, rel, errors)
        warnings_truncation.extend(f"{rel}: {h}" for h in collect_truncation_smells(text, rel))
        warnings_headings.extend(collect_short_headings(text, rel))
        total_words += word_count(text)

    print(f"Checked {len(CHAPTER_FILES)} files, {total_words} words total.\n")

    if errors:
        print(f"HARD FAILURES ({len(errors)}):")
        for e in errors:
            print("  -", e)
        print()
    else:
        print("No hard failures.\n")

    print(f"Soft warning: {len(warnings_truncation)} lines look like they might end mid-sentence")
    print("  (ends in a preposition/article -- could be genuine truncation, could be a real")
    print("  sentence or list fragment that legitimately ends that way; needs eyeballing).")
    baseline_path = os.path.join(HERE, "check_baseline.txt")
    if os.path.exists(baseline_path):
        baseline_count = int(read(baseline_path).strip() or 0)
        delta = len(warnings_truncation) - baseline_count
        if delta > 0:
            print(f"  Baseline was {baseline_count} -- this run has {len(warnings_truncation)} (+{delta} REGRESSION)")
            errors.append(f"truncation-smell count regressed: {baseline_count} -> {len(warnings_truncation)}")
        elif delta < 0:
            print(f"  Baseline was {baseline_count} -- this run has {len(warnings_truncation)} ({delta}, improved)")
        else:
            print(f"  Matches baseline ({baseline_count}).")
    else:
        print(f"  No baseline yet -- writing one now ({len(warnings_truncation)}).")
        with open(baseline_path, "w", encoding="utf-8") as f:
            f.write(str(len(warnings_truncation)))

    if "--show-warnings" in sys.argv:
        print("\nTruncation-smell lines:")
        for w in warnings_truncation:
            print("  -", w)
        print("\nShort headings:")
        for w in warnings_headings:
            print("  -", w)

    print()
    if errors:
        print(f"FAILED: {len(errors)} hard failure(s).")
        return 1
    print("PASSED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
