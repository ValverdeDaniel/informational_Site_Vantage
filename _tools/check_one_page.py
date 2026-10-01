"""Checks that one-page.html still matches the five pages. Reads only; changes nothing.

    python _tools/check_one_page.py              check the site this script sits in
    python _tools/check_one_page.py <folder>     check another copy of the site

Exit code 0 means everything matches, 1 means problems are listed, 2 means the checker itself failed.

The five pages (index, employee-benefits, property-casualty, about, legal) are the master copy.
one-page.html is a hand-made copy of them, with a fixed list of deliberate differences (README,
"The two layouts"). This script allows exactly those differences and reports anything else that
differs, with file:line on both sides. It compares every section of <main> (tags, attributes, words
and the spaces between them), the head's charset, viewport, theme-color, icon and stylesheet tags,
<html lang>, the skip link, the top bar, the Multi-page | One-page switch and the footer, and it
checks every link and image path on all six pages and every url() in styles.css (the fonts). It does
not compare comments, or each page's own <title> and description. Within one section it reports the
first difference: fix it and run again.

Standard library only. GitHub Pages does not publish this folder: Jekyll skips names starting with "_".
"""
import difflib
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

PAGES = ["index.html", "employee-benefits.html", "property-casualty.html", "about.html", "legal.html"]
ONE = "one-page.html"
BAND_PAGES = ["index.html", "employee-benefits.html", "property-casualty.html"]  # their Talk to a broker band is left out
# Where each page's content starts on one-page.html. Home is the top of the page.
CHAPTER = {"index.html": "top", "employee-benefits.html": "employee-benefits",
           "property-casualty.html": "property-casualty", "about.html": "about", "legal.html": "legal"}
CHAPTER_IDS = ["employee-benefits", "property-casualty", "about", "legal"]
SWITCH_TARGET = {"index.html": "one-page.html", "employee-benefits.html": "one-page.html#employee-benefits",
                 "property-casualty.html": "one-page.html#property-casualty", "about.html": "one-page.html#about",
                 "legal.html": "one-page.html#legal"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
BLOCK = {"address", "article", "aside", "blockquote", "br", "dd", "div", "dl", "dt", "figure", "footer", "form",
         "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr", "img", "li", "main", "nav", "ol", "p", "section",
         "table", "td", "th", "tr", "ul"}
URL_ATTRS = {"a": ["href"], "link": ["href"], "img": ["src", "srcset"], "source": ["src", "srcset"]}
CHROME_LINK_RELS = {"icon", "apple-touch-icon", "stylesheet"}
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")        # tel:, mailto:, https: ... are left alone
WS = re.compile(r"[ \t\n\r\f]+")                        # HTML whitespace; a no-break space is content

problems = []


def problem(kind, *lines):
    problems.append((kind, lines))


# ---------- a small tree built with the standard HTML parser ----------
class Node:
    def __init__(self, tag, attrs, line, parent):
        self.tag, self.attrs, self.line, self.parent, self.children = tag, attrs, line, parent, []


class Text:
    def __init__(self, raw, line, parent):
        self.raw, self.line, self.parent = raw, line, parent
        self.text = WS.sub(" ", raw).strip(" ")          # "" when the node is only whitespace


class Tree(HTMLParser):
    """Comments and the doctype are ignored, so text inside <!-- --> never counts."""

    def __init__(self, name):
        super().__init__(convert_charrefs=True)
        self.name = name
        self.root = Node("#document", {}, 0, None)
        self.cur = self.root

    def _node(self, tag, attrs):
        return Node(tag, {k: (v if v is not None else "") for k, v in attrs}, self.getpos()[0], self.cur)

    def handle_starttag(self, tag, attrs):
        node = self._node(tag, attrs)
        self.cur.children.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(self._node(tag, attrs))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is self.root:
            problem("HTML", f"{self.name}:{self.getpos()[0]}  </{tag}> closes nothing - a stray or extra closing tag")
            return
        if n is not self.cur:
            problem("HTML", f"{self.name}:{self.cur.line}  <{self.cur.tag}> is never closed "
                            f"(</{tag}> at line {self.getpos()[0]} closed it)")
        self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(Text(data, self.getpos()[0], self.cur))


def parse(root, name):
    path = root / name
    if not path.exists():
        problem("MISSING", f"{name} is not in {root}")
        return None
    try:
        source = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as e:
        problem("ENCODING", f"{name} is not saved as UTF-8 (byte {e.start} is not UTF-8). Re-save it as UTF-8 - "
                            "in Notepad: File > Save as > Encoding: UTF-8.")
        return None
    t = Tree(name)
    t.feed(source)
    t.close()
    if t.cur is not t.root:
        problem("HTML", f"{name}:{t.cur.line}  <{t.cur.tag}> is never closed")
    return t.root


def walk(node):
    for c in node.children:
        yield c
        if isinstance(c, Node):
            yield from walk(c)


def elements(node, tag=None):
    return [n for n in walk(node) if isinstance(n, Node) and (tag is None or n.tag == tag)]


def classes(n):
    return n.attrs.get("class", "").split()


def text_of(n):
    return " ".join(t.text for t in walk(n) if isinstance(t, Text) and t.text)


def rendered(n):
    """The words as a browser lays them out: spaces between inline pieces count, block edges are spaces."""
    parts = []

    def rec(x):
        for c in x.children:
            if isinstance(c, Text):
                parts.append(c.raw)
            else:
                edge = " " if c.tag in BLOCK else ""
                parts.append(edge)
                rec(c)
                parts.append(edge)
    rec(n)
    return WS.sub(" ", "".join(parts)).strip(" ")


def inside(n, cls):
    while n is not None:
        if isinstance(n, Node) and cls in classes(n):
            return True
        n = n.parent
    return False


def inside_tag(n, tag, **attrs):
    while n is not None:
        if isinstance(n, Node) and n.tag == tag and all(n.attrs.get(k) == v for k, v in attrs.items()):
            return True
        n = n.parent
    return False


def first(node, pred):
    return next((n for n in walk(node) if isinstance(n, Node) and pred(n)), None)


# ---------- the link rule (README, "The two layouts") ----------
def map_href(h):
    """X.html -> #<X's chapter>, X.html#part -> #part, anything else unchanged."""
    page, sep, part = h.partition("#")
    if page in CHAPTER:
        return "#" + (part if sep and part else CHAPTER[page])
    return h


# ---------- token streams, for comparing two copies ----------
def stream(node, norm_el, norm_text=None, include_self=True):
    out = []

    def rec(n):
        for c in n.children:
            if isinstance(c, Text):
                if c.text:
                    out.append(("text", norm_text(c) if norm_text else c.text, c.line))
            else:
                one(c)

    def one(n):
        r = norm_el(n)
        if r is None:
            return
        tag, attrs = r
        out.append(("open", (tag, tuple(sorted(attrs.items()))), n.line))
        if n.tag not in VOID:
            rec(n)
            out.append(("close", tag, n.line))

    one(node) if include_self else rec(node)
    return out


def show(tok):
    if tok is None:
        return "(nothing more here)"
    kind, val, _ = tok
    if kind == "text":
        return val if len(val) <= 110 else val[:107] + "..."
    if kind == "close":
        return f"</{val}>"
    tag, attrs = val
    return "<" + " ".join([tag] + [f'{k}="{v}"' for k, v in attrs]) + ">"


def first_difference(a, b):
    for i in range(max(len(a), len(b))):
        x = a[i] if i < len(a) else None
        y = b[i] if i < len(b) else None
        if x is None or y is None or x[:2] != y[:2]:
            return x, y
    return None


def norm_plain(n):
    attrs = dict(n.attrs)
    if "class" in attrs:
        attrs["class"] = " ".join(attrs["class"].split())
    return n.tag, attrs


def expected_norm(section, chapter_id):
    """How a five-page section must look on one-page.html. Links point at sections everywhere. On a
    chapter's first section only: the section gains class chapter and the chapter id, its h1 becomes
    h2.chapter-title, and its photo loads lazily instead of first (README, The two layouts, 2-5)."""
    def norm(n):
        tag, attrs = norm_plain(n)
        if "href" in attrs:
            attrs["href"] = map_href(attrs["href"])
        if chapter_id:
            if n is section:
                attrs["class"] = " ".join(attrs.get("class", "").split() + ["chapter"])
                attrs["id"] = chapter_id
            elif tag == "h1":
                tag = "h2"
                attrs["class"] = " ".join(attrs.get("class", "").split() + ["chapter-title"])
            elif tag == "img" and "fetchpriority" in attrs:
                del attrs["fetchpriority"]
                attrs["loading"] = "lazy"
        return tag, attrs
    return norm


def main_sections(doc, name):
    """Top-level sections of <main>. Anything else directly inside <main> is reported: it would not be compared."""
    mains = elements(doc, "main")
    if len(mains) != 1:
        problem("STRUCTURE", f"{name}: needs exactly one <main>, has {len(mains)}")
        return []
    out = []
    for c in mains[0].children:
        if isinstance(c, Text):
            if c.text:
                problem("STRAY", f"{name}:{c.line}  text directly in <main>, outside any section: {c.text[:70]}")
        elif c.tag == "section":
            out.append(c)
        else:
            problem("STRAY", f"{name}:{c.line}  <{c.tag}> directly in <main>, outside any section - move it into one")
    return out


def check_body(docs):
    """Everything a visitor sees must be in the skip link, the header, <main> or the footer."""
    for name, doc in docs.items():
        body = elements(doc, "body")
        if len(body) != 1:
            problem("STRUCTURE", f"{name}: needs exactly one <body>, has {len(body)}")
            continue
        for c in body[0].children:
            if isinstance(c, Text):
                if c.text:
                    problem("STRAY", f"{name}:{c.line}  text directly in <body>: {c.text[:70]}")
            elif not (c.tag in ("header", "main", "footer") or "skip-link" in classes(c)):
                problem("STRAY", f"{name}:{c.line}  <{c.tag}> directly in <body>, outside the header, main and footer")


def is_band(name, s):
    return name in BAND_PAGES and "contact" in classes(s) and "id" not in s.attrs


def label(chapter, s):
    mark = first(s, lambda n: "eyebrow" in classes(n)) or first(s, lambda n: n.tag in ("h1", "h2", "h3", "h4", "h5", "h6"))
    return f"{chapter} > {text_of(mark) if mark else '(no heading)'}"


# ---------- check 1: every section's tags, attributes, words and spacing match ----------
def check_text(secs):
    expected = []
    for name in PAGES:
        chapter = "index" if name == "index.html" else CHAPTER[name]
        kept = [s for s in secs[name] if not is_band(name, s)]
        for k, s in enumerate(kept):
            cid = CHAPTER[name] if (k == 0 and name != "index.html") else None
            expected.append((label(chapter, s), name, s, cid))
    actual, chapter = [], "index"
    for s in secs[ONE]:
        if s.attrs.get("id") in CHAPTER_IDS:
            chapter = s.attrs["id"]
        actual.append((label(chapter, s), s))
    sm = difflib.SequenceMatcher(a=[e[0] for e in expected], b=[a[0] for a in actual], autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for (lab, name, s, cid), (_, t) in zip(expected[i1:i2], actual[j1:j2]):
                d = first_difference(stream(s, expected_norm(s, cid)), stream(t, norm_plain))
                if d:
                    x, y = d
                    problem("DRIFT", lab, f"{name}:{x[2] if x else s.line}  {show(x)}",
                            f"{ONE}:{y[2] if y else t.line}  {show(y)}")
                    continue
                a, b = rendered(s), rendered(t)
                if a != b:
                    i = next((k for k in range(min(len(a), len(b))) if a[k] != b[k]), min(len(a), len(b)))
                    lo = max(0, i - 30)
                    problem("SPACING", f"{lab}: the words match but the spaces between them differ",
                            f"{name}:{s.line}  ...{a[lo:i + 30]}...", f"{ONE}:{t.line}  ...{b[lo:i + 30]}...")
            continue
        for lab, name, s, _ in expected[i1:i2]:
            problem("MISSING", f"{name}:{s.line}  section \"{lab}\" has no copy in {ONE}")
        for lab, t in actual[j1:j2]:
            problem("EXTRA", f"{ONE}:{t.line}  section \"{lab}\" is not on any of the five pages")
    return actual


# ---------- check 2: page structure ----------
def check_structure(docs, secs):
    one = docs[ONE]

    def count(doc, tag, pred=lambda n: True):
        return sum(1 for n in elements(doc, tag) if pred(n))

    for name in PAGES:
        if count(docs[name], "h1") != 1:
            problem("STRUCTURE", f"{name}: needs exactly one <h1> (its main heading), has {count(docs[name], 'h1')}")
    need = [("<h1>", count(one, "h1")),
            ("fetchpriority", sum(1 for n in elements(one) if "fetchpriority" in n.attrs)),
            ('<meta charset="utf-8">', count(one, "meta", lambda n: n.attrs.get("charset", "").lower() == "utf-8")),
            ("viewport <meta>", count(one, "meta", lambda n: n.attrs.get("name") == "viewport")),
            ('<html lang="en">', count(one, "html", lambda n: n.attrs.get("lang") == "en"))]
    for what, n in need:
        if n != 1:
            problem("STRUCTURE", f"{ONE}: needs exactly one {what}, has {n}")
    seen = {}
    for n in elements(one):
        if "id" in n.attrs:
            if n.attrs["id"] in seen:
                problem("STRUCTURE", f"{ONE}:{n.line}  id=\"{n.attrs['id']}\" is also used at line {seen[n.attrs['id']]}")
            seen.setdefault(n.attrs["id"], n.line)
    body = elements(one, "body")
    if not body or body[0].attrs.get("id") != "top":
        problem("STRUCTURE", f"{ONE}: <body> must carry id=\"top\" (the logo and Home links jump to it)")
    order = [s.attrs.get("id") for s in secs[ONE] if "chapter" in classes(s)]
    if order != CHAPTER_IDS:
        problem("STRUCTURE", f"{ONE}: chapter sections (class \"chapter\") must be {CHAPTER_IDS} in that order, "
                             f"found {order}")


# ---------- check 3: links and image paths on all six pages ----------
def urls(n):
    for attr in URL_ATTRS.get(n.tag, []):
        v = n.attrs.get(attr)
        if v is None:
            continue
        if attr == "srcset":
            for cand in v.split(","):
                if cand.strip():
                    yield attr, cand.split()[0]
        else:
            yield attr, v


def check_links(root, docs):
    ids = {name: {n.attrs["id"] for n in elements(doc) if "id" in n.attrs} for name, doc in docs.items()}
    for name, doc in docs.items():
        for n in elements(doc):
            for attr, v in urls(n):
                where = f"{name}:{n.line}"
                if SCHEME.match(v):
                    continue
                if v.startswith("/"):
                    problem("LINK", f"{where}  {attr}=\"{v}\" - starts with /, which breaks on the GitHub Pages "
                                    "project site and on double-click; write it relative, without the /")
                    continue
                path, _, frag = v.partition("#")
                path = path.split("?", 1)[0]
                if not path:
                    if frag not in ids[name]:
                        problem("LINK", f"{where}  {attr}=\"{v}\" - no id=\"{frag}\" on this page")
                    continue
                if not exists_exact(root, unquote(path)):
                    problem("LINK", f"{where}  {attr}=\"{v}\" - no file with exactly that name "
                                    "(GitHub Pages is case-sensitive, even though Windows is not)")
                    continue
                if frag and path in ids and frag not in ids[path]:
                    problem("LINK", f"{where}  {attr}=\"{v}\" - {path} has no id=\"{frag}\"")
                if n.tag == "a" and name == ONE and path in PAGES + [ONE] \
                        and not (inside(n, "layout-switch") and v == "index.html"):
                    problem("LINK", f"{where}  href=\"{v}\" - on {ONE} links to the pages must point at sections "
                                    "(\"#...\"); the rule is in the README, The two layouts")
                if n.tag == "a" and name != ONE and path == ONE and not inside(n, "layout-switch"):
                    problem("LINK", f"{where}  href=\"{v}\" - the five pages link to {ONE} only from the switch")


# ---------- check 3b: every url() in styles.css names a file, with that exact case ----------
CSS_URL = re.compile(r"""url\(\s*(['"]?)([^'")]+)\1\s*\)""")


def check_css_urls(root):
    """GitHub Pages is case-sensitive and Windows is not, so a font whose file name differs only in
    case renders on the desk and silently falls back on the web. The link check above never reads
    the stylesheet, so this does."""
    path = root / "styles.css"
    if not path.exists():
        problem("MISSING", f"styles.css is not in {root}")
        return
    css = path.read_text(encoding="utf-8-sig")
    for m in CSS_URL.finditer(css):
        v = m.group(2).strip()
        line = css.count("\n", 0, m.start()) + 1
        if SCHEME.match(v) or v.startswith("#"):
            continue
        if v.startswith("/"):
            problem("LINK", f"styles.css:{line}  url({v}) - starts with /, which breaks on the GitHub Pages "
                            "project site and on double-click; write it relative, without the /")
            continue
        if not exists_exact(root, unquote(v.split("?", 1)[0])):
            problem("LINK", f"styles.css:{line}  url({v}) - no file with exactly that name "
                            "(GitHub Pages is case-sensitive, even though Windows is not)")


def exists_exact(root, rel):
    cur = root
    for seg in rel.split("/"):
        if seg in ("", "."):
            continue
        try:
            if seg not in os.listdir(cur):
                return False
        except (NotADirectoryError, FileNotFoundError):
            return False
        cur = cur / seg
    return cur.exists()


# ---------- check 4: head tags, skip link, header, footer; the switch; aria-current ----------
def chrome(doc):
    parts = []
    head = elements(doc, "head")
    for n in (head[0].children if head else []):
        if not isinstance(n, Node):
            continue
        if n.tag == "meta" and ("charset" in n.attrs or n.attrs.get("name") in ("viewport", "theme-color")):
            parts.append(n)
        elif n.tag == "link" and set(n.attrs.get("rel", "").split()) & CHROME_LINK_RELS:
            parts.append(n)
    body = elements(doc, "body")
    parts += [n for n in (body[0].children if body else [])
              if isinstance(n, Node) and (n.tag in ("header", "footer") or "skip-link" in classes(n))]
    return parts


WRONG_HEADING = "Pages (one-page.html should say Sections here)"


def chrome_norms(is_one):
    """The footer column is headed Sections on one-page.html and Pages on the five pages (difference 7)."""
    def norm(n):
        if "layout-switch" in classes(n):
            return None                                   # checked on its own, exactly
        tag, attrs = norm_plain(n)
        attrs.pop("aria-current", None)                   # checked on its own
        if "href" in attrs:
            attrs["href"] = map_href(attrs["href"])
        if is_one and tag == "nav" and inside_tag(n, "footer"):
            label_ = attrs.get("aria-label")
            attrs["aria-label"] = "Pages" if label_ == "Sections" else (WRONG_HEADING if label_ == "Pages" else label_)
        return tag, attrs

    def text(t):
        if is_one and t.parent.tag == "h3" and inside_tag(t, "footer") and t.text in ("Sections", "Pages"):
            return "Pages" if t.text == "Sections" else WRONG_HEADING
        return t.text
    return norm, text


def switch_expected(name, labels, div_attrs):
    """The exact switch markup for a page, from index.html's labels (so a consistent rename is fine)."""
    here, there = labels
    div = ("open", ("div", tuple(sorted(div_attrs.items()))), None)
    span = lambda txt: [("open", ("span", (("aria-current", "true"),)), None), ("text", txt, None), ("close", "span", None)]
    link = lambda href, txt: [("open", ("a", (("href", href),)), None), ("text", txt, None), ("close", "a", None)]
    if name == ONE:
        body = link("index.html", here) + span(there)
    else:
        body = span(here) + link(SWITCH_TARGET[name], there)
    return [div] + body + [("close", "div", None)]


def check_chrome(docs):
    langs = {name: (elements(doc, "html")[0].attrs.get("lang") if elements(doc, "html") else None)
             for name, doc in docs.items()}
    for name, lang in langs.items():
        if lang != langs["index.html"]:
            problem("CHROME", f"{name}: <html lang=\"{lang}\"> differs from index.html's lang=\"{langs['index.html']}\"")
    ref_norm, ref_text = chrome_norms(False)
    ref = [tok for n in chrome(docs["index.html"]) for tok in stream(n, ref_norm, ref_text)]
    for name in PAGES[1:] + [ONE]:
        norm, text = chrome_norms(name == ONE)
        got = [tok for n in chrome(docs[name]) for tok in stream(n, norm, text)]
        d = first_difference(ref, got)
        if d:
            x, y = d
            problem("CHROME", "head tags / skip link / top bar / footer differ",
                    f"index.html:{x[2] if x else '-'}  {show(x)}", f"{name}:{y[2] if y else '-'}  {show(y)}")
    # the switch, exactly
    ix = [n for n in elements(docs["index.html"]) if "layout-switch" in classes(n)]
    kids = [c for c in ix[0].children if isinstance(c, Node)] if len(ix) == 1 else []
    if len(kids) != 2 or kids[0].tag != "span" or kids[1].tag != "a":
        problem("SWITCH", "index.html: the Multi-page | One-page switch must be one <span aria-current=\"true\"> "
                          "then one <a href=\"one-page.html\">; the other pages are checked against it")
        return
    labels = (text_of(kids[0]), text_of(kids[1]))
    div_attrs = dict(norm_plain(ix[0])[1])
    for name in PAGES + [ONE]:
        doc = docs[name]
        sws = [n for n in elements(doc) if "layout-switch" in classes(n)]
        if len(sws) != 1 or not inside_tag(sws[0], "header"):
            problem("SWITCH", f"{name}: needs exactly one Multi-page | One-page switch, in the top bar; has {len(sws)}")
        else:
            d = first_difference(switch_expected(name, labels, div_attrs), stream(sws[0], norm_plain))
            if d:
                x, y = d
                problem("SWITCH", f"{name}:{sws[0].line}  the switch differs from what this page needs",
                        f"expected  {show(x)}", f"found     {show(y)}")
        # aria-current="page": only the Main nav link to the page itself (none on index, legal or one-page.html)
        if name == ONE:
            for n in elements(doc):
                if "aria-current" in n.attrs and not inside(n, "layout-switch"):
                    problem("CURRENT", f"{ONE}:{n.line}  no link on {ONE} is the current page; remove aria-current")
            continue
        marked = [n for n in elements(doc) if n.attrs.get("aria-current") == "page"]
        own = [n for n in marked if inside_tag(n, "nav", **{"aria-label": "Main"}) and n.attrs.get("href") == name]
        for n in marked:
            if n not in own:
                problem("CURRENT", f"{name}:{n.line}  aria-current=\"page\" belongs only on the Main nav link to {name}")
        has_nav_link = any(a.attrs.get("href") == name for a in elements(doc, "a")
                           if inside_tag(a, "nav", **{"aria-label": "Main"}))
        if has_nav_link and len(own) != 1:
            problem("CURRENT", f"{name}: the Main nav link to {name} needs aria-current=\"page\"")


# ---------- check 5: the three Talk to a broker bands left off one-page.html ----------
def check_bands(docs, secs):
    bands = {}
    for name in BAND_PAGES:
        found = [s for s in secs[name] if is_band(name, s)]
        if len(found) != 1:
            problem("BAND", f"{name}: expected one Talk to a broker band at the end of <main>, found {len(found)}")
        else:
            bands[name] = found[0]
    if not bands:
        return
    ref_name, ref = next(iter(bands.items()))
    ref_stream = stream(ref, norm_plain)
    for name, b in bands.items():
        d = first_difference(ref_stream, stream(b, norm_plain))
        if d:
            x, y = d
            problem("BAND", "the Talk to a broker bands differ",
                    f"{ref_name}:{x[2] if x else ref.line}  {show(x)}", f"{name}:{y[2] if y else b.line}  {show(y)}")
    contact = first(docs["about.html"], lambda n: n.attrs.get("id") == "contact")
    if contact is None:
        problem("BAND", "about.html has no id=\"contact\" section")
        return
    have = {t.text for t in walk(contact) if isinstance(t, Text) and t.text}
    for t in walk(ref):
        if isinstance(t, Text) and t.text and not inside(t, "btn") and t.text not in have:
            problem("BAND", f"{ref_name}:{t.line}  the band says \"{t.text[:80]}\", which about.html's Contact "
                            f"section does not; {ONE} leaves the bands out, so this would be missing there")


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    docs = {name: parse(root, name) for name in PAGES + [ONE]}
    sections = []
    if all(d is not None for d in docs.values()):
        secs = {name: main_sections(doc, name) for name, doc in docs.items()}
        check_body(docs)
        sections = check_text(secs)
        check_structure(docs, secs)
        check_links(root, docs)
        check_css_urls(root)
        check_chrome(docs)
        check_bands(docs, secs)
    if problems:
        for kind, lines in problems:
            print(f"{kind:<10} {lines[0]}")
            for extra in lines[1:]:
                print(" " * 11 + extra)
        print(f"\n{len(problems)} problem{'s' if len(problems) != 1 else ''}. The five pages are the master: "
              f"make {ONE} match them, then run this again.")
        return 1
    main_el = elements(docs[ONE], "main")[0]
    words = sum(len(t.text.split()) for t in walk(main_el) if isinstance(t, Text) and t.text)
    open_ph = sum(1 for n in elements(main_el) if "ph" in classes(n))
    left = f"{open_ph} placeholder{'s' if open_ph != 1 else ''} still to fill" if open_ph else "no placeholders left"
    print(f"OK - {ONE} matches the five pages: {len(sections)} sections, {words} words, {left}.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # the checker itself broke: say so, and never look like "drift found"
        print(f"CHECKER ERROR ({type(exc).__name__}): {exc}")
        sys.exit(2)
