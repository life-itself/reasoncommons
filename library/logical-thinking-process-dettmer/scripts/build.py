import re, os, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.dirname(HERE)
IMG_DIR = os.path.join(OUT_DIR, "images")
PDF = os.path.join(OUT_DIR, "source", "logical-thinking-process-dettmer.pdf")
FULL = os.path.join(tempfile.gettempdir(), "ltp_full_plain.txt")

# Regenerate the plain-text extraction and figure-page images from the PDF.
# Run once; comment out after the first run if iterating on reflow logic only.
def build_text_extraction():
    subprocess.run(["pdftotext", PDF, FULL], check=True)


def build_figure_images(printed_pages):
    os.makedirs(IMG_DIR, exist_ok=True)
    for printed in printed_pages:
        phys = printed + 32
        fname = f"p{printed:03d}"
        out_png = os.path.join(IMG_DIR, fname + ".png")
        if os.path.exists(out_png):
            continue
        tmp_prefix = os.path.join(IMG_DIR, "tmp_" + fname)
        subprocess.run(["pdftoppm", "-png", "-r", "100", "-f", str(phys), "-l", str(phys), PDF, tmp_prefix], check=True)
        src = tmp_prefix + f"-{phys}.png"
        if not os.path.exists(src):
            matches = [f for f in os.listdir(IMG_DIR) if f.startswith("tmp_" + fname)]
            if not matches:
                continue
            src = os.path.join(IMG_DIR, matches[0])
        try:
            subprocess.run(["pngquant", "--quality=65-90", "--force", "--output", out_png, src], check=True)
        except Exception:
            os.replace(src, out_png)
        if os.path.exists(src):
            os.remove(src)

# Printed pages to render as figure images: the book's own List of Illustrations
# (222 pages) plus 29 more found by scanning for diagram-label text with no
# matching prose (mostly the unlabeled decorative diagrams opening each chapter).
FIGURE_PRINTED_PAGES = [3,4,7,8,9,10,11,13,16,18,20,23,24,25,26,27,28,29,30,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,53,54,55,56,57,60,61,62,63,64,65,67,71,72,73,74,75,77,78,79,80,81,82,83,84,86,88,91,93,95,96,97,99,100,102,103,104,106,107,110,111,112,113,114,116,117,118,119,120,121,123,124,126,127,129,130,131,132,133,134,135,136,137,139,141,142,143,144,145,148,149,150,151,152,153,156,159,160,161,165,166,167,168,169,170,173,174,176,177,178,179,181,182,183,184,185,186,187,188,189,190,191,193,194,196,197,198,199,200,201,202,203,205,207,210,211,212,213,214,215,218,219,220,221,222,223,224,226,227,229,230,231,232,233,234,236,237,239,240,244,245,246,247,248,251,252,261,263,264,266,268,269,271,273,275,276,277,278,279,280,282,283,284,286,287,288,289,291,292,293,296,297,298,299,301,302,303,304,305,306,307,308,311,314,318,319,321,324,326,330,333,334,337,342,345,346,347,348,350,351,352,353,354,371,372,373,374,375,384,385,388,389,390,394,395]

SMALLWORDS = {"a","an","the","of","in","on","to","and","or","for","vs","vs.","is","as","at","by","from","with","it"}

CHAPTER_TITLES = {
    "Categories of Legitimate Reservation",
    "Introduction to the Theory of Constraints",
    "Intermediate Objectives Map",
    "Current Reality Tree",
    "Evaporating Cloud",
    "Future Reality Tree",
    "Prerequisite and Transition Trees",
    "Changing the Status Quo",
}
RUNNING_HEADER_STRINGS = CHAPTER_TITLES | {
    "Front Matter", "Table of Contents", "List of Illustrations", "Preface",
    "Acknowledgments", "Introduction", "Epilogue",
    "Appendix A", "Appendix B", "Appendix C", "Appendix D",
    "Appendix E", "Appendix F", "Appendix G", "Appendix H", "Appendix I", "Appendix J",
    "Glossary of Thinking Process Terms", "Bibliography", "Index",
    "Glossary", "Appendix", "Epilogue's",
}

GLOSSARY_SPLIT_RE = re.compile(r'(?<=[\.\)\?!”"])\s+(?=[A-Za-z][a-zA-Z\-\s\(\)]{1,55}?—)')


def split_glossary_entries(text):
    parts = GLOSSARY_SPLIT_RE.split(text)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if "—" in p:
            term, rest = p.split("—", 1)
            out.append(f"**{term.strip()}** — {rest.strip()}")
        else:
            out.append(p)
    return out

# printed_page -> markdown heading lines to inject before that page's content;
# and title text fragments (lower-cased, no punctuation) to suppress if auto-detected.
INJECTED_HEADINGS = {
    1:   (["# Part I -- The Destination", "", "# Chapter 1: Introduction to the Theory of Constraints"], ["the destination", "introduction to the", "theory of constraints"]),
    31:  (["# Chapter 2: Categories of Legitimate Reservation"], ["categories of", "legitimate reservation"]),
    67:  (["# Chapter 3: Intermediate Objectives Map"], ["intermediate objectives map"]),
    89:  (["# Part II -- Gap Analysis and Correction", "", "# Chapter 4: Current Reality Tree"], ["gap analysis and correction", "current reality tree"]),
    159: (["# Chapter 5: Evaporating Cloud"], ["evaporating cloud"]),
    205: (["# Chapter 6: Future Reality Tree"], ["future reality tree"]),
    259: (["# Part III -- Executing Change", "", "# Chapter 7: Prerequisite and Transition Trees"], ["executing change", "prerequisite and transition trees"]),
    311: (["# Chapter 8: Changing the Status Quo"], ["changing the status quo"]),
    339: (["# Epilogue"], ["epilogue"]),
    341: (["# Appendices", "", "## Appendix A: Strategic Intermediate Objectives Map"], ["appendices", "appendix a", "strategic intermediate objectives map"]),
    343: (["## Appendix B: Executive Summary Trees"], ["appendix b", "executive summary trees"]),
    356: (["## Appendix C: Current Reality Tree Exercise"], ["appendix c", "current reality tree exercise"]),
    357: (["## Appendix D: Evaporating Cloud Exercise"], ["appendix d", "evaporating cloud exercise"]),
    359: (["## Appendix E: The 3-UDE Cloud"], ["appendix e", "the 3-ude cloud"]),
    369: (["## Appendix F: The Challenger Conflict"], ["appendix f", "the challenger conflict"]),
    376: (["## Appendix G: Correlation Versus Cause and Effect"], ["appendix g", "correlation versus cause and effect"]),
    377: (["## Appendix H: Theories of Motivation"], ["appendix h", "theories of motivation"]),
    382: (["## Appendix I: Legal Application of the Thinking Process"], ["appendix i", "legal application of the thinking process"]),
    394: (["## Appendix J: Transformation Logic Tree Software"], ["appendix j", "transformation logic tree software"]),
    397: (["# Glossary of Thinking Process Terms"], ["glossary of thinking process terms"]),
    401: (["# Bibliography"], ["bibliography"]),
    -22: (["# Preface"], ["preface"]),   # placeholder, replaced below via roman map
}

# front-matter special pages use roman numerals; map by physical page instead.
FRONT_MATTER_INJECT_BY_PHYSICAL = {
    3:  ["# The Logical Thinking Process", "", "*A Systems Approach to Complex Problem Solving*", "", "H. William Dettmer"],
    9:  ["# Table of Contents"],
    17: ["# List of Illustrations"],
    25: ["# Preface"],
    27: ["# Acknowledgments"],
    29: ["# Introduction"],
}
del INJECTED_HEADINGS[-22]


DIAGRAM_LABEL_WORDS = {
    "inj", "injection", "positives", "negatives", "potential", "loop",
    "desired effect", "undesirable effect", "ude", "positive", "negative",
    "negative branch", "desirable effect", "mag", "qsr", "branchtrimming",
}


def _looks_like_diagram_label(s):
    if s.startswith("[") or s.endswith("]"):
        return True
    if re.search(r"#\s*\d", s):
        return True
    if re.match(r"^\d{1,4}\s+[A-Za-z]{1,15}$", s.strip()):
        return True
    norm = re.sub(r"[^a-z ]", "", s.lower()).strip()
    if norm in DIAGRAM_LABEL_WORDS:
        return True
    return False


def is_allcaps_heading(line):
    if _looks_like_diagram_label(line):
        return False
    letters = re.sub(r"[^A-Za-z]", "", line)
    if len(letters) < 3:
        return False
    if letters != letters.upper():
        return False
    words = line.split()
    if not (1 <= len(words) <= 12):
        return False
    if line.rstrip().endswith((".", ",", ";", ":")):
        return False
    return True


def is_numbered_marker(line):
    return re.match(r"^(\d{1,2})\.\s+\S", line.strip()) is not None


def numbered_marker_num(line):
    m = re.match(r"^(\d{1,2})\.\s+(.*)$", line.strip())
    return int(m.group(1)), m.group(2)


def is_titlecase_heading(line):
    s = line.strip()
    if not s or len(s) > 60 or len(s) < 4:
        return False
    if _looks_like_diagram_label(s):
        return False
    if s.endswith((".", ",", ";", ":", "!", ")", '"', "”")):
        return False
    if ENDS_WITH_CONNECTIVE_RE.search(s):
        # A real heading doesn't dangle on "...a" / "...the" / "...of" --
        # this is a body sentence that happens to line-wrap right after a
        # short word, not a heading (e.g. "Sometimes a" wrapping before
        # "contributing cause is...").
        return False
    words = re.findall(r"[A-Za-z'’]+", s)
    if not (1 <= len(words) <= 8):
        return False
    if len(words) == 1 and words[0].lower() in {"yes", "no", "true", "false", "and", "or", "but", "note", "test"}:
        return False
    if any(ch.isdigit() for ch in s):
        return False
    for i, w in enumerate(words):
        wl = w.lower()
        if w[0].isupper():
            continue
        if wl in SMALLWORDS and i != 0:
            continue
        return False
    return True


LABEL_RE = re.compile(r"^([A-Z][A-Z \-]{2,25}):\s*(.*)$")


def is_label_line(line):
    m = LABEL_RE.match(line.strip())
    if not m:
        return False
    return 1 <= len(m.group(1).split()) <= 4


def strip_page_furniture(page_text):
    lines = page_text.split("\n")
    i, n = 0, len(lines)

    def blank(k):
        return k < n and lines[k].strip() == ""

    if i < n and lines[i].startswith("H1315"):
        i += 1
        while blank(i):
            i += 1
        if i < n and re.match(r"^\d{1,2}/\d{1,2}/\d{2}$", lines[i].strip()):
            i += 1
            while blank(i):
                i += 1
        if i < n and re.match(r"^\d{1,2}:\d{2}\s*(AM|PM)$", lines[i].strip(), re.IGNORECASE):
            i += 1
            while blank(i):
                i += 1
        if i < n and re.match(r"^Page\s+[ivxlcIVXLC0-9]+$", lines[i].strip()):
            i += 1
            while blank(i):
                i += 1

    for _ in range(2):
        if i >= n:
            break
        s = lines[i].strip()
        if s == "":
            i += 1
            continue
        if s in RUNNING_HEADER_STRINGS:
            i += 1
            continue
        if re.match(r"^\d{1,4}\s+[A-Za-z].{0,40}$", s) and not s.endswith((".", "?", "!")):
            i += 1
            continue
        if re.match(r"^[ivxlc]+$", s, re.IGNORECASE) or re.match(r"^\d{1,4}$", s):
            i += 1
            continue
        break

    return "\n".join(lines[i:])


QUOTE_CHARS = {'"', "'", "“", "‘"}


def merge_drop_cap(text):
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if re.match(r"^[A-Z]$", s) and i + 1 < len(lines):
            j = i + 1
            while j < len(lines) and lines[j].strip() == "":
                j += 1
            quote = ""
            if j < len(lines) and lines[j].strip() in QUOTE_CHARS:
                quote = lines[j].strip()
                j += 1
                while j < len(lines) and lines[j].strip() == "":
                    j += 1
            if j < len(lines) and re.match(r"^[a-z]", lines[j].strip()):
                out.append(quote + s + lines[j].strip())
                i = j + 1
                continue
        out.append(lines[i])
        i += 1
    return "\n".join(out)


def classify_and_reflow(body_text):
    raw_lines = body_text.split("\n")

    # Pass 1: find numbered-marker line indices (non-blank content lines only)
    marker_idxs = [k for k, l in enumerate(raw_lines) if is_numbered_marker(l.strip())]
    treat_as_list = len(marker_idxs) >= 2

    items = []
    buf, buf_type = [], "p"

    def flush():
        nonlocal buf, buf_type
        if buf:
            text = re.sub(r"\s+", " ", " ".join(x.strip() for x in buf if x.strip())).strip()
            if text:
                items.append((buf_type, text))
        buf, buf_type = [], "p"

    for k, raw in enumerate(raw_lines):
        s = raw.strip()
        if s == "":
            flush()
            continue
        if re.match(r"^\d{1,4}$", s):
            # stray running page-number noise; drop entirely
            continue
        if is_numbered_marker(s):
            flush()
            if treat_as_list:
                buf_type = "olist"
                num, rest = numbered_marker_num(s)
                buf.append(rest)
                continue
            else:
                # lone numbered heading candidate
                num, rest = numbered_marker_num(s)
                words = rest.split()
                if 1 <= len(words) <= 8 and not rest.rstrip().endswith((".", ",", ";", ":")):
                    items.append(("h3", f"{num}. {rest}"))
                    continue
                buf_type = "p"
                buf.append(s)
                continue
        if s.startswith("•") or s.startswith("●") or re.match(r"^[–-]\s+\S", s):
            # "•"/"●" are the book's usual bullet glyphs; a leading en dash
            # or hyphen ("– Determine the two preceding causes of...") is
            # this book's alternate bullet style for procedural checklists
            # -- NOT an em-dash ("—") epigraph attribution, which is a
            # different character handled separately below.
            flush()
            buf_type = "bullet"
            buf.append(re.sub(r"^[•●–-]\s*", "", s))
            continue
        if re.match(r"^—\s*\S", s):
            flush()
            items.append(("attrib", s))
            continue
        if is_allcaps_heading(s):
            flush()
            items.append(("h2", s))
            continue
        if is_titlecase_heading(s):
            flush()
            items.append(("h3", s))
            continue
        if is_label_line(s):
            flush()
            buf_type = "label"
            buf.append(s)
            continue
        buf.append(s)

    flush()

    # merge adjacent same-type headings (wrapped multi-line titles)
    merged = []
    for typ, text in items:
        if merged and merged[-1][0] == typ and typ in ("h2", "h3"):
            merged[-1] = (typ, merged[-1][1] + " " + text)
        else:
            merged.append((typ, text))
    return merge_split_sentences(merged)


# A real English sentence never ends on one of these -- if the extracted
# text does, it's a strong, case-independent signal of a genuine mid-word
# cut (e.g. "...associated with" / "the sum of all the"), stronger than
# just "no terminal punctuation". Used to allow stitching even when the
# continuation happens to start with a capitalized term (e.g. "Throughput",
# a term this book always capitalizes).
ENDS_WITH_CONNECTIVE_RE = re.compile(
    r"\b(of|the|a|an|to|and|or|in|on|for|with|is|are|by|from|that|which|as|at)$",
    re.IGNORECASE,
)


def merge_split_sentences(items):
    """Stitch a paragraph back together when a sidebar figure interrupts it
    mid-sentence in the source PDF's linear reading order (body text wraps
    around a boxed figure; pdftotext reads the figure's caption/bullets in
    between the two halves of the sentence). Detected as: a 'p' paragraph
    with no terminal punctuation, followed (after any intervening
    headings/bullets/labels from the figure) by another 'p' paragraph that
    starts with a lowercase word -- i.e. a continuation, not a new sentence
    -- or, regardless of case, when the cut paragraph ends on a preposition
    or article (a stronger, unambiguous truncation signal).
    """
    out = list(items)
    i = 0
    while i < len(out):
        typ, text = out[i]
        if typ in ("p", "label", "bullet") and word_count(text) >= 10 and not text.rstrip().endswith((".", "!", "?", "”", '"', ":", ";", ")")):
            # Bullets legitimately end on a stranded preposition/conjunction
            # a lot ("...as you can think of", "...to invalidate, and") so
            # the case-independent connective bypass is unsafe for them --
            # only merge a bullet when the next paragraph unambiguously
            # starts lowercase (a real continuation, not a coincidence).
            definitely_cut = typ != "bullet" and bool(ENDS_WITH_CONNECTIVE_RE.search(text.rstrip()))
            for j in range(i + 1, len(out)):
                jtyp, jtext = out[j]
                if jtyp in ("p", "label"):
                    if word_count(jtext) < 10:
                        continue  # too short to be a real paragraph (e.g. a figure caption) -- keep scanning
                    if definitely_cut or jtext[:1].islower():
                        out[i] = (typ, text.rstrip() + " " + jtext)
                        del out[j]
                    break
        i += 1
    return out


def word_count(text):
    return len(text.split())


def para_is_fragment(text):
    """A short, punctuation-less snippet -- typically a diagram box label or
    a page-reference bubble ("205 / p. 2") bleeding out of a figure. Used
    only to decide whether text is *substantial enough to justify a
    heading above it* -- never to discard text outright, since a genuinely
    truncated real sentence (cut off at a page boundary) has exactly the
    same shape (short, no terminal punctuation) and must not be deleted.
    """
    wc = word_count(text)
    if wc < 6:
        return True
    if wc <= 20 and not text.endswith((".", "!", "”", '"', ";")):
        return True
    return False


def _is_substantial(item):
    if item is None:
        return False
    typ, text = item
    if typ in ("bullet", "olist"):
        return word_count(text) >= 6
    if typ == "p":
        return word_count(text) >= 10 and not para_is_fragment(text)
    return False


def drop_orphan_headings(items, has_image):
    """Demote headings/labels that look like diagram-label bleed rather than
    real section headings (i.e. not followed by substantial content) back
    into plain paragraph text, folded into the previous paragraph if there
    is one. Never silently discards text -- misclassified real prose stays,
    just without the spurious heading marker in front of it.
    """
    out = []
    for idx, (typ, text) in enumerate(items):
        is_orphan_candidate = (
            typ == "h3"
            or (typ == "h2" and has_image)
            or (typ == "label" and has_image and not (LABEL_RE.match(text) and LABEL_RE.match(text).group(2).strip()))
        )
        if is_orphan_candidate:
            nxt = items[idx + 1] if idx + 1 < len(items) else None
            if not _is_substantial(nxt):
                if out and out[-1][0] == "p":
                    prev_typ, prev_text = out.pop()
                    out.append(("p", prev_text + " " + text))
                else:
                    out.append(("p", text))
                continue
        out.append((typ, text))
    return out


def merge_attributions(items):
    out = []
    i = 0
    while i < len(items):
        typ, text = items[i]
        if typ == "attrib" and out and out[-1][0] == "p":
            prev_typ, prev_text = out.pop()
            out.append(("quote", prev_text + "\n>\n> " + text))
        else:
            out.append((typ, text))
        i += 1
    return out


def smart_title(text):
    words = text.split(" ")
    out = []
    for w in words:
        if not w:
            out.append(w)
            continue
        lw = w.lower()
        if len(out) > 0 and lw in SMALLWORDS:
            out.append(lw)
            continue
        # capitalize first alpha char, lowercase the rest (keeps trailing 's, -, etc. sane)
        m = re.match(r"^([^A-Za-z]*)([A-Za-z])(.*)$", w)
        if m:
            out.append(m.group(1) + m.group(2).upper() + m.group(3).lower())
        else:
            out.append(w)
    return " ".join(out)


def render_items(items, has_image):
    items = merge_attributions(items)
    out = []
    for typ, text in items:
        if typ == "h2":
            out.append(f"### {smart_title(text)}" if text.isupper() else f"### {text}")
        elif typ == "h3":
            out.append(f"#### {text}")
        elif typ == "bullet":
            out.append(f"- {text}")
        elif typ == "olist":
            out.append(("OLIST", text))
        elif typ == "label":
            m = LABEL_RE.match(text)
            if m:
                label, rest = m.group(1), m.group(2)
                out.append(f"**{label}:** {rest}" if rest else f"**{label}:**")
            else:
                out.append(text)
        elif typ == "attrib":
            out.append(f"> {text}")
        elif typ == "quote":
            out.append(f"> {text}")
        elif typ == "p":
            out.append(text)
    # renumber consecutive OLIST entries
    final = []
    n = 1
    for x in out:
        if isinstance(x, tuple) and x[0] == "OLIST":
            final.append(f"{n}. {x[1]}")
            n += 1
        else:
            final.append(x)
            n = 1
    return final


def suppress_title_dupes(items, suppress_fragments):
    if not suppress_fragments:
        return items
    out = []
    for typ, text in items:
        norm = re.sub(r"[^a-z ]", "", text.lower()).strip()
        if typ in ("h2", "h3") and any(frag in norm or norm in frag for frag in suppress_fragments):
            continue
        out.append((typ, text))
    return out


def _is_plain_paragraph_line(s):
    if not s:
        return False
    if s[0] in "#>!-":
        return False
    if re.match(r"^\d+\.\s", s):
        return False
    return True


def drop_residual_fragments(buf):
    """Final cleanup pass, run after both stitchers: any plain-paragraph
    line that's still short and unpunctuated at this point had no
    reachable continuation anywhere nearby, so it's not a truncated real
    sentence -- it's diagram-label debris (box labels, Yes/No decision
    branches, lettered checklist fragments) that the embedded page image
    already shows. Headings, bullets, quotes and images are untouched.
    """
    out = []
    for s in buf:
        if _is_plain_paragraph_line(s) and para_is_fragment(s):
            continue
        out.append(s)
    return out


def stitch_cross_page_sentences(buf, window=40):
    """Same problem as merge_split_sentences, but for splits that land on
    either side of a page boundary: a sentence cut off by a sidebar figure
    that runs to the bottom of a page, continuing at the top of the next
    page's rendered content (after that page's own heading/bullets/image).
    """
    out = list(buf)
    i = 0
    while i < len(out):
        s = out[i]
        is_bullet_source = s.startswith("- ")
        if (_is_plain_paragraph_line(s) or is_bullet_source) and word_count(s) >= 10 and not s.rstrip().endswith((".", "!", "?", "”", '"', ":", ";", ")")):
            # Same reasoning as merge_split_sentences: bullets often
            # legitimately end on a stranded preposition, so only merge a
            # bullet source when the continuation unambiguously starts
            # lowercase; the case-independent bypass is plain-paragraph-only.
            definitely_cut = (not is_bullet_source) and bool(ENDS_WITH_CONNECTIVE_RE.search(s.rstrip()))
            for j in range(i + 1, min(i + 1 + window, len(out))):
                t = out[j]
                if t == "":
                    continue
                if _is_plain_paragraph_line(t):
                    if word_count(t) < 10:
                        continue  # too short to be a real paragraph (e.g. a figure caption) -- keep scanning
                    if definitely_cut or t[:1].islower():
                        out[i] = s.rstrip() + " " + t
                        del out[j]
                    break
        i += 1
    return out


LIST_ITEM_RE = re.compile(r"^(-|\d+\.)\s")


def collapse_list_page_breaks(buf):
    """Each page's rendered content is followed by a blank-line spacer in
    buf (so unrelated blocks stay visually separated). If a list happens
    to continue right across that page boundary, the spacer lands between
    two list items and produces a loose (blank-line-separated) list even
    though join_blocks tight-joins adjacent list items everywhere else.
    Drop exactly those spacers.
    """
    out = list(buf)
    i = 1
    while i < len(out) - 1:
        if out[i] == "" and LIST_ITEM_RE.match(out[i - 1] or "") and LIST_ITEM_RE.match(out[i + 1] or ""):
            del out[i]
            continue
        i += 1
    return out


def join_blocks(blocks):
    parts = [b for b in blocks]
    out = []
    for i, b in enumerate(parts):
        if i > 0:
            prev = parts[i - 1]
            sep = "\n" if LIST_ITEM_RE.match(prev) and LIST_ITEM_RE.match(b) else "\n\n"
            out.append(sep)
        out.append(b)
    return "".join(out)


def main():
    if not os.path.exists(FULL):
        build_text_extraction()
    build_figure_images(FIGURE_PRINTED_PAGES)

    with open(FULL, encoding="utf-8") as f:
        pages = f.read().split("\f")
    if pages and pages[-1].strip() == "":
        pages = pages[:-1]

    available_images = set(os.listdir(IMG_DIR))

    chapters = [
        ("00-front-matter", 1, 32),
        ("01-chapter-1-introduction-to-toc", 33, 62),
        ("02-chapter-2-categories-of-legitimate-reservation", 63, 98),
        ("03-chapter-3-intermediate-objectives-map", 99, 120),
        ("04-chapter-4-current-reality-tree", 121, 190),
        ("05-chapter-5-evaporating-cloud", 191, 236),
        ("06-chapter-6-future-reality-tree", 237, 290),
        ("07-chapter-7-prerequisite-and-transition-trees", 291, 342),
        ("08-chapter-8-changing-the-status-quo", 343, 370),
        ("09-back-matter", 371, 436),  # stops before the Index (printed p.405+) -- not useful in a digital edition
    ]

    for fname, start, end in chapters:
        buf = []
        for phys in range(start, end + 1):
            idx = phys - 1
            if idx >= len(pages):
                break
            printed = phys - 32
            body = strip_page_furniture(pages[idx])
            body = merge_drop_cap(body)
            items = classify_and_reflow(body)

            heading_lines = []
            suppress = []
            if phys in FRONT_MATTER_INJECT_BY_PHYSICAL:
                heading_lines = FRONT_MATTER_INJECT_BY_PHYSICAL[phys]
            elif printed in INJECTED_HEADINGS:
                heading_lines, suppress = INJECTED_HEADINGS[printed]
            items = suppress_title_dupes(items, suppress)

            img_name = f"p{printed:03d}.png" if printed > 0 else None
            has_img = img_name in available_images
            items = drop_orphan_headings(items, has_img)
            if has_img and items and not any(_is_substantial(it) for it in items):
                # No item on this page reads as real prose (>=10 words,
                # ends in terminal punctuation) -- the whole page is almost
                # certainly a flowchart/decision-tree figure (labels,
                # Yes/No branches, lettered checklist items), and the
                # embedded image already shows it. Unlike the bulk
                # drop_all_p heuristic this replaced, this only fires when
                # there is no substantial paragraph to protect anywhere on
                # the page, so it can't eat a real sentence.
                items = []
            rendered = render_items(items, has_img)
            if 397 <= printed <= 400:
                new_rendered = []
                for line in rendered:
                    if line.startswith("#") or line.startswith(">"):
                        new_rendered.append(line)
                    else:
                        new_rendered.extend(split_glossary_entries(line))
                rendered = new_rendered

            if not rendered and not has_img and not heading_lines:
                continue

            if heading_lines:
                buf.extend(heading_lines)
                buf.append("")
            if has_img:
                buf.append(f"![page {printed}](images/{img_name})")
                buf.append("")
            buf.extend(rendered)
            buf.append("")
        out_path = os.path.join(OUT_DIR, fname + ".md")
        buf = stitch_cross_page_sentences([x for x in buf if x is not None])
        buf = drop_residual_fragments(buf)
        buf = collapse_list_page_breaks(buf)
        text = join_blocks(buf)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = text.replace(
            "An element of the Prerequisite Tree (PRT) and the Intermediate Objectives (IO) Map.\n\nintermediate objectives (IO)\n\n**map**",
            "An element of the Prerequisite Tree (PRT) and the Intermediate Objectives (IO) Map.\n\n**intermediate objectives (IO) map**",
        )
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print("wrote", out_path)


if __name__ == "__main__":
    main()
