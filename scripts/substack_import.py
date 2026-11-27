#!/usr/bin/env python3
"""Import The Pricing Conundrum into the repository (AGENTS.md section 16).

Two sources, one output:

    python3 scripts/substack_import.py --export /path/to/unzipped-export   # Substack export (all posts, full text)
    python3 scripts/substack_import.py --add --title "..." --date YYYY-MM-DD --url URL [--subtitle "..."] [--paid]
                                                                           # record a new piece seen on the public archive page
    python3 scripts/substack_import.py --feed                              # the public RSS feed (Substack currently refuses
                                                                           # automated requests from GitHub, so this may fail)

Writes one Markdown file per published post to substack/posts/YYYY-MM-DD-<slug>.md and rebuilds the
catalogue in _data/substack/published.yml. Existing files are never overwritten with shorter text, so a
paid post first imported from the feed (preview only) is replaced when a later export brings the full text.
Drafts, unpublished posts and the subscriber list are never imported.

Needs: pandoc, beautifulsoup4, pyyaml.
"""
import argparse, csv, json, os, re, subprocess, sys, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
import yaml
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, "substack", "posts")
CATALOG = os.path.join(ROOT, "_data", "substack", "published.yml")
BASE = "https://thepricingconundrum.substack.com"

# ---------------------------------------------------------------- classification
THEMES = [  # (pattern on title + subtitle + url, theme); first three matches win
    (r"price change communication|diocletian|13th century shrinkflation|planned price increase|1963", "Price-change communication series"),
    (r"ai shopping agent|behavioral pricing tactics dying", "AI shopping agents"),
    (r"\bai\b|ai-|outcome-based|credit-based|ai pricing|ai products|ai-native|ai renewal|personalization in customer", "AI pricing"),
    (r"hall and hitch|1939|ginzberg|1936|lanzillotti|gardiner means|dewey|elizabeth anderson|purgatory|coin in the coffer|history of explaining", "History of pricing thought"),
    (r"transparency|disclos", "Price transparency"),
    (r"shrinkflation|junk fee|resort fee|surcharge|stealthy price|tomato vacation|pink tax", "Fees and hidden price increases"),
    (r"fair|taj mahal|dual ticket|higher consumer demand doesn|domino|restraint|greedflation|regressive|unaffordab", "Price fairness"),
    (r"dynamic|variable|frequent price changes|changing constantly|griddy|electricity in texas|fifa|life of a price", "Dynamic and variable pricing"),
    (r"promotion|coupon|black friday|matka|everyday low|bed bath|apex blend|strikethrough|20% off", "Promotions"),
    (r"subscription|consent|prime membership|unlimited|two-part|costco|loyalty|sandals|all-inclusive|flat-rate", "Subscriptions"),
    (r"legal|court|\blaw\b", "Legal and regulation"),
    (r"b2b|oilfield|drilling|ironwood|sentinel|streamline energy|kaval|cepheid|lenacapavir|gilead|sotheby|two-sided", "B2B pricing"),
    (r"value-based|value pricing|price structure|price level|cost-based|four pillars|decision inputs|good pricing decision|willingness to pay|list price map|experience curves|incremental|houston symphony|capability gap|pricing organization|vulnerable", "Pricing strategy fundamentals"),
    (r"psycholog|price point|left-digit|ending in the number 8|informational value|high prices attract|low prices can backfire|distinctiveness|threshold|name your own|pay what you want|price image|salve|affordances|decision journey|good price|cost per use|big purchases|\$2\.95|hermes|birkin|moonswatch|payless|horsehair|artist|movies-on-demand|every price tells|cash or a credit|doom spending", "Consumer psychology"),
    (r"hermes|birkin|moonswatch|luxury", "Luxury and status"),
    (r"valuation|financialization|purchases from investments|pluralist|wedding gift", "Valuation theory"),
    (r"survey|backward research|quantitative information|growth rate numbers", "Research and analysis methods"),
    (r"prepay|wedding gift|shop smartly|cash or a credit|good price\?", "Consumer advice"),
    (r"why you should subscribe|end-of-year post|thanking", "About the publication"),
]
THEME_OVERRIDES = {  # slug -> themes, where the patterns misfire
    "coming-soon": ["About the publication"],
    "unaffordability-and-the-doom-spending": ["Consumer psychology", "Price fairness"],
    "predicate-ai-pricing-an-ai-native": ["AI pricing", "B2B pricing"],
    "predicate-ai-pricing-an-ai-native-b8f": ["AI pricing", "B2B pricing"],
    "how-to-benefit-from-a-planned-price": ["Price-change communication series", "History of pricing thought"],
}
KINDS = ("essay", "case-study", "teaching-case", "teaching-note", "concept", "book-excerpt", "talk", "publication-note")


def classify(title, subtitle, slug):
    hay = f"{title} {subtitle} {slug}".lower()
    if slug in THEME_OVERRIDES:
        themes = THEME_OVERRIDES[slug]
    else:
        themes = []
        for pat, t in THEMES:
            if re.search(pat, hay) and t not in themes:
                themes.append(t)
        themes = themes[:3] or ["Pricing strategy fundamentals"]
    tl, sl = title.lower(), subtitle.lower()
    if "teaching note" in tl or tl.endswith("problem solution"):
        kind = "teaching-note"
    elif re.search(r"maverick drilling|ironwood|sentinel solutions|kaval|apex blend|streamline energy|predicate ai|orchestra problem$|case study: pricing the 2026 fifa", tl) or "case study about" in sl or "a case study on" in sl:
        kind = "teaching-case"
    elif "edited version of chapter" in sl:
        kind = "book-excerpt"
    elif re.search(r"subscribe to the pricing conundrum|end-of-year post", tl):
        kind = "publication-note"
    elif "slide deck" in sl:
        kind = "talk"
    elif "case study" in tl:
        kind = "case-study"
    elif re.search(r"^pricing (tool|concept)|framework|four pillars|method in six steps", tl):
        kind = "concept"
    else:
        kind = "essay"
    return themes, kind


# ---------------------------------------------------------------- HTML -> Markdown
def html_to_md(html):
    s = BeautifulSoup(html, "html.parser")
    for t in s.select("button, svg, div.image-link-expand, div.subscription-widget-wrap-editor, div.subscription-widget, p.button-wrapper"):
        t.decompose()
    for pic in s.find_all("picture"):
        img = pic.find("img")
        pic.replace_with(img) if img else pic.decompose()
    for img in s.find_all("img"):
        img.replace_with(s.new_tag("img", src=img.get("src", ""), alt=img.get("alt") or ""))
    for a in s.select("a.image-link"):
        a.unwrap()
    for f in s.find_all("iframe"):
        src = f.get("src", "")
        p = s.new_tag("p"); a = s.new_tag("a", href=src)
        a.string = "Embedded content: " + (src.split("/")[2] if "//" in src else src)
        p.append(a); f.replace_with(p)
    for e in s.select("div.twitter-embed, div.instagram-embed-wrap, div.native-audio-embed"):
        links = [x.get("href") for x in e.find_all("a") if x.get("href")]
        m = re.search(r'"url":"([^"]+)"', e.get("data-attrs") or "")
        url = links[0] if links else (m.group(1) if m else None)
        p = s.new_tag("p")
        if url:
            a = s.new_tag("a", href=url); a.string = "Embedded post: " + url; p.append(a)
        else:
            p.string = "[Embedded social post not preserved in the export]"
        e.replace_with(p)
    for a in s.select("a.footnote-anchor"):
        a.replace_with(f"[^{a.get_text(strip=True)}]")
    notes = []
    for d in s.select("div.footnote"):
        num = d.select_one("a.footnote-number")
        content = d.select_one("div.footnote-content")
        notes.append((num.get_text(strip=True) if num else str(len(notes) + 1), str(content) if content else ""))
        d.decompose()
    body = pandoc(str(s))
    body = re.sub(r"\\\[\^(\w+)\\\]", r"[^\1]", body)
    body = re.sub(r"\[\^(\w+)\\\]", r"[^\1]", body)
    if notes:
        body += "\n\n"
        for n, c in notes:
            text = re.sub(r"\s*\n+\s*", " ", pandoc(c)).strip()
            body += "[^" + n + "]: " + text + "\n"
    return re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"


def pandoc(html):
    r = subprocess.run(["pandoc", "-f", "html", "-t", "gfm-raw_html", "--wrap=none"], input=html,
                       capture_output=True, text=True, check=True)
    return r.stdout.strip()


def word_count(md):
    return len(re.findall(r"\b\w+\b", re.sub(r"\(https?://[^)]*\)|!\[[^\]]*\]|<https?://[^>]*>", " ", md)))


# ---------------------------------------------------------------- writing
def write_post(meta, body, source):
    """Write one post unless a fuller version already exists. Returns True if written."""
    os.makedirs(POSTS, exist_ok=True)
    fn = f"{meta['date']}-{meta['slug']}.md"
    path = os.path.join(POSTS, fn)
    for old in os.listdir(POSTS):  # same slug under another date (date edits on Substack)
        if old.endswith(f"-{meta['slug']}.md") and old != fn:
            path = os.path.join(POSTS, old); fn = old
    words = word_count(body)
    if os.path.exists(path):
        old_words = int(re.search(r"^word_count: (\d+)", open(path, encoding="utf-8").read(), re.M).group(1))
        if old_words >= words:
            return False
    fm = dict(meta, word_count=words, full_text=source == "export" or (source == "feed" and meta["audience"] == "free"), imported_from=source)
    head = "---\n" + "".join(f"{k}: {json.dumps(v, ensure_ascii=False)}\n" for k, v in fm.items()) + "---\n\n"
    open(path, "w", encoding="utf-8").write(head + body)
    return True


def from_export(d):
    n = 0
    for r in csv.DictReader(open(os.path.join(d, "posts.csv"), encoding="utf-8")):
        if r["is_published"] != "true" or r["type"] != "newsletter" or not r["post_date"]:
            continue
        pid, slug = r["post_id"].split(".", 1)
        path = os.path.join(d, "posts", r["post_id"] + ".html")
        if not os.path.exists(path):
            print("missing:", path, file=sys.stderr); continue
        meta = {"title": r["title"].strip(), "subtitle": (r["subtitle"] or "").strip(), "date": r["post_date"][:10],
                "slug": slug, "url": f"{BASE}/p/{slug}",
                "audience": "paid" if r["audience"] == "only_paid" else "free", "post_id": int(pid)}
        n += write_post(meta, html_to_md(open(path, encoding="utf-8").read()), "export")
    return n


def from_feed():
    req = urllib.request.Request(f"{BASE}/feed", headers={"User-Agent": "pricing-briefings-archive/1.0"})
    root = ET.fromstring(urllib.request.urlopen(req, timeout=60).read())
    ns = {"content": "http://purl.org/rss/1.0/modules/content/"}
    n = 0
    for it in root.iter("item"):
        link = it.findtext("link") or ""
        m = re.search(r"/p/([^/?#]+)", link)
        if not m:
            continue
        html = it.findtext("content:encoded", default="", namespaces=ns)
        date = datetime.strptime(it.findtext("pubDate"), "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc)
        paid = bool(re.search(r"paywall|This post is for paid subscribers", html, re.I))
        meta = {"title": (it.findtext("title") or "").strip(), "subtitle": (it.findtext("description") or "").strip(),
                "date": date.strftime("%Y-%m-%d"), "slug": m.group(1), "url": f"{BASE}/p/{m.group(1)}",
                "audience": "paid" if paid else "free", "post_id": None}
        n += write_post(meta, html_to_md(html), "feed")
    return n


def add_stub(title, date, url, subtitle, paid):
    """Record a piece seen on the public archive page: catalogue entry now, full text from the next export."""
    m = re.search(r"/p/([^/?#]+)", url)
    if not m or not re.match(r"\d{4}-\d{2}-\d{2}$", date):
        sys.exit("--add needs a Substack post URL (…/p/<slug>) and --date YYYY-MM-DD")
    slug = m.group(1)
    if any(fn.endswith(f"-{slug}.md") for fn in os.listdir(POSTS)):
        print(f"{slug} is already in the archive"); return 0
    body = (f"{subtitle}\n\n" if subtitle else "") + (
        "*Full text not yet imported: recorded from the public archive page. "
        "The next Substack export fills it in (AGENTS.md section 16).*\n")
    meta = {"title": title, "subtitle": subtitle, "date": date, "slug": slug, "url": f"{BASE}/p/{slug}",
            "audience": "paid" if paid else "free", "post_id": None}
    return int(write_post(meta, body, "archive-page"))


def rebuild_catalog():
    """Regenerate _data/substack/published.yml from the post files. Keeps hand-added fields (related, notes)."""
    keep = {}
    if os.path.exists(CATALOG):
        for row in yaml.safe_load(open(CATALOG, encoding="utf-8")) or []:
            keep[row["slug"]] = {k: row[k] for k in ("related_claims", "related_ideas", "notes") if row.get(k)}
    rows = []
    for fn in sorted(os.listdir(POSTS)):
        if not fn.endswith(".md"):
            continue
        text = open(os.path.join(POSTS, fn), encoding="utf-8").read()
        fm = yaml.safe_load(text.split("---\n", 2)[1])
        themes, kind = classify(fm["title"], fm.get("subtitle") or "", fm["slug"])
        rows.append({"slug": fm["slug"], "title": fm["title"], "subtitle": fm.get("subtitle") or "", "date": str(fm["date"]),
                     "url": fm["url"], "audience": fm["audience"], "kind": kind, "themes": themes,
                     "word_count": fm["word_count"], "full_text": fm.get("full_text", True),
                     "file": f"substack/posts/{fn}", "preview": "(PREVIEW)" in fm["title"].upper(), "version_of": None,
                     **keep.get(fm["slug"], {})})
    # versions (reposts, updated [year] editions, previews): point each at one canonical piece, the first full non-preview version
    norm = lambda t: re.sub(r"\s*\(preview\)|\s*\[\d{4}\]|^pricing (concept|tool|strategy): ", "", t.lower()).strip()
    groups = {}
    for r in sorted(rows, key=lambda r: r["date"]):
        groups.setdefault(norm(r["title"]), []).append(r)
    for g in groups.values():
        if len(g) < 2:
            continue
        canon = next((r for r in g if not r["preview"]), g[0])
        for r in g:
            if r is not canon:
                r["version_of"] = canon["slug"]
    rows.sort(key=lambda r: (r["date"], r["slug"]), reverse=True)
    header = ("# The Pricing Conundrum: every published piece. Generated by scripts/substack_import.py from substack/posts/;\n"
              "# do not edit by hand except the related_claims, related_ideas and notes fields, which are kept on rebuild.\n"
              "# AGENTS.md section 16. kind: " + " / ".join(KINDS) + "\n")
    open(CATALOG, "w", encoding="utf-8").write(header + yaml.safe_dump(rows, sort_keys=False, allow_unicode=True, width=1000))
    return len(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--export", help="folder of an unzipped Substack export")
    ap.add_argument("--feed", action="store_true", help="import new posts from the public RSS feed")
    ap.add_argument("--add", action="store_true", help="record one new piece seen on the public archive page")
    ap.add_argument("--title"); ap.add_argument("--date"); ap.add_argument("--url")
    ap.add_argument("--subtitle", default=""); ap.add_argument("--paid", action="store_true")
    a = ap.parse_args()
    if a.export:
        written = from_export(a.export)
    elif a.feed:
        written = from_feed()
    elif a.add:
        if not (a.title and a.date and a.url):
            ap.error("--add needs --title, --date and --url")
        written = add_stub(a.title.strip(), a.date, a.url, a.subtitle.strip(), a.paid)
    else:
        ap.error("give --export DIR, --add or --feed")
    total = rebuild_catalog()
    print(f"{written} post files written or updated; catalogue has {total} pieces")
