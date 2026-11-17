#!/usr/bin/env python3
"""Validate the research base before it reaches the site build.

Usage:
    python3 scripts/validate.py            # errors fail (exit 1); warnings are printed
    python3 scripts/validate.py --firms    # also print the firm registry report

Checks (AGENTS.md sections 2, 6, 8, 10, 11):
  * every YAML file under _data/ parses
  * controlled vocabularies in the trackers, the AI pricing database and the pipeline
  * briefing front matter: required keys, agent key, date matches filename, 3-15 tags, all tags in _data/tags.yml
  * case_id / related_case_id slug format
  * mechanism_codes exist in _data/mechanisms.yml
  * firm registry (_data/firms.yml): unique IDs, listed case_ids exist, aliases match at least one entry (warning)
Needs only Python 3 and PyYAML.
"""
import datetime
import glob
import os
import re
import sys
from collections import defaultdict

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

errors, warnings = [], []


def err(where, msg):
    errors.append(f"{where}: {msg}")


def warn(where, msg):
    warnings.append(f"{where}: {msg}")


# ---------------------------------------------------------------- vocabularies
OUTCOME = {"Ongoing", "Reversed", "Partially reversed", "Held", "Mitigated", "Unknown"}
VOCAB = {
    "_data/trackers/backlash.yml": {"reversed": {"Yes", "No", "Partial", "Pending", "Unknown"}},
    "_data/trackers/explanations.yml": {
        "category": {"Apology", "Cost", "Capacity / market", "Pledge", "Deflect to third party",
                     "Refusal to cut", "Restraint", "Screening", "Lower list price", "Efficiency",
                     "Auditability", "Reference-point reframing", "Value / quality", "Evidence"},
        "outcome": OUTCOME,
    },
    "_data/trackers/essential_prices.yml": {
        "outcome": OUTCOME,
        "sector": {"Energy", "Tuition", "Healthcare", "Housing", "Food"},
    },
    "_data/trackers/laws.yml": {"status": {"Proposed", "Passed", "Enacted", "In force", "Vetoed",
                                           "Under challenge", "Withdrawn"}},
    "_data/trackers/stories.yml": {"status": {"Open", "Closed", "Dormant"}},
    "_data/trackers/b2b_pricing.yml": {
        "mechanism": {"seat-based", "usage-based", "credits", "flat", "outcome-based"},
        "price_type": {"list", "net", "quote"},
    },
    "_data/trackers/questions.yml": {
        "status": {"Open", "In progress", "Answered", "Dead end"},
        "priority": {"High", "Medium", "Low"},
    },
    "_data/ai_pricing/price_changes.yml": {
        "mechanism": {"per-token", "per-seat", "credits", "per-job", "outcome-based",
                      "flat-subscription", "usage-tier", "free"},
        "change_type": {"price-cut", "price-rise", "allowance-cut", "allowance-rise", "new-tier",
                        "tier-removed", "mechanism-change", "new-model", "model-retired",
                        "credit-repricing", "free-tier-change", "other"},
    },
    "_data/ai_pricing/subscriptions.yml": {
        "mechanism": {"per-token", "per-seat", "credits", "per-job", "outcome-based",
                      "flat-subscription", "usage-tier", "free"},
    },
    "_data/substack/ideas.yml": {
        "status": {"idea", "outlining", "drafting", "ready", "published", "parked", "dead"},
        "priority": {"High", "Medium", "Low"},
        "source_type": {"question", "deep-dive", "briefing", "tracker", "utpal"},
    },
}
# Section 6 case trackers: every entry should carry last_checked and follow_up_date.
CASE_TRACKERS = ["explanations", "backlash", "stories", "essential_prices", "nonwestern_pricing",
                 "hidden_increases", "laws", "ai_agents", "ai_product_pricing", "b2b_pricing"]
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATEISH = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")
FIRM_FIELDS = ("firm", "firm_or_place", "provider", "who", "offer")


def as_list(data):
    """Return the list of records in a data file (list at top level, or the first list in a dict)."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for v in data.values():
            if isinstance(v, list):
                return v
    return []


# ---------------------------------------------------------------- 1. YAML parses
data = {}
for path in sorted(glob.glob("_data/**/*.yml", recursive=True)):
    try:
        with open(path, encoding="utf-8") as fh:
            data[path] = yaml.safe_load(fh)
    except yaml.YAMLError as exc:
        err(path, f"YAML does not parse: {str(exc).splitlines()[0]}")

mechanisms = set()
if isinstance(data.get("_data/mechanisms.yml"), list):
    codes = [m.get("code") for m in data["_data/mechanisms.yml"]]
    mechanisms = set(codes)
    for c in codes:
        if not c or not SLUG.match(c):
            err("_data/mechanisms.yml", f"bad code {c!r}")
    if len(codes) != len(mechanisms):
        err("_data/mechanisms.yml", "duplicate codes")

# ---------------------------------------------------------------- 2. records
all_case_ids = defaultdict(list)       # case_id -> [file]
records_by_file = {}
for path, d in data.items():
    if path in ("_data/tags.yml", "_data/mechanisms.yml", "_data/firms.yml"):
        continue
    recs = as_list(d)
    records_by_file[path] = recs
    vocab = VOCAB.get(path, {})
    short = os.path.basename(path)[:-4]
    for i, r in enumerate(recs):
        if not isinstance(r, dict):
            continue
        where = f"{path}[{i}] {r.get('case_id') or r.get('id') or r.get('idea') or ''}".strip()
        for field, allowed in vocab.items():
            if field in r and r[field] is not None and str(r[field]) not in allowed:
                err(where, f"{field}={r[field]!r} not in allowed values")
        for k in ("case_id", "related_case_id"):
            v = r.get(k)
            if v is not None:
                if not isinstance(v, str) or not SLUG.match(v):
                    err(where, f"{k} {v!r} is not a lowercase slug")
                else:
                    all_case_ids[v].append(path)
        for code in r.get("mechanism_codes") or []:
            if code not in mechanisms:
                err(where, f"mechanism code {code!r} is not in _data/mechanisms.yml")
        for k in ("date", "last_checked", "follow_up_date", "outcome_date", "updated", "next_check"):
            v = r.get(k)
            if v is not None and not isinstance(v, datetime.date) and not DATEISH.match(str(v)):
                warn(where, f"{k}={v!r} is not an ISO date")
        if short in CASE_TRACKERS:
            for k in ("last_checked", "follow_up_date"):
                if k not in r:
                    warn(where, f"missing {k}")

# ---------------------------------------------------------------- 3. briefings
tags = set(data.get("_data/tags.yml") or [])
with open("_config.yml", encoding="utf-8") as fh:
    agents = set((yaml.safe_load(fh) or {}).get("agents", {}).keys())
FNAME = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z]+)(?:-[a-z0-9-]+)?\.md$")
for path in sorted(glob.glob("_briefings/*.md")):
    name = os.path.basename(path)
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if not text.startswith("---"):
        err(path, "no front matter")
        continue
    try:
        fm = yaml.safe_load(text.split("---", 2)[1]) or {}
    except yaml.YAMLError as exc:
        err(path, f"front matter does not parse: {str(exc).splitlines()[0]}")
        continue
    for k in ("title", "agent", "date", "summary", "tags"):
        if not fm.get(k):
            err(path, f"front matter missing {k}")
    m = FNAME.match(name)
    if not m:
        err(path, "filename is not YYYY-MM-DD-<agent>[-slug].md")
    else:
        if str(fm.get("date")) != m.group(1):
            err(path, f"date {fm.get('date')} does not match filename")
        if fm.get("agent") != m.group(2):
            err(path, f"agent {fm.get('agent')!r} does not match filename")
    if fm.get("agent") and fm["agent"] not in agents:
        err(path, f"agent {fm['agent']!r} not in _config.yml agents")
    t = fm.get("tags") or []
    if not 3 <= len(t) <= 15:
        warn(path, f"{len(t)} tags (expected 3-15)")
    for tag in t:
        if tag not in tags:
            err(path, f"tag {tag!r} not in _data/tags.yml")

# ---------------------------------------------------------------- 4. firm registry
firms = data.get("_data/firms.yml")
firm_report = []
if firms is not None:
    if not isinstance(firms, list):
        err("_data/firms.yml", "must be a list")
        firms = []
    seen = set()
    for f in firms:
        fid = f.get("firm_id")
        where = f"_data/firms.yml {fid}"
        if not fid or not SLUG.match(fid):
            err(where, "firm_id must be a lowercase slug")
        if fid in seen:
            err(where, "duplicate firm_id")
        seen.add(fid)
        for k in ("name", "sector"):
            if not f.get(k):
                err(where, f"missing {k}")
        cids = set(f.get("case_ids") or [])
        aliases = set(f.get("aliases") or [])
        for c in cids:
            if c not in all_case_ids:
                err(where, f"case_id {c!r} not found in any tracker or database file")
        matched, alias_hits = [], defaultdict(int)
        for path, recs in records_by_file.items():
            for r in recs:
                if not isinstance(r, dict):
                    continue
                hit = r.get("case_id") in cids or r.get("related_case_id") in cids
                for fld in FIRM_FIELDS:
                    if r.get(fld) in aliases:
                        alias_hits[r[fld]] += 1
                        hit = True
                if hit:
                    matched.append((path, r))
        for a in aliases:
            if not alias_hits[a]:
                warn(where, f"alias {a!r} matches no entry")
        if len(matched) < 3:
            warn(where, f"only {len(matched)} entries (dossier threshold is 3)")
        dates = sorted(str(r.get("date") or r.get("started") or r.get("announced") or "")
                       for _, r in matched if (r.get("date") or r.get("started") or r.get("announced")))
        firm_report.append((fid, len(matched), dates[0] if dates else None,
                            sorted({os.path.basename(p)[:-4] for p, _ in matched})))

# ---------------------------------------------------------------- output
if "--firms" in sys.argv:
    print("Firm registry report (firm_id, entries, first_seen, files):")
    for row in sorted(firm_report, key=lambda x: -x[1]):
        print("  ", *row)
for w in warnings:
    print("WARNING", w)
for e in errors:
    print("ERROR", e)
print(f"{len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
