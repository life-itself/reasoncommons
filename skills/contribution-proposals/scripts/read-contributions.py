#!/usr/bin/env python3
"""Print the plain text of a contributions document.

Contributions arrive as whatever the room's tooling produced — most often a
Word or Google Docs export, sometimes a text file or a form dump. This turns
any of those into plain text on stdout so the reading step starts from the
words rather than from a zip archive.

    python3 read-contributions.py talk/2r_participant_contributions_test.docx

It extracts text and nothing else. Segmenting the text into contributions,
attributing them, and reading them against a model is the skill's own work and
is deliberately not automated here — see SKILL.md.

Supported: .docx (including Google Docs "Download as .docx"), .txt, .md, .csv,
.tsv. A .doc, .pdf or .odt is not handled; re-export it as .docx or paste it
into a .txt.
"""

from __future__ import annotations

import argparse
import html
import pathlib
import re
import sys
import zipfile

PLAIN = {".txt", ".md", ".markdown", ".csv", ".tsv", ".text", ""}


def from_docx(path: pathlib.Path) -> str:
    """Paragraph text out of a .docx, in document order."""
    try:
        archive = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        raise SystemExit(
            f"{path} is not a readable .docx (a .doc saved with the wrong extension?). "
            "Re-export it as .docx."
        )
    try:
        xml = archive.read("word/document.xml").decode("utf-8")
    except KeyError:
        raise SystemExit(f"{path} is a zip but has no word/document.xml — not a Word file.")

    lines = []
    for para in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S):
        # <w:br/> and <w:tab/> carry meaning inside a paragraph; keep them as space.
        para = re.sub(r"<w:(?:br|tab)\b[^>]*/?>", " ", para)
        runs = re.findall(r"<w:t[^>]*>(.*?)</w:t>", para, re.S)
        text = html.unescape(re.sub(r"<[^>]+>", "", "".join(runs)))
        lines.append(re.sub(r"[ \t]+", " ", text).strip())
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("path")
    ap.add_argument("--out", help="write here instead of stdout")
    args = ap.parse_args()

    path = pathlib.Path(args.path)
    if not path.exists():
        raise SystemExit(f"{path} does not exist")

    suffix = path.suffix.lower()
    if suffix == ".docx":
        text = from_docx(path)
    elif suffix in PLAIN:
        text = path.read_text(encoding="utf-8", errors="replace")
    else:
        raise SystemExit(
            f"cannot read {suffix or 'that'} files — supported: .docx, "
            + ", ".join(sorted(s for s in PLAIN if s))
            + ". Re-export as .docx or paste into a .txt."
        )

    # Collapse runs of blank lines; a Word export is full of empty paragraphs,
    # and blank lines are the main signal for where one contribution ends.
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"

    if args.out:
        pathlib.Path(args.out).write_text(text, encoding="utf-8")
        words = len(text.split())
        print(f"  wrote {args.out} — {words} words", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
