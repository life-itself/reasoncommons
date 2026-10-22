"""HTML for the site of commons. Every page is complete without JavaScript.

Editorial text (introductions, captions, the six questions) orients the reader; the
statements and connections of record are always shown in their published wording,
with their standing, contributors and endorsers.
"""
from collections import defaultdict
from datetime import date
import html

import diagrams

TREE_ORDER = ["goal", "current_reality", "conflict", "future_reality", "prerequisite", "transition"]
TREES = {
    "goal": {"slug": "goal", "step": "The goal", "question": "What are we trying to achieve?",
             "about": "The goal, and what has to be true for it.",
             "read": "Read from the top down: the goal needs each condition beneath it.",
             "method": "goal tree", "next": "Next: what stands in the way of those conditions."},
    "current_reality": {"slug": "in-the-way", "step": "In the way", "question": "What stands in the way?",
                        "about": "What is happening now, and why.",
                        "read": "Read from the bottom up: each arrow means “contributes to”.",
                        "method": "current reality tree", "next": "Next: the conflict that keeps the problem in place."},
    "conflict": {"slug": "conflict", "step": "Pulling apart", "question": "Where do needs pull two ways?",
                 "about": "Two needs that both serve one objective, and positions that rule each other out.",
                 "read": "Read from right to left: each position is held to meet a need, and both needs serve the objective on the left.",
                 "method": "conflict cloud, also called an evaporating cloud", "next": "Next: the change that gets past the conflict."},
    "future_reality": {"slug": "change", "step": "The change", "question": "What will we change?",
                       "about": "The change, and what it should lead to.",
                       "read": "Read from the bottom up: from each change to the effects it should have.",
                       "method": "future reality tree", "next": "Next: what has to happen before the change can work."},
    "prerequisite": {"slug": "prerequisites", "step": "First steps", "question": "What has to happen first?",
                     "about": "What stands in the way of the change, and what gets past it.",
                     "read": "Read from the top down: the objective needs each step beneath it, and each step overcomes the obstacle below it.",
                     "method": "prerequisite tree", "next": "Next: who does what."},
    "transition": {"slug": "actions", "step": "Actions", "question": "Who does what?",
                   "about": "Actions, and what each should achieve.",
                   "read": "Read from the bottom up: each action should produce the effect above it.",
                   "method": "transition tree", "next": "Back to the start: each action should move a condition for the goal forward."},
}
KIND_LABELS = {"goal": "Goal", "critical_success_factor": "Success factor", "necessary_condition": "Condition",
               "undesirable_effect": "Problem", "cause": "Cause", "observation": "Observation", "objective": "Objective",
               "need": "Need", "prerequisite": "Position", "injection": "Change", "existing_condition": "Already true",
               "predicted_effect": "Expected effect", "desirable_effect": "Desired effect", "obstacle": "Obstacle",
               "intermediate_objective": "Step", "action": "Action", "expected_effect": "Expected effect"}
SPECIAL_KINDS = {("future_reality", "undesirable_effect"): "Possible harm", ("conflict", "objective"): "Shared objective"}
PLURALS = {"Goal": "Goals", "Success factor": "Success factors", "Condition": "Conditions", "Problem": "Problems",
           "Cause": "Causes", "Observation": "Observations", "Objective": "Objectives", "Shared objective": "Shared objectives",
           "Need": "Needs", "Position": "Positions", "Change": "Changes", "Already true": "Already true",
           "Expected effect": "Expected effects", "Desired effect": "Desired effects", "Possible harm": "Possible harms",
           "Obstacle": "Obstacles", "Step": "Steps", "Action": "Actions"}
ROLE_ORDER = {"goal": ["goal", "critical_success_factor", "necessary_condition"],
              "current_reality": ["undesirable_effect", "cause"],
              "conflict": ["objective", "need", "prerequisite"],
              "future_reality": ["injection", "existing_condition", "predicted_effect", "desirable_effect", "undesirable_effect"],
              "prerequisite": ["objective", "obstacle", "intermediate_objective"],
              "transition": ["action", "need", "existing_condition", "expected_effect"]}
STANDING = {"accepted": "Accepted for now", "proposed": "Proposed", "disputed": "Disputed"}
VERDICTS = {"observed": "Observed", "not_observed": "Not observed", "unclear": "Unclear", "not_assessed": "Not assessed",
            "unavailable": "Unavailable", "awaiting": "Awaiting report"}
READINESS = {"experienced": "Has experienced the change", "not_yet": "Not yet experienced", "cannot_assess": "Cannot assess"}
WORK_GROUPS = [("Explain or connect", {"connect_or_explain"}), ("Check an assumption", {"examine_assumption"}),
               ("Examine a challenge", {"resolve_challenge"}), ("Find out what happens", {"review_feedback", "test_causality"})]
CHANGE_WORDS = {"added": "Added", "revised": "Reworded", "disputed": "Disputed", "accepted": "Accepted", "removed": "Removed", "report": "Reports"}
TRACE_WORDS = {"addresses": "Meant to address", "derived_from": "Developed from", "implements": "Puts into practice"}


def esc(value):
    return html.escape(str(value), quote=True)


def kind_label(tree, kind):
    return SPECIAL_KINDS.get((tree, kind), KIND_LABELS.get(kind, kind.replace("_", " ").capitalize()))


def names(items):
    items = list(dict.fromkeys(items))
    if len(items) < 2:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def plural(n, word, words=None):
    return f"{n} {word if n == 1 else (words or word + 's')}"


def day(value):
    stamp = date.fromisoformat(value[:10])
    return f"{stamp.day} {stamp.strftime('%B %Y')}"


def short_day(value):
    stamp = date.fromisoformat(value[:10])
    return stamp.day, stamp.strftime("%b %Y")


# ---------------------------------------------------------------- indexes over one commons

class Commons:
    def __init__(self, data):
        self.__dict__.update(data)
        self.items, self.tree_of, self.order = {}, {}, []
        for name, tree in self.trees.items():
            for item in tree["nodes"] + tree["links"]:
                self.items[item["id"]] = item
                self.tree_of[item["id"]] = name
                self.order.append(item["id"])
        self.reports = {r["id"]: (req, r) for req in self.feedback for r in req["reports"]}
        self.backlog = defaultdict(list)
        for tree in self.trees.values():
            for task in tree["backlog"]:
                self.backlog[task["ref"]].append(task)

    def is_link(self, ident):
        return "relation" in self.items[ident]

    def kind_of(self, ident):
        item = self.items[ident]
        return "Connection" if self.is_link(ident) else kind_label(self.tree_of[ident], item["kind"])

    def text(self, ident):
        item = self.items[ident]
        if not self.is_link(ident):
            return item["text"]
        sources = " and ".join(f"“{self.items[s]['text']}”" for s in item["from"])
        return f"{sources} {diagrams.RELATIONS.get(item['relation'], item['relation'])} “{self.items[item['to']]['text']}”"

    def short(self, ident):
        item = self.items[ident]
        return item.get("label") or item["text"] if not self.is_link(ident) else self.text(ident)

    def href(self, ident, here="commons"):
        return ("" if here == "commons" else f'{self.slug}/') + f"items.html#{ident}"

    def counts(self, standing=None):
        nodes = [n for t in self.trees.values() for n in t["nodes"] if standing in (None, n["status"])]
        links = [l for t in self.trees.values() for l in t["links"] if standing in (None, l["status"])]
        return len(nodes), len(links)

    def open_items(self):
        owners = [i for i in self.order if self.backlog.get(i) or self.items[i]["status"] == "disputed"]
        return owners

    def shapes(self, name):
        """Diagram geometry for each connected part of a tree, and the statements with no connection."""
        tree = self.trees[name]
        label = lambda kind: kind_label(name, kind)
        pieces, loose = diagrams.components(tree)
        shapes = [diagrams.geometry(tree, p["ids"], p["links"], label) for p in pieces]
        cloud_only = not tree["links"] and name == "conflict" and diagrams.cloud_roles({n["id"]: n for n in tree["nodes"]}, [])
        if cloud_only:
            shapes = [diagrams.geometry(tree, loose, [], label)]
            loose = []
        return pieces, shapes, loose


# ---------------------------------------------------------------- shared components

LOGO = ('<svg viewBox="0 0 32 36" width="26" height="30" aria-hidden="true"><path d="M16 33V17M16 24L5 15M16 18L26 8M16 13V4" '
        'fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="5" cy="13" r="4" fill="currentColor"/>'
        '<circle cx="26" cy="6" r="4" fill="currentColor"/><circle cx="16" cy="4" r="3.5" fill="currentColor"/></svg>')


def chip(status, prior=None):
    if status == "accepted":
        return '<span class="chip chip-accepted"><svg viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 6.2l2.3 2.4 4.7-5.2"/></svg>Accepted for now</span>'
    return f'<span class="chip chip-{status}">{STANDING[status]}</span>'


def endorsement(item):
    people = item.get("accepted_by", [])
    if item["status"] == "accepted":
        return f"Accepted for now by {names(people)}"
    if item["status"] == "disputed":
        return f"Disputed; earlier accepted by {names(people)}" if people else "Disputed"
    return f"Proposed by {names(c['name'] for c in item['contributors'])}"


def card(c, ident, tree=None, extra=""):
    item = c.items[ident]
    tree = tree or c.tree_of[ident]
    return (f'<a class="card role-{item["kind"]} is-{item["status"]}" href="items.html#{ident}">'
            f'<span class="card-top"><span class="kind">{esc(kind_label(tree, item["kind"]))}</span>{chip(item["status"])}</span>'
            f'<span class="card-text">{esc(item["text"])}</span>{extra}'
            f'<span class="card-foot">{esc(endorsement(item))}</span></a>')


def figure(svg, label, caption="", width=None):
    cap = f"<figcaption>{caption}</figcaption>" if caption else ""
    size = f' style="--w:{width + 24}px"' if width else ""
    return (f'<figure class="dg"{size}><div class="dg-scroll" tabindex="0" role="region" aria-label="{esc(label)}">{svg}</div>{cap}</figure>')


def loose_groups(c, name, ids, heading=True):
    groups = defaultdict(list)
    for ident in ids:
        groups[c.items[ident]["kind"]].append(ident)
    order = ROLE_ORDER[name] + ["observation"]
    blocks = []
    for kind in sorted(groups, key=lambda k: order.index(k) if k in order else 99):
        label = kind_label(name, kind)
        cards = "".join(card(c, i, name) for i in groups[kind])
        blocks.append(f'<div class="group"><h4>{esc(PLURALS.get(label, label))} <span>{len(groups[kind])}</span></h4><div class="cards">{cards}</div></div>')
    return f'<div class="groups">{"".join(blocks)}</div>'


def legend(c, name, shapes):
    tree = c.trees[name]
    kinds = []
    for node in tree["nodes"]:
        if node["kind"] not in kinds:
            kinds.append(node["kind"])
    order = ROLE_ORDER[name] + ["observation"]
    kinds.sort(key=lambda k: order.index(k) if k in order else 99)
    parts = [f'<span class="lg role-{k}"><i></i>{esc(kind_label(name, k))}</span>' for k in kinds]
    standings = {i["status"] for i in tree["nodes"] + tree["links"]}
    for status in ("accepted", "proposed", "disputed"):
        if status in standings and len(standings) > 1 or status != "accepted" and status in standings:
            parts.append(f'<span class="lg lg-{status}"><i></i>{STANDING[status]}</span>')
    if any(len(l["from"]) > 1 for l in tree["links"]):
        parts.append('<span class="lg lg-and"><i>and</i>Joint conditions</span>')
    if any(l["relation"] == "overcomes" for l in tree["links"]):
        parts.append('<span class="lg lg-down"><i></i>Overcomes</span>')
    if any(l["relation"] == "precedes" for l in tree["links"]):
        parts.append('<span class="lg lg-then"><i></i>Comes before</span>')
    if any(l["relation"] == "conflicts_with" for l in tree["links"]):
        parts.append('<span class="lg lg-clash"><i></i>Conflict</span>')
    return f'<div class="legend" aria-label="Key">{"".join(parts)}</div>'


def strip(c, prefix=""):
    """The shape of every question in one row: the real topology, drawn small."""
    cells = []
    for i, name in enumerate(TREE_ORDER, 1):
        if name not in c.trees:
            continue
        pieces, shapes, loose = c.shapes(name)
        n, l = len(c.trees[name]["nodes"]), len(c.trees[name]["links"])
        thumb = diagrams.thumbnail(shapes, [c.items[x] for x in loose], 120, 74)
        cells.append(f'<a class="strip-cell" href="{prefix}{TREES[name]["slug"]}.html">{thumb}<span class="strip-label"><b>{i}</b> {esc(TREES[name]["step"])}</span>'
                     f'<span class="strip-count">{n} · {l}</span></a>')
    return f'<div class="strip" aria-label="Six questions: statements and connections in each">{"".join(cells)}</div>'


def brief(c, ident, site):
    item = c.items[ident]
    name = c.tree_of[ident]
    url = f'{site["base_url"]}{c.slug}/items.html#{ident}'
    if c.is_link(ident):
        wording = "\nAND\n".join(c.items[s]["text"] for s in item["from"]) + f"\n{diagrams.RELATIONS.get(item['relation'], item['relation'])}\n" + c.items[item["to"]]["text"]
        noun = "connection"
    else:
        wording, noun = item["text"], "statement"
    standing = {"accepted": f"accepted for now by {names(item['accepted_by'])}",
                "proposed": f"proposed by {names(x['name'] for x in item['contributors'])}",
                "disputed": "disputed" + (f" (earlier accepted by {names(item['accepted_by'])})" if item["accepted_by"] else "")}[item["status"]]
    if c.is_example:
        opening = f"This is the fictional example commons on the Reason Commons demonstration site; its people and reports are invented. I want to practise developing a contribution about one {noun}."
        closing = ("Use the reason-commons skill if you have it, and treat this as practice: there is no shared record behind this example. "
                   "Help me work out a question, an observation or a challenge, and keep it as a draft. Copying this brief submits nothing.")
    elif c.is_reconstruction:
        opening = f"I'm reading Gandhi 2.0, a proposed AI reconstruction from supplied analyses of a real discussion, and want to develop a contribution about one {noun}. The original participants have not endorsed this map."
        closing = ("Use the reason-commons skill if available. Check the cited analysis and, if accessible, the original passage before attributing the claim to a participant. "
                   "Help me develop a question, correction or challenge as a draft; don't treat my interest as endorsement or invent a trial commitment. Copying this brief submits nothing.")
    else:
        opening = f"I'm reading a commons on the Reason Commons demonstration site and want to develop a contribution about one {noun}."
        closing = ("Use the reason-commons skill if you have it. First establish who I am and whether I can reach the current working record, "
                   "and check whether this item has changed since this release before proposing anything. Help me work out a question, an observation "
                   "or a challenge; don't assume I endorse the item. If I can't reach the shared record, help me keep a draft. Copying this brief submits nothing.")
    locators = "" if not c.is_reconstruction else "\nSource locators: " + "; ".join(f'{ref["source_id"]}: {ref["locator"]} ({ref["basis"]})' for ref in item["source_refs"])
    return (f"{opening}\n\nCommons: {c.title}\nRelease: {c.release_id}, published {day(c.date)}\nQuestion: {TREES[name]['question']}\n"
            f"Item: {ident} ({c.kind_of(ident)})\nStanding in this release: {standing}{locators}\n\n{wording}\n\nPublic page: {url}\n\n{closing}")


# ---------------------------------------------------------------- page shell

def shell(*, title, description, depth, body, nav=None, c=None, page="", head=""):
    up = "../" * depth
    links = [("index.html#commons", "Commons", "commons"), ("how-it-works.html", "How it works", "how")]
    current = ' aria-current="page"'
    nav_html = "".join(f'<a href="{up}{href}"{current if key == nav else ""}>{label}</a>' for href, label, key in links)
    banner = ""
    if c and c.is_example:
        banner = (f'<div class="example-banner" role="note"><div class="wrap"><strong>Fictional example.</strong> The school, its people and their reports are invented, '
                  f'to show everything a commons can hold. <a href="{up}reason-commons/index.html">See a real commons →</a></div></div>')
    elif c and c.is_reconstruction:
        banner = ('<div class="reconstruction-banner" role="note"><div class="wrap"><strong>Source reconstruction · Proposed.</strong> '
                  'Prepared by AI from supplied analyses. The discussion participants have not endorsed this map. '
                  '<a href="about.html#sources">Sources and limits →</a></div></div>')
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{esc(description)}">
<meta name="theme-color" content="#f7f4ec">
<title>{esc(title)}</title>
<link rel="stylesheet" href="{up}styles.css">
<script src="{up}app.js" defer></script>{head}
</head>
<body class="page-{page}{' is-example' if c and c.is_example else ''}{' is-reconstruction' if c and c.is_reconstruction else ''}">
<a class="skip" href="#main">Skip to content</a>
{banner}<header class="site-head"><div class="wrap">
<a class="brand" href="{up}index.html">{LOGO}<span>Reason Commons</span></a>
<nav class="site-nav" aria-label="Site">{nav_html}<a class="nav-cta" href="/skills">Try the skill <span aria-hidden="true">↗</span></a></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="site-foot"><div class="wrap">
<div><a class="brand foot-brand" href="{up}index.html">{LOGO}<span>Reason Commons</span></a><p>Thinking that accumulates.<br>A collaboration between Rufus Pollock and David Joseph.</p></div>
<nav aria-label="Further reading"><a href="/explainers">Read the series</a><a href="/ltp">The method underneath</a><a href="/skills">Use the skill</a><a href="/about">About</a><a href="/demos">More demos</a></nav>
<p class="foot-note">A static, read-only demonstration. Nothing here is live, and nothing you do here is sent anywhere. <a href="/">Back to the main site ↗</a></p>
</div></footer>
</body>
</html>
"""


def publication_tag(c):
    if c.is_reconstruction:
        return '<span class="tag tag-reconstruction">Source reconstruction · Proposed</span>'
    return ('<span class="tag tag-example">Fictional example</span>' if c.is_example
           else '<span class="tag tag-real">Real commons</span>')


def commons_head(c, tab, heading=None):
    tag = publication_tag(c)
    statements, connections = c.counts()
    tabs = [("index.html", "Overview", "overview", ""), ("map.html", "Map", "map", "6 questions"),
            ("items.html", "Statements", "items", str(statements + connections))]
    if c.open_items():
        tabs.append(("questions.html", "Open questions", "questions", str(len(c.open_items()))))
    if c.feedback:
        tabs.append(("learning.html", "Learning", "learning", plural(sum(len(r["reports"]) for r in c.feedback), "report")))
    tabs += [("changes.html", "Changes", "changes", plural(len(c.history), "release")), ("about.html", "About", "about", "")]
    current = ' aria-current="page"'
    tab_html = "".join(f'<a href="{href}"{current if key == tab else ""}>{label}{f" <span>{esc(count)}</span>" if count else ""}</a>'
                       for href, label, key, count in tabs)
    title = f'<h1 class="ch-title">{esc(c.name)}</h1>' if heading is None else f'<p class="ch-title">{esc(c.name)}</p>'
    return (f'<div class="ch"><div class="wrap">'
            f'<nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html#commons">Commons</a><span aria-hidden="true">/</span><span>{esc(c.name)}</span></nav>'
            f'<div class="ch-row"><div>{tag}{title}<p class="ch-by">{esc(c.byline)}</p></div>'
            f'<p class="ch-meta">Published {day(c.date)}<br><span>Release {esc(c.release_id)}</span></p></div>'
            f'<nav class="tabs" aria-label="This commons">{tab_html}</nav></div></div>')


# ---------------------------------------------------------------- home

def home(site, commons):
    cards = []
    for c in commons:
        goal = next((n for n in c.trees.get("goal", {"nodes": []})["nodes"] if n["kind"] == "goal"), None)
        statements, connections = c.counts()
        mix = sorted({i["status"] for t in c.trees.values() for i in t["nodes"] + t["links"]}, key=list(STANDING).index)
        standing = "all accepted for now" if mix == ["accepted"] else ", ".join(STANDING[s].lower().replace(" for now", "") for s in mix)
        tag = publication_tag(c)
        quote = f'<blockquote class="cc-goal"><span>The goal</span>{esc(goal["text"])}</blockquote>' if goal else ""
        cards.append(f'<article class="cc{" cc-example" if c.is_example else ""}">'
                     f'<div class="cc-head">{tag}<h3><a href="{c.slug}/index.html">{esc(c.name)}</a></h3><p class="cc-by">{esc(c.byline)}</p></div>'
                     f'<p class="cc-summary">{esc(c.summary)}</p>{quote}{strip(c, c.slug + "/")}'
                     f'<p class="cc-meta">{plural(statements, "statement")} · {plural(connections, "connection")} · {esc(standing)}<br>Published {day(c.date)}</p>'
                     f'<a class="button" href="{c.slug}/index.html">Open this commons <span aria-hidden="true">→</span></a></article>')
    cards.append('<article class="cc cc-yours"><div class="cc-head"><span class="tag tag-yours">Yours</span><h3>Start a commons</h3></div>'
                 '<p class="cc-summary">Bring a goal you share with other people. In conversation, the Reason Commons skill helps you structure the thinking and keeps the record: what you agree, what is still open, and who said what.</p>'
                 '<ol class="cc-steps"><li>Install the skill in your AI</li><li>Describe the goal and what makes it hard</li><li>Accept what you can build on, together</li></ol>'
                 '<a class="button button-quiet" href="/skills">Get the skill <span aria-hidden="true">↗</span></a></article>')
    questions = "".join(f'<li><span class="q-n">{i}</span><span class="q-t">{esc(TREES[n]["question"])}</span><span class="q-a">{esc(TREES[n]["about"])}</span></li>'
                        for i, n in enumerate(TREE_ORDER, 1))
    real = next(c for c in commons if c.kind == "real")
    example = next((c for c in commons if c.is_example), None)
    body = f"""<section class="hero"><div class="wrap hero-grid">
<div class="hero-copy">
<p class="eyebrow"><span class="dot" aria-hidden="true"></span>A demonstration of Reason Commons</p>
<h1>Common goals,<br><em>reasoned in the open.</em></h1>
<p class="lede">A commons is a goal and the reasoning a group builds around it: what it depends on, what stands in the way, where needs pull apart, and what the group decides to do. Groups build a commons in ordinary conversation with an AI, using the Reason Commons skill. This site is where anyone can read one.</p>
<div class="actions"><a class="button" href="{real.slug}/index.html">Read our commons <span aria-hidden="true">→</span></a>{f'<a class="button button-quiet" href="{example.slug}/index.html">See the worked example</a>' if example else ''}</div>
</div>
<aside class="hero-path" aria-label="The six questions a commons answers"><p class="path-title">Every commons answers six questions</p><ol class="path">{questions}</ol><p class="path-foot">Each answer sets up the next.</p></aside>
</div></section>
<section class="band" id="commons" aria-labelledby="commons-heading"><div class="wrap">
<div class="band-head"><h2 id="commons-heading">Commons on this site</h2><p>Read accepted reasoning from our own collaboration, a proposed reconstruction from a Second Renaissance discussion, and an invented example that includes a trial and reports. Each record says where it comes from and who has accepted what.</p></div>
<div class="cc-grid">{"".join(cards)}</div>
</div></section>
<section class="band band-steps" aria-labelledby="made-heading"><div class="wrap">
<div class="band-head"><h2 id="made-heading">How a commons gets made</h2><p>The site is read-only. All the thinking happens in conversation, where the skill keeps the record.</p></div>
<ol class="steps">
<li><span>1</span><h3>Talk it through</h3><p>A group works on a shared goal in ordinary conversations with an AI. The skill turns what people say into statements and connections, and keeps track of who said what.</p></li>
<li><span>2</span><h3>Accept what you can build on</h3><p>Named people accept statements and connections for now. Proposals stay marked as proposals, and objections are kept as disputes.</p></li>
<li><span>3</span><h3>Publish a selection</h3><p>The group decides what to make public. Each release keeps earlier wording, so anyone can see how the thinking changed.</p></li>
<li><span>4</span><h3>Read, then respond</h3><p>Anyone can read a commons here. To add to one, copy a statement's brief into your own AI. Nothing is posted from this site.</p></li>
</ol>
<p class="steps-more"><a class="text-link" href="how-it-works.html">How it works, in more detail →</a></p>
</div></section>"""
    redirect = """
<script>(function(){var q=new URLSearchParams(location.search),v=q.get('view'),i=q.get('item');if(!v&&!i)return;
var t={goal:'goal',current_reality:'in-the-way',conflict:'conflict',future_reality:'change',prerequisite:'prerequisites',transition:'actions'};
var p='reason-commons/';p+=i?'items.html#'+encodeURIComponent(i):v==='record'?'about.html':v==='reasoning'?(t[q.get('tree')]||'map')+'.html':'index.html';location.replace(p);})();</script>"""
    return shell(title="Commons · Reason Commons", description="Read shared goals and the reasoning groups build around them with the Reason Commons skill.",
                 depth=0, body=body, nav="commons", page="home", head=redirect)


# ---------------------------------------------------------------- how it works

def how_it_works(site, commons):
    rows = "".join(f'<tr><th scope="row"><span class="q-n">{i}</span>{esc(TREES[n]["question"])}</th><td>{esc(TREES[n]["about"])}</td><td>{esc(TREES[n]["method"]).capitalize()}</td><td>{esc(TREES[n]["read"])}</td></tr>'
                   for i, n in enumerate(TREE_ORDER, 1))
    toy = {"name": "current_reality", "nodes": [
        {"id": "toy-a", "kind": "cause", "text": "Parents drive on their way to work.", "status": "accepted"},
        {"id": "toy-b", "kind": "cause", "text": "There is nowhere near the gate to stop.", "status": "accepted"},
        {"id": "toy-c", "kind": "undesirable_effect", "text": "Cars double-park at the gate.", "status": "accepted"}],
        "links": [{"id": "toy-l", "from": ["toy-a", "toy-b"], "to": "toy-c", "relation": "contributes_to", "status": "accepted"}]}
    shape = diagrams.geometry(toy, ["toy-a", "toy-b", "toy-c"], toy["links"], lambda k: kind_label("current_reality", k))
    toy_svg = diagrams.svg(shape, {n["id"]: n for n in toy["nodes"]}, lambda i: "#joint", "Two causes acting together on one problem").replace("<a ", "<g ").replace("</a>", "</g>")
    standing_cards = "".join(f'<div class="sc sc-{s}">{chip(s)}<p>{t}</p></div>' for s, t in (
        ("accepted", "Named people are willing to build on it for now. It records their judgement at the time, not proof, and not that everyone agrees."),
        ("proposed", "Someone has put it forward and no one has accepted it yet. It is part of the conversation, not part of the agreement."),
        ("disputed", "Someone has raised a substantive objection. Earlier acceptance is kept as history, and the objection is shown beside it.")))
    body = f"""<section class="page-head"><div class="wrap">
<p class="eyebrow">How it works</p>
<h1>How a commons works</h1>
<p class="lede">A commons keeps a group's reasoning about one goal: what they've agreed, what is still open, and who said what. The reasoning is built in conversations with an AI and published here as a read-only record.</p>
</div></section>
<section class="band"><div class="wrap">
<div class="band-head"><h2>Six questions, one method</h2><p>Underneath is the Logical Thinking Process, a set of thinking tools from the Theory of Constraints. Each of its six tools answers one of the questions a commons asks, and each answer sets up the next. <a class="text-link" href="/ltp">More on the method ↗</a></p></div>
<div class="table-wrap"><table class="method"><thead><tr><th scope="col">Question</th><th scope="col">What it shows</th><th scope="col">The method's name</th><th scope="col">How to read it</th></tr></thead><tbody>{rows}</tbody></table></div>
</div></section>
<section class="band" id="joint"><div class="wrap split">
<div><h2>Statements and connections</h2><p>Each statement has one role, such as a problem, a cause, a need or a change, and the diagrams colour it by that role. A connection says how statements relate: one contributes to another, is needed for it, or overcomes it.</p><p>When a connection has several sources, they act <em>together</em>. The diagrams join them at an “and” before the single arrow, so they never look like separate, sufficient causes. Statements with no published connection are grouped by role, and no arrow is ever drawn that the group hasn't recorded.</p></div>
{figure(toy_svg, "An example of a joint connection", "Two causes acting together, adapted from the fictional example.")}
</div></section>
<section class="band"><div class="wrap">
<div class="band-head"><h2>Accepted, proposed, disputed</h2><p>Every statement and connection carries one standing. It is spelled out in words and shown by the border, never by colour alone.</p></div>
<div class="sc-grid">{standing_cards}</div>
</div></section>
<section class="band"><div class="wrap split">
<div><h2>Who said what</h2><p>Each item records who contributed the idea and, separately, who accepted it. An idea suggested by the AI is attributed to the AI. Only named people can accept anything, and imported material whose author is unknown says so.</p></div>
<div><h2>What gets published</h2><p>A group decides what to make public and publishes it as a release. Each release keeps earlier wording, so the Changes page can show how the thinking moved. The site is a snapshot, not a live feed: the working record stays with the group.</p><p>A <strong>source reconstruction</strong> is different: the AI has drafted a map from supplied material, and the original participants have not endorsed it. Its items stay proposed, with source locators and explicit inferences. Gandhi 2.0 is such a reconstruction.</p></div>
</div></section>
<section class="band band-cta"><div class="wrap split">
<div><h2>Taking part</h2><p>Every statement page has a brief you can copy into your own AI. The skill then checks the current record before helping you develop an observation, a question or a challenge. Copying a brief submits nothing, and this site never edits a commons.</p></div>
<div class="cta-box"><h3>Start your own commons</h3><p>All you need is a goal you share with others and an AI that can use the skill.</p><a class="button" href="/skills">Get the skill <span aria-hidden="true">↗</span></a></div>
</div></section>"""
    return shell(title="How it works · Reason Commons", description="How a commons is built in conversation, what its six questions are, and what accepted, proposed and disputed mean.",
                 depth=0, body=body, nav="how", page="how")


# ---------------------------------------------------------------- overview

def reconstruction_outline(c, name, ids, links):
    tree = c.trees[name]
    rendered = diagrams.outline(tree, ids, links, c.href, lambda kind: kind_label(name, kind))
    for link in links:
        if link["relation"] == "conflicts_with":
            target = f'<a href="{esc(c.href(link["to"]))}">{esc(c.items[link["to"]]["text"])}</a>'
            rendered = rendered.replace(f'<p class="o-then">then → {target}</p>',
                                        f'<p class="o-then"><a class="o-rel is-{link["status"]}" href="{esc(c.href(link["id"]))}">conflicts with</a> {chip(link["status"])} {target}</p>')
    return rendered


def reconstruction_overview(c, site):
    goal = next(n for n in c.trees["goal"]["nodes"] if n["kind"] == "goal")
    statements, connections = c.counts()
    conditions = "".join(card(c, ident) for ident in ("g2-g-capability", "g2-g-control", "g2-g-future"))
    _, shapes, _ = c.shapes("conflict")
    cloud = "".join(figure(diagrams.svg(s, {n["id"]: n for n in c.trees["conflict"]["nodes"]}, c.href, "AI capability and resilient autonomy: a proposed conflict"), "Proposed conflict: AI capability and resilient autonomy", "The dashed connections are proposed. The two positions concern the same essential function; inspect each connection to question its assumption.") for s in shapes)
    tree = c.trees["conflict"]
    outline = reconstruction_outline(c, "conflict", [n["id"] for n in tree["nodes"]], tree["links"])
    cloud = ('<div class="view-toggle" role="group" aria-label="Show conflict as" hidden><button type="button" data-view="diagram" aria-pressed="true">Diagram</button><button type="button" data-view="outline" aria-pressed="false">Outline</button></div>'
             f'<div class="views" data-views><div class="view view-diagram">{cloud}</div><div class="view view-outline">{outline}</div></div>')
    body = commons_head(c, "overview") + f'''<div class="wrap overview">
<section class="goal-hero"><div class="gh-main"><p class="eyebrow">The proposed goal</p><p class="gh-text">{esc(goal["text"])}</p><p class="gh-by">{chip("proposed")} <span>Reconstructed by AI; awaiting participant review</span></p><a class="text-link" href="items.html#{goal["id"]}">Inspect the goal →</a></div><div class="gh-side"><p class="eyebrow">From a conversation to a shared question</p><p>{esc(c.description)}</p><p class="gh-count"><b>{statements}</b> proposed statements<br><b>{connections}</b> proposed connections</p><a class="text-link" href="about.html#sources">Where this map comes from →</a></div></section>
<section class="ov"><div class="ov-head"><p class="eyebrow">A place to begin</p><h2>What seems to be shared</h2><p>The analyses report overlapping concerns: useful capabilities, meaningful control and preserving the possibility of a future. These are candidate starting points for review.</p></div><div class="cards cards-grid">{conditions}</div><a class="text-link" href="goal.html">The goal and its proposed conditions →</a></section>
<section class="ov"><div class="ov-head"><p class="eyebrow">Pulling apart</p><h2>Useful capacity, without becoming captive</h2><p>A community needs enough capability to endure. It also needs to keep essential functions running when a provider, power supply or AI fails. Does that really require choosing between dependence on AI and doing without it?</p></div>{cloud}<a class="text-link" href="conflict.html">Inspect the conflict and its assumptions →</a></section>
<section class="ov"><div class="ov-head"><p class="eyebrow">A possible change</p><h2>Try conflict guidance that members can question and leave</h2><p>The proposal is to test useful guidance while members retain control, access to human help and competence without the tool. Confidentiality, fair grievance handling and independent comparison are part of the design.</p></div><div class="cards cards-grid">{card(c, "g2-f-guidance")}{card(c, "g2-f-protections")}</div><a class="text-link" href="change.html">The proposed change and its effects →</a></section>
<section class="ov"><div class="ov-head"><p class="eyebrow">The question to test</p><h2>What would change our minds?</h2><p>Do destructive conflict costs and unnecessary escalation fall, while fair treatment, independent competence and member influence remain? Compare AI guidance with optional-AI and human approaches.</p></div><div class="cards cards-grid">{card(c, "g2-f-benefit")}{card(c, "g2-f-harm")}</div><p>Fewer complaints or higher satisfaction would not settle it. Costs may have moved elsewhere, or justified grievances may have been silenced. Agree the comparison and the results that would defeat the claim before starting.</p><p>A local success would still leave a larger question open: do small democratic groups gain enough relative to hierarchies to change which institutions survive? The supplied analyses do not establish that step.</p><a class="text-link" href="items.html#g2-f-rel-benefit">Inspect the prediction and what remains untested →</a></section>
<section class="ov"><div class="ov-head"><p class="eyebrow">First step · Unassigned</p><h2>Choose one willing host and one function</h2><p>No trial is recorded here. The first task is to establish a bounded case, check what already operates, and agree measures, protections, responsibilities and resources with the people affected. A missing detail in an analysis does not prove that a host lacks it.</p></div><div class="cards cards-grid">{card(c, "g2-t-select")}{card(c, "g2-p-protocol")}</div><a class="text-link" href="prerequisites.html">What has to happen first →</a></section>
<section class="ov"><div class="ov-head"><p class="eyebrow">The wider picture</p><h2>One entry point into a broader programme</h2><p>The sources also explore reflective development, trustworthy governance, model adaptation, voice participation, federation, material services and security. Conflict guidance is one possible starting point. No single global constraint has been established.</p></div>{strip(c)}<p><a class="text-link" href="map.html">Explore all six views →</a></p><p><a class="text-link" href="questions.html">Review the open questions →</a></p></section>
</div>'''
    return shell(title=f"{c.name} · Reason Commons", description=c.summary, depth=1, body=body, nav="commons", c=c, page="overview")


def overview(c, site):
    if c.is_reconstruction:
        return reconstruction_overview(c, site)
    o = c.overview
    goal = next((n for n in c.trees["goal"]["nodes"] if n["kind"] == "goal"), None) if "goal" in c.trees else None
    statements, connections = c.counts()
    blocks = []
    hero = (f'<section class="goal-hero"><div class="gh-main"><p class="eyebrow">The goal</p><p class="gh-text">{esc(goal["text"])}</p>'
            f'<p class="gh-by">{chip(goal["status"])} <span>{esc(endorsement(goal))}</span></p>'
            f'<a class="text-link" href="items.html#{goal["id"]}">Inspect the goal →</a></div>'
            f'<div class="gh-side"><p class="eyebrow">At a glance</p><p class="gh-count"><b>{statements}</b> statements<br><b>{connections}</b> connections</p>'
            f'{strip(c)}<p class="gh-note">{esc(c.description)}</p></div></section>') if goal else ""
    blocks.append(hero)
    if "goal" in c.trees:
        pieces, shapes, loose = c.shapes("goal")
        diagram = "".join(figure(diagrams.svg(s, {n["id"]: n for n in c.trees["goal"]["nodes"]}, c.href, "What the goal depends on"), "Diagram: what the goal depends on") for s in shapes)
        blocks.append(f'<section class="ov"><div class="ov-head"><p class="eyebrow">1 · {esc(TREES["goal"]["step"])}</p><h2>What it depends on</h2><p>{esc(o["conditions"])}</p></div>{diagram}'
                      f'<a class="text-link" href="goal.html">The goal and its conditions →</a></section>')
    if "current_reality" in c.trees:
        tree = c.trees["current_reality"]
        pieces, shapes, loose = c.shapes("current_reality")
        focus = next((s for p, s in zip(pieces, shapes) if o["obstacles_focus"] in p["ids"]), shapes[0] if shapes else None)
        diagram = figure(diagrams.svg(focus, {n["id"]: n for n in tree["nodes"]}, c.href, "What stands in the way"), "Diagram: what stands in the way") if focus else ""
        others = len(tree["nodes"]) - (len(focus["nodes"]) if focus else 0)
        aside = ""
        if o.get("aside_ids"):
            cards = "".join(card(c, i) for i in o["aside_ids"])
            aside = f'<aside class="ov-aside"><p class="eyebrow">{esc(o["aside_title"])}</p><p>{esc(o["aside"])}</p><div class="cards cards-stack">{cards}</div></aside>'
        split = " ov-split" if aside else ""
        blocks.append(f'<section class="ov{split}"><div class="ov-main"><div class="ov-head"><p class="eyebrow">2 · {esc(TREES["current_reality"]["step"])}</p><h2>What stands in the way</h2><p>{esc(o["obstacles"])}</p></div>{diagram}'
                      f'<a class="text-link" href="in-the-way.html">All {plural(len(tree["nodes"]), "statement")} about what stands in the way{f", {others} more than shown" if others else ""} →</a></div>{aside}</section>')
    if "conflict" in c.trees:
        tree = c.trees["conflict"]
        pieces, shapes, loose = c.shapes("conflict")
        cloud = "".join(figure(diagrams.svg(s, {n["id"]: n for n in tree["nodes"]}, c.href, "Where needs pull two ways"), "Diagram: where needs pull two ways") for s in shapes)
        if loose:
            cloud += loose_groups(c, "conflict", loose)
        changes = [n for n in c.trees.get("future_reality", {"nodes": []})["nodes"] if n["kind"] == "injection" and n["status"] == "accepted"]
        change_cards = "".join(card(c, n["id"], "future_reality") for n in changes[:2])
        blocks.append(f'<section class="ov"><div class="ov-head"><p class="eyebrow">3 and 4 · {esc(TREES["conflict"]["step"])}, and {esc(TREES["future_reality"]["step"].lower())}</p><h2>Where needs pulled two ways, and what they chose</h2><p>{esc(o["change"])}</p></div>'
                      f'{cloud}<a class="text-link" href="conflict.html">The conflict →</a>'
                      f'<div class="ov-chosen"><div><p class="eyebrow">The change chosen</p><p>What they decided to do about it.</p><a class="text-link" href="change.html">The change and its effects →</a></div>'
                      f'<div class="cards">{change_cards}</div></div></section>')
    if c.feedback:
        blocks.append(f'<section class="ov"><div class="ov-head"><p class="eyebrow">Learning</p><h2>What happened when they tried it</h2><p>{esc(o["learning"])}</p></div>{trial_matrix(c, c.feedback[0])}'
                      f'<a class="text-link" href="learning.html">Every report, in full →</a></section>')
    owners = c.open_items()
    if owners:
        blocks.append(f'<section class="ov"><div class="ov-head"><p class="eyebrow">Unfinished</p><h2>Open questions</h2><p>{plural(len(owners), "published item")} still {"has" if len(owners) == 1 else "have"} questions to work through.</p></div>'
                      f'{question_board(c, limit=2)}<a class="text-link" href="questions.html">All open questions →</a></section>')
    if "transition" in c.trees:
        actions = [n for n in c.trees["transition"]["nodes"] if n["kind"] == "action"]
        cards = "".join(card(c, n["id"], "transition") for n in actions)
        blocks.append(f'<section class="ov"><div class="ov-head"><p class="eyebrow">6 · {esc(TREES["transition"]["step"])}</p><h2>What they plan to do</h2><p>{esc(o["actions"])}</p></div>'
                      f'<div class="cards cards-grid">{cards}</div><a class="text-link" href="actions.html">Actions and what they should achieve →</a></section>')
    blocks.append(f'<section class="ov"><div class="ov-head"><p class="eyebrow">People</p><h2>Who contributed, and who accepted</h2><p>Contributing an idea and accepting it are recorded separately.</p></div>{people_table(c)}'
                  f'<a class="text-link" href="about.html">About this record →</a></section>')
    body = commons_head(c, "overview") + f'<div class="wrap overview">{"".join(blocks)}</div>'
    return shell(title=f"{c.name} · Reason Commons", description=c.summary, depth=1, body=body, nav="commons", c=c, page="overview")


def people_stats(c):
    stats = defaultdict(lambda: {"contributed": [0, 0], "accepted": [0, 0], "earlier": [0, 0], "role": ""})
    for person in c.people:
        stats[person["name"]]["role"] = person["role"]
    for tree in c.trees.values():
        for index, key in ((0, "nodes"), (1, "links")):
            for item in tree[key]:
                for contributor in item["contributors"]:
                    stats[contributor["name"]]["contributed"][index] += 1
                for name in item.get("accepted_by", []):
                    stats[name]["accepted" if item["status"] == "accepted" else "earlier"][index] += 1
    order = [p["name"] for p in c.people] + [n for n in stats if n not in {p["name"] for p in c.people}]
    return [(name, stats[name]) for name in order]


def people_table(c):
    rows = []
    for name, s in people_stats(c):
        note = {"AI assistant": "Suggestions from the AI; it cannot accept anything", "Original contributor not identified": "Imported before contributors were recorded"}.get(name, s["role"])
        earlier = f'<br><span class="muted">{s["earlier"][0] + s["earlier"][1]} earlier, now disputed</span>' if sum(s["earlier"]) else ""
        accepted = f'{s["accepted"][0]} · {s["accepted"][1]}' if name not in ("AI assistant", "Original contributor not identified") else "—"
        rows.append(f'<tr><th scope="row">{esc(name)}{f"<span>{esc(note)}</span>" if note else ""}</th><td>{s["contributed"][0]} · {s["contributed"][1]}</td><td>{accepted}{earlier}</td></tr>')
    return (f'<div class="table-wrap"><table class="people"><thead><tr><th scope="col">Who</th><th scope="col">Contributed<br><span>statements · connections</span></th>'
            f'<th scope="col">Accepted for now<br><span>statements · connections</span></th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


# ---------------------------------------------------------------- map and the six question pages

def map_page(c, site):
    cells = []
    for i, name in enumerate(TREE_ORDER, 1):
        if name not in c.trees:
            continue
        tree = c.trees[name]
        pieces, shapes, loose = c.shapes(name)
        thumb = diagrams.thumbnail(shapes, [c.items[x] for x in loose], 260, 150)
        mix = defaultdict(int)
        for item in tree["nodes"] + tree["links"]:
            mix[item["status"]] += 1
        detail = " · ".join(f"{mix[s]} {STANDING[s].replace(' for now', '').lower()}" for s in STANDING if mix[s] and len(mix) > 1)
        state = "Not yet connected" if not tree["links"] else plural(len(tree["links"]), "connection")
        cells.append(f'<a class="mq" href="{TREES[name]["slug"]}.html"><span class="mq-n">{i}</span><span class="mq-thumb">{thumb}</span>'
                     f'<span class="mq-q">{esc(TREES[name]["question"])}</span><span class="mq-a">{esc(TREES[name]["about"])}</span>'
                     f'<span class="mq-c">{plural(len(tree["nodes"]), "statement")} · {state}{f"<br>{detail}" if detail else ""}</span></a>')
    body = commons_head(c, "map", heading=False) + f"""<div class="wrap">
<section class="page-intro"><h1>One goal, six questions</h1><p class="lede">Each question gets its own page, with a diagram drawn only from published connections. Each answer sets up the next one.</p></section>
<div class="mq-grid">{"".join(cells)}</div>
<p class="fine">Small diagrams show the real shape of each part: boxes are statements coloured by role, and lines are published connections. Loose boxes have no connection yet.</p>
</div>"""
    return shell(title=f"Map · {c.name} · Reason Commons", description=f"The six questions of the {c.name} commons.", depth=1, body=body, nav="commons", c=c, page="map")


def tree_page(c, name, site):
    tree = c.trees[name]
    info = TREES[name]
    index = TREE_ORDER.index(name)
    pieces, shapes, loose = c.shapes(name)
    nodes = {n["id"]: n for n in tree["nodes"]}
    diagram_parts, outline_parts, figures = [], [], []
    for piece, shape in zip(pieces, shapes) if pieces else ():
        notes = diagrams.number_markers(shape)
        svg = diagrams.svg(shape, nodes, c.href, f'{info["question"]}: {plural(len(shape["nodes"]), "statement")}')
        figures.append(figure(svg, f'Diagram: {info["question"]} Scrolls sideways when it is wider than the screen.', width=shape["w"]))
        if notes:
            items = "".join(f'<li><span class="m-n">{i}</span><div><p>{esc(a["text"])}</p><p class="muted">Assumed by {esc(a["by"])} under <a href="items.html#{l["id"]}">{esc(diagrams.RELATIONS.get(l["relation"], l["relation"]))}</a>'
                            f'{" · this connection is disputed" if l["status"] == "disputed" else ""}</p></div></li>'
                            for i, l in enumerate(notes, 1) for a in l["assumptions"][:1])
            diagram_parts.append(f'<div class="assumptions"><h3>Assumptions under the arrows</h3><ol>{items}</ol></div>')
        outline_parts.append(reconstruction_outline(c, name, piece["ids"], piece["links"]) if c.is_reconstruction else diagrams.outline(tree, piece["ids"], piece["links"], c.href, lambda k: kind_label(name, k)))
    if figures:
        diagram_parts.insert(0, f'<div class="dg-set">{"".join(figures)}</div>')
    if not pieces and shapes:  # Our conflict: five statements in their places, without arrows.
        svg = diagrams.svg(shapes[0], nodes, c.href, f'{info["question"]}: statements without accepted connections')
        diagram_parts.append(figure(svg, f'Diagram: {info["question"]}', "The positions follow each statement's role. No connections have been accepted, so no arrows are drawn."))
        outline_parts.append(loose_groups(c, name, [n["id"] for n in tree["nodes"]]))
    if loose:
        heading = "Not yet connected" if pieces else "Statements by role"
        text = ("These statements have no published connection yet." if pieces else
                "No connections in this part have been accepted yet, so the statements are grouped by their role, with no arrows between them.")
        group = f'<section class="loose"><h2>{heading}</h2><p>{text}</p>{loose_groups(c, name, loose)}</section>'
        diagram_parts.append(group)
        outline_parts.append(group)
    views = (f'<div class="view-toggle" role="group" aria-label="Show as" hidden><button type="button" data-view="diagram" aria-pressed="true">Diagram</button>'
             f'<button type="button" data-view="outline" aria-pressed="false">Outline</button></div>'
             f'<div class="views" data-views><div class="view view-diagram" data-view-panel="diagram">{"".join(diagram_parts)}</div>'
             f'<div class="view view-outline" data-view-panel="outline"><h2 class="sr-only">Outline</h2>{"".join(outline_parts)}</div></div>')
    if not shapes:  # Nothing connected to draw: the role groups are the whole view.
        views = f'<div class="views">{"".join(diagram_parts)}</div>'
    open_count = len([i for i in tree["nodes"] + tree["links"] if c.backlog.get(i["id"]) or i["status"] == "disputed"])
    previous = TREE_ORDER[index - 1] if index else None
    following = TREE_ORDER[index + 1] if index + 1 < len(TREE_ORDER) else TREE_ORDER[0]
    reading = info["read"] if tree["links"] else "Nothing here is connected yet: read each statement on its own."
    pager = (f'<nav class="pager" aria-label="Questions">'
             + (f'<a class="pager-prev" href="{TREES[previous]["slug"]}.html"><span>← Question {index}</span>{esc(TREES[previous]["question"])}</a>' if previous else '<span></span>')
             + f'<a class="pager-next" href="{TREES[following]["slug"]}.html"><span>{esc(info["next"])}</span>{esc(TREES[following]["question"])} →</a></nav>')
    body = commons_head(c, "map", heading=False) + f"""<div class="wrap">
<section class="q-head"><div><p class="eyebrow">Question {index + 1} of 6 · {esc(info["step"])}</p><h1>{esc(info["question"])}</h1><p class="lede">{esc(info["about"])}</p></div>
<dl class="q-stats"><div><dt>Statements</dt><dd>{len(tree["nodes"])}</dd></div><div><dt>Connections</dt><dd>{len(tree["links"])}</dd></div>{f'<div><dt>Open questions</dt><dd>{open_count}</dd></div>' if open_count else ''}</dl></section>
<div class="q-guide"><p><b>How to read it.</b> {esc(reading)}</p>{legend(c, name, shapes)}</div>
{views}
<details class="method-note"><summary>Where this comes from</summary><p>In the Logical Thinking Process this view is a {esc(info["method"])}. <a href="../how-it-works.html">How a commons works →</a></p></details>
{pager}
</div>"""
    return shell(title=f'{info["question"]} · {c.name} · Reason Commons', description=f'{info["about"]} From the {c.name} commons.', depth=1, body=body, nav="commons", c=c, page="tree")


# ---------------------------------------------------------------- statements and connections

def item_detail(c, ident, site):
    item = c.items[ident]
    name = c.tree_of[ident]
    info = TREES[name]
    tree = c.trees[name]
    link = c.is_link(ident)
    if link:
        sources = "".join(card(c, s, name) for s in item["from"])
        joint = '<p class="joint">All of these together</p>' if len(item["from"]) > 1 else ""
        statement = (f'<h2 class="sr-only">Connection: {esc(c.text(ident))}</h2><div class="conn">{joint}<div class="cards cards-stack">{sources}</div>'
                     f'<p class="conn-rel is-{item["status"]}">{esc(diagrams.RELATIONS.get(item["relation"], item["relation"]))} <span aria-hidden="true">↓</span></p>'
                     f'<div class="cards cards-stack">{card(c, item["to"], name)}</div></div>')
    else:
        label = f'<p class="item-label">Shown in diagrams as: “{esc(item["label"])}”</p>' if item.get("label") and item["label"] != item["text"] else ""
        statement = f'<h2 class="item-statement">{esc(item["text"])}</h2>{label}'
    near = "" if link else diagrams.neighbourhood(tree, ident, lambda k: kind_label(name, k), lambda i: f"#{i}")
    where = (figure(near, "Diagram: where this sits") if near else
             '<p class="muted">Its sources and target are shown above, with the relation between them.</p>' if link else
             '<p class="muted">Not yet connected. No published connection leads into or out of this statement.</p>')
    facts = [("Contributed by", names(x["name"] for x in item["contributors"]))]
    if item["status"] == "accepted":
        facts.append(("Accepted for now by", names(item["accepted_by"])))
    elif item["status"] == "disputed":
        facts.append(("Standing", "Disputed" + (f"; earlier accepted by {names(item['accepted_by'])}" if item["accepted_by"] else "")))
    else:
        facts.append(("Standing", "Proposed; no one has accepted it yet"))
    if item.get("acceptance_context"):
        facts.append(("Recorded context", item["acceptance_context"]))
    facts_html = "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in facts)
    traces = ""
    for key, word in TRACE_WORDS.items():
        refs = item.get(key, [])
        if refs:
            anchors = "".join(f'<a href="#{r}">{esc(c.short(r))}</a>' for r in refs)
            traces += f'<div><dt>{word}</dt><dd>{anchors}</dd></div>'
    backrefs = [(other, key) for other in c.order if not c.is_link(other) for key in TRACE_WORDS if ident in c.items[other].get(key, [])]
    if backrefs:
        traces += '<div><dt>Referred to by</dt><dd>' + "".join(f'<a href="#{o}">{esc(c.short(o))}</a>' for o, _ in backrefs) + "</dd></div>"
    sections = []
    if c.is_reconstruction:
        source_titles = {source["id"]: source["title"] for source in c.sources}
        rows = "".join(f'<li><p><a href="about.html#source-{esc(ref["source_id"])}">{esc(source_titles[ref["source_id"]])}</a> · {esc(ref["locator"])}</p><p class="muted">{"AI inference" if ref["basis"] == "inference" else "AI reconstruction"} from the supplied analysis; the original passage has not been independently checked.</p></li>' for ref in item["source_refs"])
        sections.append(f'<section class="d-sec d-sources"><h3>Sources and reconstruction</h3><ul class="notes">{rows}</ul></section>')
    if not link:
        rels = [l for l in tree["links"] if ident in l["from"] or l["to"] == ident]
        if rels:
            rows = "".join(f'<li><a href="#{l["id"]}"><span>{"Leads into" if l["to"] == ident else "Leads from here"} · {esc(diagrams.RELATIONS.get(l["relation"], l["relation"]))}{" · " + STANDING[l["status"]] if l["status"] != "accepted" else ""}</span>'
                           f'{esc(names(c.items[s]["text"] for s in l["from"]) if l["to"] == ident else c.items[l["to"]]["text"])}</a></li>' for l in rels)
            sections.append(f'<section class="d-sec"><h3>Connections</h3><ul class="rel-list">{rows}</ul></section>')
    for key, title in (("assumptions", "Assumptions"), ("challenges", "Challenges")):
        if item.get(key):
            rows = "".join(f'<li><p>{esc(a["text"])}</p><p class="muted">{"Assumed" if key == "assumptions" else "Raised"} by {esc(a["by"])}</p></li>' for a in item[key])
            sections.append(f'<section class="d-sec d-{key}"><h3>{title}</h3><ul class="notes">{rows}</ul></section>')
    if c.backlog.get(ident):
        rows = "".join(f'<li><p>{esc(t.get("label") or t["work"].replace("_", " ").capitalize())}</p>' + (f'<p class="muted">{esc(t["note"])}</p>' if t.get("note") else "") + "</li>"
                       for t in c.backlog[ident])
        sections.append(f'<section class="d-sec d-open"><h3>Open questions</h3><ul class="notes">{rows}</ul></section>')
    learning = [(req, role) for req in c.feedback for role, group in (("about", [req["about"]]), ("benefit", req["benefits"]), ("reservation", req["reservations"])) for s in group if s["ref"] == ident]
    if learning:
        rows = "".join(f'<li><p>{"The change being tried" if role == "about" else "An expected benefit" if role == "benefit" else "A possible harm"} in a trial recorded {day(req["recorded_at"])}.</p>'
                       f'<p class="muted"><a href="learning.html#{req["id"]}">See what people reported →</a></p></li>' for req, role in learning)
        sections.append(f'<section class="d-sec"><h3>Learning</h3><ul class="notes">{rows}</ul></section>')
    history = []
    for release in c.history:
        for change in release["changes"]:
            if ident in change["refs"]:
                before = f'<p class="before"><span>Earlier wording</span><s>{esc(change["before"])}</s></p>' if change.get("before") else ""
                note = ": " + esc(change["note"]) if change.get("note") and change["type"] != "added" else ""
                history.append(f'<li><p><b>{CHANGE_WORDS[change["type"]]}</b> in the release of {day(release["date"])}{note}</p>{before}</li>')
    if history:
        sections.append(f'<section class="d-sec"><h3>History</h3><ul class="notes">{"".join(history)}</ul></section>')
    text = brief(c, ident, site)
    instruction = ("This commons is invented, so there is no one to send anything to. Use the brief to practise with the skill." if c.is_example else
                   "Copy the brief into your AI to draft a question or correction. Check the supplied analysis and original passage before attributing a view to anyone." if c.is_reconstruction else
                   "Copy this brief into a conversation with your AI to develop a question, an observation or a challenge. The skill checks the current record first.")
    contribute = (f'<section class="d-sec d-brief"><h3>{"Practise a contribution" if c.is_example else "Bring a contribution to your AI"}</h3>'
                  f'<p>{instruction}</p>'
                  f'<div class="brief-actions"><button type="button" class="button" data-copy="brief-{ident}" hidden>Copy the brief</button><a class="text-link" href="/skills">Get the skill ↗</a><span class="copy-status" role="status"></span></div>'
                  f'<details><summary>Read the brief</summary><pre class="brief" id="brief-{ident}" tabindex="0">{esc(text)}</pre></details>'
                  f'<p class="fine">This page is read-only. Copying prepares text; it does not submit anything or give access to the shared record.</p></section>')
    position = c.order.index(ident)
    prev_id = c.order[position - 1] if position else None
    next_id = c.order[position + 1] if position + 1 < len(c.order) else None
    pager = ('<nav class="pager pager-item" aria-label="Neighbouring items">'
             + (f'<a class="pager-prev" href="#{prev_id}"><span>← Previous</span>{esc(c.short(prev_id))}</a>' if prev_id else "<span></span>")
             + (f'<a class="pager-next" href="#{next_id}"><span>Next →</span>{esc(c.short(next_id))}</a>' if next_id else "<span></span>") + "</nav>")
    kind = f'Connection · {diagrams.RELATIONS.get(item["relation"], item["relation"])}' if link else kind_label(name, item["kind"])
    return (f'<div class="item-detail"><nav class="item-crumbs" aria-label="Item"><a href="#statements">← All statements</a><a href="{info["slug"]}.html">{esc(info["question"])}</a></nav>'
            f'<div class="item-top"><span class="kind kind-{"link" if link else item["kind"]}">{esc(kind)}</span>{chip(item["status"])}</div>{statement}'
            f'<div class="item-grid"><div class="item-where"><h3>Where it sits</h3>{where}</div><aside class="item-facts"><dl>{facts_html}{traces}</dl></aside></div>'
            f'{"".join(sections)}{contribute}{pager}</div>')


def items_page(c, site):
    groups = []
    for i, name in enumerate(TREE_ORDER, 1):
        if name not in c.trees:
            continue
        tree = c.trees[name]
        articles = []
        for item in tree["nodes"] + tree["links"]:
            ident = item["id"]
            link = c.is_link(ident)
            searchable = " ".join([c.text(ident), c.kind_of(ident), STANDING[item["status"]], *item.get("accepted_by", []), *(x["name"] for x in item["contributors"])])
            summary = (f'<a class="item-summary card role-{"link" if link else item["kind"]} is-{item["status"]}" href="#{ident}"><span class="card-top"><span class="kind">{esc(c.kind_of(ident))}</span>{chip(item["status"])}</span>'
                       f'<span class="card-text">{esc(c.text(ident))}</span><span class="card-foot">{esc(endorsement(item))}</span></a>')
            articles.append(f'<article class="item{" item-link" if link else ""}" id="{ident}" data-search="{esc(searchable.lower())}">{summary}{item_detail(c, ident, site)}</article>')
        groups.append(f'<section class="items-tree" aria-labelledby="t-{name}"><h2 class="items-tree-title" id="t-{name}"><span>Question {i}</span>{esc(TREES[name]["question"])} '
                      f'<a class="text-link" href="{TREES[name]["slug"]}.html">See the diagram →</a></h2><div class="items-list">{"".join(articles)}</div></section>')
    statements, connections = c.counts()
    body = commons_head(c, "items", heading=False) + f"""<div class="wrap items" id="statements">
<section class="items-intro"><h1>Every statement and connection</h1><p class="lede">{plural(statements, "statement")} and {plural(connections, "connection")}, in the order of the six questions. Open one to see where it sits, who contributed it, who accepted it, and a brief for your AI.</p>
<div class="search" hidden><label for="filter">Find a statement</label><input id="filter" type="search" placeholder="Try a word or a name" autocomplete="off"><p class="search-status" role="status"></p></div></section>
{"".join(groups)}
</div>"""
    return shell(title=f"Statements · {c.name} · Reason Commons", description=f"Every statement and connection in the {c.name} commons.", depth=1, body=body, nav="commons", c=c, page="items")


# ---------------------------------------------------------------- open questions

def question_board(c, limit=None):
    columns = []
    used = set()
    for title, works in WORK_GROUPS + [("Other unfinished reasoning", None)]:
        cards = []
        for ident in c.open_items():
            tasks = [t for t in c.backlog.get(ident, []) if (works is None and not any(t["work"] in w for _, w in WORK_GROUPS)) or (works and t["work"] in works)]
            if not tasks and title == "Examine a challenge" and c.items[ident]["status"] == "disputed" and not c.backlog.get(ident):
                tasks = [{"label": "A challenge waits for a response.", "work": "resolve_challenge"}]
            for task in tasks:
                note = f'<span class="qc-note">{esc(task["note"])}</span>' if task.get("note") else ""
                cards.append(f'<a class="qc" href="items.html#{ident}"><span class="qc-task">{esc(task.get("label") or task["work"].replace("_", " ").capitalize())}</span>{note}'
                             f'<span class="qc-about"><span class="kind">{esc(c.kind_of(ident))}</span>{chip(c.items[ident]["status"])}<span class="qc-text">{esc(c.short(ident))}</span></span>'
                             f'<span class="qc-where">{esc(TREES[c.tree_of[ident]]["question"])}</span></a>')
                used.add(ident)
        if cards:
            shown = cards[:limit] if limit else cards
            more = f'<p class="muted">{len(cards) - len(shown)} more</p>' if len(cards) > len(shown) else ""
            columns.append(f'<section class="qcol"><h3>{esc(title)} <span>{len(cards)}</span></h3>{"".join(shown)}{more}</section>')
    return f'<div class="qboard">{"".join(columns)}</div>'


def questions_page(c, site):
    owners = c.open_items()
    body = commons_head(c, "questions", heading=False) + f"""<div class="wrap">
<section class="page-intro"><h1>Open questions</h1><p class="lede">{plural(len(owners), "published item")} with open questions, grouped by the kind of work they need. An item can be accepted and still have work left on it.</p></section>
{question_board(c)}
<p class="fine">These come from the commons' own record of unfinished reasoning, and from disputed items. No deadline, owner or priority is shown because none is recorded.</p>
</div>"""
    return shell(title=f"Open questions · {c.name} · Reason Commons", description="Where the reasoning is unfinished.", depth=1, body=body, nav="commons", c=c, page="questions")


# ---------------------------------------------------------------- learning

def latest(request, person, ref):
    answer, when = None, ""
    for report in request["reports"]:
        if report["by"] != person:
            continue
        for outcome in report["outcomes"]:
            if outcome["ref"] == ref and report["recorded_at"] >= when:
                answer, when = outcome, report["recorded_at"]
    reported = any(r["by"] == person for r in request["reports"])
    return answer or ({"verdict": "not_assessed", "note": "Reported, but did not assess this."} if reported else {"verdict": "awaiting", "note": "No report yet."})


def trial_matrix(c, request):
    providers = request["feedback_from"]
    head = "".join(f'<th scope="col">{esc(p)}</th>' for p in providers)
    rows = []
    for role, group in (("Expected benefit", request["benefits"]), ("Possible harm", request["reservations"])):
        for snap in group:
            cells = "".join(f'<td><span class="v v-{v["verdict"]}" title="{esc(v["note"])}"><i aria-hidden="true"></i>{VERDICTS[v["verdict"]]}</span></td>'
                            for v in (latest(request, p, snap["ref"]) for p in providers))
            rows.append(f'<tr><th scope="row"><span class="kind">{role}</span><a href="items.html#{snap["ref"]}">{esc(snap["text"])}</a></th>{cells}</tr>')
    return (f'<div class="table-wrap"><table class="matrix"><caption class="sr-only">Expected outcomes and what each person reported</caption>'
            f'<thead><tr><th scope="col">What was expected</th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def learning_page(c, site):
    blocks = []
    for request in c.feedback:
        about = request["about"]
        snaps = {s["ref"]: s for s in request["benefits"] + request["reservations"]}
        reports = []
        for report in sorted(request["reports"], key=lambda r: r["recorded_at"]):
            outcomes = "".join(f'<li><span class="v v-{o["verdict"]}"><i aria-hidden="true"></i>{VERDICTS[o["verdict"]]}</span> <span>{esc(snaps[o["ref"]]["text"])}</span><span class="muted">{esc(o["note"])}</span></li>'
                               for o in report["outcomes"])
            d, m = short_day(report["recorded_at"])
            reports.append(f'<article class="report" id="{report["id"]}"><div class="report-date"><b>{d}</b>{m}</div><div><p class="report-by">{esc(report["by"])} · {esc(READINESS[report["readiness"]])}</p>'
                           f'<blockquote>{esc(report["text"])}</blockquote><ul class="report-outcomes">{outcomes}</ul></div></article>')
        waiting = [p for p in request["feedback_from"] if not any(r["by"] == p for r in request["reports"])]
        ready = " " + esc(request["ready_when"]) if request.get("ready_when") else ""
        blocks.append(f"""<section class="trial" id="{request["id"]}">
<div class="trial-head"><p class="eyebrow">Trial · expectations version {request["revision"]}</p><h2><a href="items.html#{about["ref"]}">{esc(about["text"])}</a></h2>
<p>Expectations recorded {day(request["recorded_at"])} by {esc(request["created_by"])}, before the trial. Asked to report: {esc(names(request["feedback_from"]))}.{ready}</p></div>
{trial_matrix(c, request)}
<h3 class="reports-title">The reports</h3>{"".join(reports)}
{f'<p class="muted">Still to report: {esc(names(waiting))}.</p>' if waiting else ''}
</section>""")
    body = commons_head(c, "learning", heading=False) + f"""<div class="wrap">
<section class="page-intro"><h1>What happened when they tried it</h1><p class="lede">Before trying a change, the group recorded what they expected it to do, good and bad, and who would report back. Each report is that person's own account.</p></section>
{"".join(blocks)}
<p class="fine">“Not observed” means that person did not see it, not that it cannot happen. “Unclear” and “Not assessed” keep the question open. A report does not by itself confirm a connection.</p>
</div>"""
    return shell(title=f"Learning · {c.name} · Reason Commons", description="Expected outcomes, and what people reported.", depth=1, body=body, nav="commons", c=c, page="learning")


# ---------------------------------------------------------------- changes and about

def changes_page(c, site):
    entries = []
    for release in reversed(c.history):
        rows = []
        for change in release["changes"]:
            refs = change["refs"]
            if change["type"] == "report":
                links = "".join(f'<a href="learning.html#{r}">{esc(c.reports[r][1]["by"])}</a>' for r in refs)
            else:
                links = "".join(f'<a href="items.html#{r}" class="is-{c.items[r]["status"]}">{esc(c.short(r))}</a>' for r in refs if not c.is_link(r))
                hidden = len([r for r in refs if c.is_link(r)])
                if hidden:
                    links += f'<span class="muted">and {plural(hidden, "connection")}</span>'
            if len(refs) > 10:
                links = f'<details><summary>{plural(len([r for r in refs if not c.is_link(r)]), "statement")} and {plural(len([r for r in refs if c.is_link(r)]), "connection")}</summary><div class="ch-links">{links}</div></details>'
            else:
                links = f'<div class="ch-links">{links}</div>'
            before = (f'<p class="before"><span>Before</span><s>{esc(change["before"])}</s></p><p class="before after"><span>Now</span>{esc(c.items[refs[0]]["text"])}</p>'
                      if change.get("before") else "")
            note = f'<p>{esc(change["note"])}</p>' if change.get("note") else ""
            rows.append(f'<li class="chg chg-{change["type"]}"><span class="chg-type">{CHANGE_WORDS[change["type"]]}</span><div>{note}{before}{links}</div></li>')
        d, m = short_day(release["date"])
        entries.append(f'<article class="release"><div class="release-date"><b>{d}</b>{m}</div><div class="release-body"><p class="eyebrow">Release {esc(release["release_id"])}</p>'
                       f'<h2>{esc(release["title"])}</h2><p class="lede">{esc(release["summary"])}</p><ul class="chgs">{"".join(rows)}</ul></div></article>')
    later = "" if c.is_example or c.is_reconstruction else ('<article class="release release-next"><div class="release-date"><b>…</b>Later</div><div class="release-body"><h2>The next release</h2>'
                                     '<p class="lede">When Rufus and David publish again, this page will show what was added, reworded or disputed, with the earlier wording kept.</p></div></article>')
    body = commons_head(c, "changes", heading=False) + f"""<div class="wrap narrow-left">
<section class="page-intro"><h1>Changes</h1><p class="lede">How the published reasoning has changed, release by release. Earlier wording is kept.</p></section>
<div class="releases">{later}{"".join(entries)}</div>
</div>"""
    return shell(title=f"Changes · {c.name} · Reason Commons", description="How the published reasoning changed.", depth=1, body=body, nav="commons", c=c, page="changes")


def about_page(c, site):
    rows = []
    present = [s for s in STANDING if any(i["status"] == s for t in c.trees.values() for i in t["nodes"] + t["links"])]
    for i, name in enumerate(TREE_ORDER, 1):
        if name not in c.trees:
            continue
        tree = c.trees[name]
        counts = {s: (len([n for n in tree["nodes"] if n["status"] == s]), len([l for l in tree["links"] if l["status"] == s])) for s in present}
        cells = "".join(f'<td>{counts[s][0]} · {counts[s][1]}</td>' for s in present)
        rows.append(f'<tr><th scope="row"><a href="{TREES[name]["slug"]}.html">{i}. {esc(TREES[name]["question"])}</a></th>{cells}</tr>')
    head = "".join(f'<th scope="col">{STANDING[s]}<br><span>statements · connections</span></th>' for s in present)
    statements, connections = c.counts()
    fiction = ('<section class="about-fiction"><h2>This commons is invented</h2><p>Willow Lane Primary, Amara, Grace, Tomasz, Dev and Ruth, and everything they say and report, are fictional. '
               'The commons was written in the skill\'s own file format and checked with the skill\'s validator, to show what a published commons can hold. '
               'Nothing here describes a real school, street or person.</p></section>') if c.is_example else ""
    if c.is_reconstruction:
        source_list = "".join(f'<article id="source-{esc(source["id"])}"><h3>{esc(source["title"])}</h3><p>{esc(source["description"])}</p></article>' for source in c.sources)
        fiction = ('<section class="ov" id="sources"><h2>Sources and limits</h2><p>This is a proposed AI reconstruction from supplied analyses of a real discussion. Every item names its analysis, page or section, and whether its connection is an inference. The source authors and forum participants have not reviewed or endorsed this selection.</p>'
                   + source_list + '<h3>The broader programme</h3><p>The later analysis covers reflective human development, trustworthy institutions, the Laboratory, Forge/model adaptation, Vocal Presence, federation, material and energy services, and enforceable security. It separates philosophical hypotheses from institutional mechanisms and distinguishes local success from a durable shift in institutional selection. This compact starting map leaves those branches as open review work.</p>'
                   '<h3>What counts as progress?</h3><p>The earlier analysis proposes measuring practices adopted and retained in viable institutions that remain faithful to their purpose. The measures, system boundary, observation period and protected conditions still need agreement. Essays and conversation alone do not establish that outcome.</p></section>')
    excluded = ("Nothing is held back: the example's whole working file is published, apart from how each contribution was captured."
                if c.is_example else
                "Proposed and disputed reasoning, open questions, assumptions and challenges, outcome reports, approval records and working notes stay in the working record. They are not published here.")
    if c.is_reconstruction:
        excluded = "The original forum posts, manuscript and source documents are not reproduced here. No participant endorsement, trial owner, budget, baseline, numerical target, feedback commitment or observed result is recorded. The map does not establish one global constraint."
    download = '<a class="button button-quiet" href="reasoning.json" download>Download this release <span aria-hidden="true">↓</span></a>'
    release_text = ""
    if c.is_reconstruction:
        # The host sandboxes HTML without allow-downloads; keep the release readable without scripts.
        download = '<a class="button button-quiet" href="#release-json">Read or copy this release <span aria-hidden="true">↓</span></a>'
        release_text = f'<details id="release-json"><summary>Read the release as JSON</summary><pre class="brief" tabindex="0">{esc(c.json)}</pre></details>'
    body = commons_head(c, "about", heading=False) + f"""<div class="wrap">
<section class="page-intro"><h1>About this record</h1><p class="lede">{esc(c.scope)}</p></section>
{fiction}
<div class="about-grid">
<section><h2>What “accepted for now” means</h2><p>Named people are willing to build on a statement or connection for now. It records their judgement at the time. It does not establish truth, and it does not mean everyone agrees: each item names exactly who accepted it.</p>
<h2>Contributed is not the same as accepted</h2><p>Each item records who contributed the idea and, separately, who accepted it. Ideas suggested by the AI are attributed to the AI, and only people can accept anything.{"" if c.is_example or c.is_reconstruction else " Some statements were imported before contributors were recorded; they say so rather than guessing."}</p>
<h2>What isn't here</h2><p>{esc(excluded)}</p>
<h2>A snapshot, not a live feed</h2><p>This is release {esc(c.release_id)}, published {day(c.date)}. {"Earlier wording stays on the Changes page." if len(c.history) > 1 else "It is the first release, so there is no earlier wording to compare yet."}</p></section>
<aside class="about-side"><p class="eyebrow">In this release</p><p class="big-count"><b>{statements}</b> statements <b>{connections}</b> connections</p>
<div class="table-wrap"><table class="counts"><thead><tr><th scope="col">Question</th>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<p>{download}</p>
<p class="fine">{"The release contains exactly what these pages show, as JSON." if c.is_reconstruction else "The download holds exactly what these pages show, as JSON."}</p>{release_text}</aside>
</div>
<section class="about-people"><h2>People</h2>{people_table(c)}</section>
</div>"""
    return shell(title=f"About · {c.name} · Reason Commons", description="What this record is, and what it isn't.", depth=1, body=body, nav="commons", c=c, page="about")


# ---------------------------------------------------------------- everything

def render(site, normalized):
    commons = [Commons(data) for data in normalized]
    outputs = {"index.html": home(site, commons), "how-it-works.html": how_it_works(site, commons)}
    for c in commons:
        outputs[f"{c.slug}/index.html"] = overview(c, site)
        outputs[f"{c.slug}/map.html"] = map_page(c, site)
        for name in TREE_ORDER:
            if name in c.trees:
                outputs[f'{c.slug}/{TREES[name]["slug"]}.html'] = tree_page(c, name, site)
        outputs[f"{c.slug}/items.html"] = items_page(c, site)
        if c.open_items():
            outputs[f"{c.slug}/questions.html"] = questions_page(c, site)
        if c.feedback:
            outputs[f"{c.slug}/learning.html"] = learning_page(c, site)
        outputs[f"{c.slug}/changes.html"] = changes_page(c, site)
        outputs[f"{c.slug}/about.html"] = about_page(c, site)
    return outputs
