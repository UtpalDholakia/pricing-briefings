#!/usr/bin/env python3
"""Validate the research base before it reaches the site build.

Usage:
    python3 scripts/validate.py            # errors fail (exit 1); warnings are printed
    python3 scripts/validate.py --firms    # also print the firm registry report
    python3 scripts/validate.py --hypotheses   # also print the hypothesis hunt report

Checks (AGENTS.md sections 2, 6, 8, 10, 11):
  * every YAML file under _data/ parses
  * controlled vocabularies in the trackers, the AI pricing database and the pipeline
  * briefing front matter: required keys, agent key, date matches filename, 3-15 tags, all tags in _data/tags.yml
  * case_id / related_case_id slug format
  * mechanism_codes exist in _data/mechanisms.yml
  * firm registry (_data/firms.yml): unique IDs, listed case_ids exist, aliases match at least one entry (warning)
  * question_id slugs are unique; claims (_data/claims.yml): vocabularies, every evidence ref and related
    question/dive resolves, status_history is consistent with status, confirmed_by is null or 'utpal'
  * hypotheses (_data/hypotheses.yml, AGENTS.md section 13): vocabularies, non-empty predicts and test,
    at most 20 Testing, every evidence ref / related_claim / related question resolves, hunts consistent
    with hunt_count and last_hunted (never in the future), Graduated entries name a claim, history consistent,
    hypothesis_ids unique and never equal to a claim_id
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
NOT_ENTRIES = {"providers.yml", "questions.yml"}  # registries and questions are not counted as firm entries


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
    if path in ("_data/tags.yml", "_data/mechanisms.yml", "_data/firms.yml", "_data/claims.yml",
                "_data/hypotheses.yml"):
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
        # An entry is one row in an event tracker or the AI pricing change log / subscriptions.
        # Registries (providers.yml) and questions are not entries. The /firms/ page uses the same rule.
        matched, alias_hits = [], defaultdict(int)
        for path, recs in records_by_file.items():
            if os.path.basename(path) in NOT_ENTRIES:
                continue
            for r in recs:
                if not isinstance(r, dict):
                    continue
                by_case = r.get("case_id") in cids or r.get("related_case_id") in cids
                by_alias = False
                for fld in FIRM_FIELDS:
                    if r.get(fld) in aliases:
                        alias_hits[r[fld]] += 1
                        by_alias = True
                if by_alias and r.get("case_id") and r.get("case_id") not in cids:
                    warn(where, f"entry {r.get('case_id')!r} in {os.path.basename(path)} matches an alias "
                                f"but its case_id is not in case_ids (add it if the case is about this firm)")
                if by_case or by_alias:
                    matched.append((path, r))
        for a in aliases:
            if not alias_hits[a]:
                warn(where, f"alias {a!r} matches no entry")
        if len(matched) < 3:
            warn(where, f"only {len(matched)} entries (dossier threshold is 3)")
        dates = sorted(str(r.get("date") or r.get("started") or r.get("announced") or "")
                       for _, r in matched if (r.get("date") or r.get("started") or r.get("announced")))
        n_cases = len({r.get("case_id") for _, r in matched if r.get("case_id")})
        firm_report.append((fid, len(matched), n_cases, dates[0] if dates else None,
                            sorted({os.path.basename(p)[:-4] for p, _ in matched})))

# ---------------------------------------------------------------- 5. questions and claims
question_ids = set()
for i, q in enumerate(as_list(data.get("_data/trackers/questions.yml"))):
    qid = q.get("question_id") if isinstance(q, dict) else None
    if qid is not None:
        if not SLUG.match(str(qid)):
            err(f"_data/trackers/questions.yml[{i}]", f"question_id {qid!r} is not a lowercase slug")
        elif qid in question_ids:
            err(f"_data/trackers/questions.yml[{i}]", f"duplicate question_id {qid!r}")
        question_ids.add(qid)

evidence_ids = {r.get("id") for r in as_list(data.get("_data/trackers/pricing_evidence.yml")) if isinstance(r, dict)}
case_slugs = {os.path.basename(p)[:-3] for p in glob.glob("_cases/*.md")}
briefing_slugs = {os.path.basename(p)[:-3] for p in glob.glob("_briefings/*.md")}
CLAIM_STATUS = {"Open", "Supported", "Contested", "Refuted", "Dead"}
CONFIDENCE = {"High", "Medium", "Low"}
REF_KINDS = {
    "evidence": (evidence_ids, "pricing_evidence.yml id"),
    "tracker": (set(all_case_ids), "case_id in a tracker or database file"),
    "case": (case_slugs, "_cases/ slug"),
    "question": (question_ids, "question_id in questions.yml"),
    "briefing": (briefing_slugs, "_briefings/ file name"),
}
claims = data.get("_data/claims.yml")
claim_ids = set()
if claims is not None:
    seen = set()
    for c in as_list(claims):
        cid = c.get("claim_id")
        where = f"_data/claims.yml {cid}"
        if not cid or not SLUG.match(cid):
            err(where, "claim_id must be a lowercase slug")
        if cid in seen:
            err(where, "duplicate claim_id")
        seen.add(cid)
        claim_ids.add(cid)
        if not c.get("claim"):
            err(where, "missing claim sentence")
        if c.get("status") not in CLAIM_STATUS:
            err(where, f"status {c.get('status')!r} not in allowed values")
        if c.get("confidence") not in CONFIDENCE:
            err(where, f"confidence {c.get('confidence')!r} not in allowed values")
        if not c.get("agent") or c.get("agent") not in agents:
            err(where, "agent missing or not in _config.yml agents")
        for code in c.get("mechanism_codes") or []:
            if code not in mechanisms:
                err(where, f"mechanism code {code!r} is not in _data/mechanisms.yml")
        pointers = (c.get("evidence_for") or []) + (c.get("evidence_against") or [])
        for ptr in pointers:
            kind, ref = ptr.get("kind"), ptr.get("ref")
            if kind not in REF_KINDS:
                err(where, f"evidence kind {kind!r} not in {sorted(REF_KINDS)}")
            elif str(ref) not in REF_KINDS[kind][0]:
                err(where, f"{kind} ref {ref!r} does not resolve ({REF_KINDS[kind][1]})")
        for q in c.get("related_questions") or []:
            if q not in question_ids:
                err(where, f"related question {q!r} has no matching question_id")
        for d in c.get("related_dives") or []:
            if d not in case_slugs:
                err(where, f"related dive {d!r} not found in _cases/")
        hist = c.get("status_history") or []
        if not hist:
            err(where, "status_history is empty")
        else:
            if hist[0].get("old_status") is not None:
                err(where, "first status_history entry must have old_status: null")
            if hist[-1].get("new_status") != c.get("status"):
                err(where, "status does not match the last status_history entry")
            for h in hist:
                for k in ("date", "new_status", "reason", "proposed_by"):
                    if not h.get(k):
                        err(where, f"status_history entry missing {k}")
                if h.get("confirmed_by") not in (None, "utpal"):
                    err(where, "confirmed_by must be null or 'utpal'")
        if not pointers:
            created = c.get("created")
            try:
                age = (datetime.date.today() - datetime.date.fromisoformat(str(created))).days
            except ValueError:
                age = 0
            if age > 30:
                warn(where, "no evidence after 30 days: move it to questions.yml or mark it Dead")


# ---------------------------------------------------------------- 6. hypotheses
HYP_STATUS = {"Testing", "Graduated", "Dead"}
HUNT_OUTCOME = {"hit", "miss"}
TESTING_CAP = 20
hyp_report = {"testing": 0, "unhunted": [], "review": []}


def as_date(v):
    if isinstance(v, datetime.date):
        return v
    try:
        return datetime.date.fromisoformat(str(v))
    except ValueError:
        return None


hyps = data.get("_data/hypotheses.yml")
if hyps is not None:
    if not isinstance(hyps, list):
        err("_data/hypotheses.yml", "must be a list")
        hyps = []
    today = datetime.date.today()
    seen = set()
    for h in hyps:
        if not isinstance(h, dict):
            err("_data/hypotheses.yml", "every entry must be a mapping")
            continue
        hid = h.get("hypothesis_id")
        where = f"_data/hypotheses.yml {hid}"
        if not hid or not SLUG.match(str(hid)):
            err(where, "hypothesis_id must be a lowercase slug")
        if hid in seen:
            err(where, "duplicate hypothesis_id")
        if hid in claim_ids:
            err(where, "hypothesis_id collides with a claim_id (graduation creates a new claim_id)")
        seen.add(hid)
        for k in ("hypothesis", "predicts", "test"):
            if not str(h.get(k) or "").strip():
                err(where, f"{k} is empty (no test, no hypothesis: move it to questions.yml)")
        status = h.get("status")
        if status not in HYP_STATUS:
            err(where, f"status {status!r} not in allowed values")
        if h.get("confidence") not in CONFIDENCE:
            err(where, f"confidence {h.get('confidence')!r} not in allowed values")
        if not h.get("agent") or h.get("agent") not in agents:
            err(where, "agent missing or not in _config.yml agents")
        if not h.get("lanes"):
            err(where, "lanes is empty")
        for ptr in (h.get("evidence_for") or []) + (h.get("evidence_against") or []):
            kind, ref = ptr.get("kind"), ptr.get("ref")
            if kind not in REF_KINDS:
                err(where, f"evidence kind {kind!r} not in {sorted(REF_KINDS)}")
            elif str(ref) not in REF_KINDS[kind][0]:
                err(where, f"{kind} ref {ref!r} does not resolve ({REF_KINDS[kind][1]})")
        rc = h.get("related_claim")
        if rc is not None and rc not in claim_ids:
            err(where, f"related_claim {rc!r} is not a claim_id")
        if status == "Graduated" and not rc:
            err(where, "a Graduated hypothesis must name its related_claim")
        for q in h.get("related_questions") or []:
            if q not in question_ids:
                err(where, f"related question {q!r} has no matching question_id")
        hunts = h.get("hunts") or []
        if h.get("hunt_count") != len(hunts):
            err(where, f"hunt_count {h.get('hunt_count')!r} does not equal the number of hunts ({len(hunts)})")
        hunt_dates = []
        for hu in hunts:
            for k in ("date", "agent", "outcome", "note"):
                if not hu.get(k):
                    err(where, f"hunt entry missing {k}")
            if hu.get("outcome") and hu["outcome"] not in HUNT_OUTCOME:
                err(where, f"hunt outcome {hu['outcome']!r} not in {sorted(HUNT_OUTCOME)}")
            if hu.get("agent") and hu["agent"] not in agents:
                err(where, f"hunt agent {hu['agent']!r} not in _config.yml agents")
            dd = as_date(hu.get("date"))
            if dd:
                hunt_dates.append(dd)
        lh = h.get("last_hunted")
        if lh is not None:
            lhd = as_date(lh)
            if not lhd:
                err(where, f"last_hunted {lh!r} is not an ISO date")
            elif lhd > today:
                err(where, "last_hunted is in the future")
            elif hunt_dates and lhd != max(hunt_dates):
                err(where, "last_hunted does not equal the latest hunt date")
        elif hunts:
            err(where, "hunts are logged but last_hunted is null")
        hist = h.get("history") or []
        if not hist:
            err(where, "history is empty")
        else:
            if hist[0].get("old_status") is not None:
                err(where, "first history entry must have old_status: null")
            if hist[-1].get("new_status") != status:
                err(where, "status does not match the last history entry")
            for e in hist:
                for k in ("date", "new_status", "reason"):
                    if not e.get(k):
                        err(where, f"history entry missing {k}")
        if status == "Testing":
            hyp_report["testing"] += 1
            hyp_report["unhunted"].append((str(lh) if lh else "never", hid))
            has_evidence = bool(h.get("evidence_for") or h.get("evidence_against"))
            misses = [hu for hu in hunts if hu.get("outcome") == "miss"]
            if len(hunts) >= 3 and not has_evidence:
                hyp_report["review"].append(hid)
                warn(where, f"{len(hunts)} hunts and no evidence: review (keep hunting with a reason, or mark Dead)")
    if hyp_report["testing"] > TESTING_CAP:
        err("_data/hypotheses.yml", f"{hyp_report['testing']} hypotheses in Testing (cap is {TESTING_CAP})")

# ---------------------------------------------------------------- output
if "--firms" in sys.argv:
    print("Firm registry report (firm_id, entries, cases, first_seen, files):")
    for row in sorted(firm_report, key=lambda x: -x[1]):
        print("  ", *row)
if "--hypotheses" in sys.argv and hyps is not None:
    print(f"Hypotheses: {hyp_report['testing']} of {TESTING_CAP} Testing slots in use")
    order = sorted(hyp_report["unhunted"], key=lambda x: (x[0] != "never", x[0]))
    print("  longest unhunted:", ", ".join(f"{hid} ({d})" for d, hid in order[:5]) or "none")
    print("  due a 3-hunt review:", ", ".join(hyp_report["review"]) or "none")
for w in warnings:
    print("WARNING", w)
for e in errors:
    print("ERROR", e)
print(f"{len(errors)} errors, {len(warnings)} warnings")
sys.exit(1 if errors else 0)
