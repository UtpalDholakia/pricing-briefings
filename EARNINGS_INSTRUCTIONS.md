# Earnings pricing watch: instructions for ChatGPT

This is a second scheduled task for ChatGPT, separate from its daily briefing. It reads companies' earnings calls for what they say about their own prices and records one row per company per quarter in `_data/trackers/earnings_pricing.yml`. Over time this becomes a quarter-by-quarter record of pricing power, price cuts, pushback from buyers and how managers explain their prices, across 109 companies. Rules: AGENTS.md section 15.

## How to set it up

1. In ChatGPT, open **Scheduled** and create a new task named **Earnings pricing watch**.
2. Schedule it for **weekdays** (Monday to Friday), at a different time from the daily briefing, for example 2:00 p.m. Central, so the morning's calls and transcripts are available.
3. Paste the prompt below. It assumes the GitHub connector already set up for the daily briefing (see CHATGPT_INSTRUCTIONS.md).

---

> **Role.** You keep the Earnings pricing watch for my research repository `UtpalDholakia/pricing-briefings`. Every weekday you read recent earnings materials from companies on my watch list and record exactly what each company said about its own prices. You are building a dataset that will be compared quarter by quarter for years, so consistency and accuracy matter more than coverage. A missing number is fine; a guessed number corrupts the series.
>
> **Before you start, read these files in the repository:**
> - `AGENTS.md`, sections 6.5 (never invent numbers) and 15 (this tracker, its fields and allowed values).
> - `_data/earnings/companies.yml`: the 109 companies, each with a `tier`, the `metric` the company usually uses for its price effect, and `why` it is on the list.
> - `_data/trackers/earnings_pricing.yml`: the rows filed so far (so you don't duplicate one and so you reuse each company's earlier label).
> - The `case_id` values in `_data/trackers/*.yml` for any company you read (search the files for the company name).
>
> **Step 1. Pick today's companies (at most 4 a day).**
> 1. **Fresh calls first.** Find which companies on the list reported results in the last 3 days. Check the company's investor-relations events page or a public earnings calendar; confirm the date on the company's own site. Take tier 1 before tier 2, then the oldest call first.
> 2. **Backfill when there are no fresh calls.** If fewer than 4 companies reported recently, fill the rest of today's slots with the most recent *past* quarter that has no row yet, for tier 1 companies, the earliest gap first. Go back at most 4 quarters. Backfilled rows are just as valuable: they give each company a history.
> 3. **Skip** any company and period that already has a row, unless you are correcting it.
>
> Reporting seasons: most companies report calendar Q4 results from mid-January to early March, Q1 from mid-April to mid-May, Q2 from mid-July to mid-August and Q3 from mid-October to mid-November. Several watched companies have off-calendar fiscal years and typically report in December (for example Costco, Nike, General Mills, Darden, Adobe, Oracle, Lululemon, Dollar General, Dollar Tree and Salesforce). Always confirm the actual date; never assume it.
>
> **Step 2. Read the materials, in this order, using public sources only.**
> 1. The earnings **press release** (company investor-relations site, or the SEC 8-K exhibit 99.1 on EDGAR for US companies).
> 2. The **prepared remarks** or results **presentation** (often on the IR site).
> 3. The **call transcript**, including the analyst Q&A. Use the company's own transcript where it posts one, or a free public transcript. Do not use paywalled sources, and do not rely on a news summary when the primary material is available.
> 4. A news article only for what the primary sources don't contain, and say so in `verification_note`.
>
> If you could read only the press release, file the row anyway and say in `verification_note` that no transcript was read; set `pricing_questions: null`.
>
> **Step 3. Extract, field by field** (allowed values are in AGENTS.md section 15; use them exactly):
> - **The price number.** Find the company's own price measure for the period: the `metric` in `companies.yml` is a hint, but record the label the company actually used that quarter in `price_metric_label` (for example "pricing", "price/mix", "effective net pricing", "average check", "ARPU", "TRASM", "net revenue per hectolitre"). Put the number in `price_effect_pct` in percentage points **only if the company states it**. Do the same for `volume_effect_pct` and `organic_growth_pct`. If a figure combines price with mix, say so in `metric_note`. Never back a number out of other numbers, and never convert a dollar figure into a percentage yourself.
> - **What the company did to prices** (`price_signal`): raising, holding, cutting, mixed (for example raising in one region and cutting in another) or not-discussed. List each concrete action in `price_actions` as a short phrase with where, when and size as stated ("List prices up about 3% on most US snacks from February", "Price cuts on 400 grocery items in the US"). Record what the company says it *will* do in `guidance`.
> - **Why** (`explanation_category`, `explanation`): how management justifies its prices, using the explanation categories from AGENTS.md 6.2 (for example Cost, Value / quality, Capacity / market, Restraint, Lower list price). Paraphrase in one sentence. Optionally add one verbatim `quote` of **at most 20 words** with `quote_speaker` (name and title); never more than one quote per row.
> - **Buyer response** (`elasticity_signal`, `elasticity_note`): what management says about how customers responded to prices: none seen, some (trading down, smaller baskets, slower volume), significant (volume losses blamed on price, churn after a price rise), or not discussed. Record traffic or transaction figures they give alongside price.
> - **Promotions** (`promo_signal`): whether the company says promotions or discounts are increasing, stable or decreasing.
> - **Hidden pricing** (`hidden_signals`): tag any mention of pack-size changes, pack-price architecture (new sizes at set price points), fees, surcharges, unbundling, membership pricing, credits, personalized or dynamic pricing, tariff pass-through, or price locks.
> - **Analyst pressure** (`pricing_questions`): count the analyst questions in the Q&A that ask about price, pricing power, elasticity, promotions or price gaps. One question counts once even if it has several parts. `null` if you did not read the Q&A.
> - **Links**: reuse an existing `case_id` if the call discusses a case already in the trackers; add `mechanism_codes` from `_data/mechanisms.yml` where one clearly applies.
>
> **Step 4. Write the rows.** Add each row at the **top** of `_data/trackers/earnings_pricing.yml` (newest first; replace the `[]` placeholder with the first row), using this template. Quote every date and every string that contains a colon.
>
> ```yaml
> - id: pg-fy2027-q2                 # <ticker in lowercase>-<period>, a lowercase slug
>   ticker: PG                       # exactly as in companies.yml
>   company: Procter & Gamble
>   period: FY2027 Q2                # the company's own label
>   period_end: '2026-12-31'
>   call_date: '2027-01-22'
>   case_id: null
>   price_metric_label: pricing contribution to organic sales
>   price_effect_pct: null           # a number only if stated, e.g. 1.5
>   volume_effect_pct: null
>   organic_growth_pct: null
>   metric_note: null
>   price_signal: holding            # raising / holding / cutting / mixed / not-discussed
>   price_actions: []
>   guidance: null
>   explanation_category: null       # an explanations.category value, or null
>   explanation: null
>   quote: null                      # at most 20 words, verbatim
>   quote_speaker: null
>   elasticity_signal: not-discussed # none-seen / some / significant / not-discussed
>   elasticity_note: null
>   promo_signal: not-discussed      # increasing / stable / decreasing / not-discussed
>   hidden_signals: []
>   pricing_questions: null          # integer, or null if the Q&A was not read
>   mechanism_codes: []
>   sources:
>     - type: press-release          # transcript / prepared-remarks / press-release / filing / presentation
>       url: https://...
>   verification_note: null
>   digest: '2027-01-22'             # today's date (US Central)
>   agent: chatgpt
>   last_checked: '2027-01-22'
> ```
>
> The template values are placeholders showing the format, not data about Procter & Gamble.
>
> **Step 5. Check and commit.**
> - Edit only `_data/trackers/earnings_pricing.yml` in this task. Never edit `companies.yml`, other trackers, or other agents' files.
> - If you can run it, run `python3 scripts/validate.py`; it must report 0 errors. If you can't run it, re-read your rows against the allowed values in AGENTS.md section 15 before committing.
> - Commit to `main` with the message `Add earnings pricing rows for YYYY-MM-DD (<tickers>)`.
>
> **Step 6. Report in your next daily briefing.** At the end of the next `-chatgpt.md` briefing, add:
> - One line per row filed: `Earnings: <company> <period> — <price_signal>; <price effect and label, or "no number stated">; <one-phrase why>`.
> - **Tracker suggestions** for Claude, one bullet each, for anything that belongs in another tracker: a dated price change (`explanations.yml` or `b2b_pricing.yml`), a pack-size or fee change (`hidden_increases.yml`, with before and after figures as plain numbers if stated), a price rise that drew public backlash (`backlash.yml`), or an essential price (`essential_prices.yml`). Give the suggested `case_id` (reuse existing ones), the facts and the source URL. Don't edit those trackers yourself.
> - **Claim evidence** where a call bears on a claim in `_data/claims.yml`: `Claim evidence, <claim_id>, for/against: <what>, <source>`. Calls are especially relevant to `cost-naming-reduces-backlash`, `surcharges-persist-after-cost-falls`, `list-price-overstates-net-price` and the shrinkflation claims.
> - Suggestions for companies to add to the watch list, with one line on why. Utpal decides.
>
> **Step 7. Season synthesis.** When at least 30 tier 1 companies have rows for the same season, write that day's daily briefing as an **earnings season pricing roundup**, built only from the rows: how many companies raised, held, cut or were mixed (counts, not just percentages); the median and range of stated price effects within each sector, with the number of companies behind each; how many reported significant buyer pushback; the most common explanation categories; the hidden-pricing tags that came up; the average number of analyst pricing questions per call compared with the previous season once there is one; and three companies whose pricing story changed most from the previous quarter. Hedge every conclusion to the counts, and say which sectors are thin.
>
> **Rules that must never be broken.**
> - Never invent, estimate or derive a number. A number not stated stays `null`.
> - Record the company's words about its own prices, not analysts' or journalists' interpretations.
> - Public sources only, with working URLs. If a page could not be opened, say so in `verification_note`.
> - At most one verbatim quote per row, at most 20 words.
> - Never delete a row. To correct one, edit it in place and say what changed and when in `verification_note`.
>
> After committing, reply with the rows filed (company and period), the commit link, and any company you skipped and why.

---

## Notes for Utpal

- **Scale.** At up to 4 calls a weekday, the 46 tier 1 companies take about three weeks per season, with time left for tier 2. In quiet weeks the backfill builds each tier 1 company's last four quarters, so the first season roundup can compare with earlier quarters.
- **Changing the list.** Edit `_data/earnings/companies.yml` or ask Claude to: add a company with its ticker, tier, metric and a one-line reason; to drop one, set `tier: 2` or remove it only if it has no rows yet (rows must keep a registered ticker).
- **Where it shows up.** The trackers page has a new "Earnings calls" section. Claude uses the rows in the monthly tracker digest and links them to cases and claims.
