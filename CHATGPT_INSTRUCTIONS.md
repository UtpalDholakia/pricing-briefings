# Instructions to paste into ChatGPT

## Step 1: Connect GitHub in ChatGPT (one time)

1. In ChatGPT, open **Settings → Apps & Connectors** (on some plans this is **Connectors**).
2. Connect **GitHub**. When GitHub asks which repositories to allow, choose **Only select repositories → `pricing-briefings`**.
3. Make sure write access is turned on for the GitHub connector.

## Step 2: Update your scheduled briefing task

Open **Scheduled** in the ChatGPT sidebar, edit your existing pricing-briefing task (or create a new one), and paste in the following. It is already filled in with your GitHub username.

---

> Every day, research and write a pricing strategy briefing, then publish it to my GitHub repository `UtpalDholakia/pricing-briefings` using the GitHub connector.
>
> Before writing, read `AGENTS.md` in that repository and follow it exactly. In short:
>
> - Create ONE new file: `_briefings/YYYY-MM-DD-chatgpt.md` (today's date, US Central time).
> - Start the file with this front matter:
>   ```
>   ---
>   title: "<specific headline>"
>   agent: chatgpt
>   date: YYYY-MM-DD
>   summary: "<1–2 sentence takeaway>"
>   tags: ["Pricing Psychology", "<tag>", "<tag>"]
>   ---
>   ```
> - Tags: pick 3–15 tags ONLY from `_data/tags.yml` in the repository (my Pricing Conundrum Substack tag list), spelled exactly as written, each in double quotes. Never invent new tags.
> - Body sections, in order: `## Key takeaways`, `## What happened`, `## Why it matters`, `## Ideas to apply`, `## Sources`. Every factual claim needs a source with a working URL. Aim for 400–900 words.
> - Commit directly to `main` with the message `Add chatgpt briefing for YYYY-MM-DD`.
> - Change no other files. Never edit or delete files written by other agents (for example `*-claude.md`).
> - If a file for today already exists from you, update it rather than creating a duplicate.
>
> Focus: pricing psychology and pricing strategy. That means behavioral pricing (anchoring, decoys, framing, charm pricing), SaaS and subscription pricing, dynamic pricing, and notable price changes by companies.
>
> After committing, reply with the file path and the page URL:
> `https://utpaldholakia.github.io/pricing-briefings/briefings/YYYY-MM-DD-chatgpt/`

---

## Research additions (AI pricing database, deep dives, pipeline)

Add this to ChatGPT's task: "When your briefing finds an AI price, allowance, tier or credit change, end it with a short 'Database suggestions' list: provider, product or model, `change_type` (from AGENTS.md section 8), old → new value as the source states it, source URL, and the matching `case_id`. Don't edit `_data/ai_pricing/`, `_cases/` or `_data/substack/`; Claude verifies and adds your suggestions. If you notice evidence a draft deep dive in `_cases/` is missing, or an essay-sized idea for the Substack pipeline, mention it in the same list." ChatGPT keeps maintaining its own trackers (`price_panel.yml`, `pricing_evidence.yml`, `model_migrations.yml`); Claude's morning run also checks any `next_check` date that has arrived. New `pricing_evidence.yml` rows should carry `mechanism_codes` from `_data/mechanisms.yml`, and every commit to `_data/` should pass `python3 scripts/validate.py` (AGENTS.md section 11). When a study you add bears on a claim in `_data/claims.yml`, name it in the briefing as "Claim evidence, `<claim_id>`, for/against: …"; Claude files the pointer (AGENTS.md section 12).

## The Pricing Conundrum archive (AGENTS.md section 16)

Add this to the daily task: "Utpal's published pieces are in `substack/posts/` (one Markdown file each) with a catalogue in `_data/substack/published.yml` (themes, dates, URLs). Before suggesting a Substack idea, a deep dive or a hypothesis, check the catalogue and read the related pieces. For every suggestion, say whether it *builds on* a piece (cite it and say what is new), *revisits* one (say what has changed), *answers a question one left open*, or is *new ground* (say which themes you checked). When a news item fits one of Utpal's frameworks (for example the Value Pricing Framework, the SALVE framework of price image, price level versus price structure, the four pricing decision inputs), name it and link the piece. If today's news challenges something he has argued, add a line: 'Challenges <piece title> (<URL>): …'. Link to pieces rather than quoting paid text."

## Hypothesis hunt (AGENTS.md section 13)

Add this to ChatGPT's task: "Before researching, read `_data/hypotheses.yml`. Pick up to 2 hypotheses with `status: Testing` that fit today's theme, preferring the one hunted longest ago (`last_hunted: null` first). Skip any hypothesis that any agent hunted yesterday, and any whose last hunt was a miss less than 14 days ago. Run searches aimed at each hypothesis's `predicts` and `test`, not only at today's theme. At the end of the briefing, add one line per hypothesis you hunted, including misses: `Hypothesis hunt: <hypothesis_id> — hit: <what you found, with its source>` or `Hypothesis hunt: <hypothesis_id> — miss: <what you searched>; next hunt after <date 14 days on>`. A hit must be directly on point (a study or a case that is itself an instance), not a related anecdote. To propose a new hypothesis, add `Hypothesis proposal: <one sentence> — predicts: <observable result> — test: <how it would be checked> — lanes: <lanes>`; a proposal without a test is a question. Don't edit `hypotheses.yml` or `claims.yml`; Claude logs your hunts and files the evidence."

## Earnings pricing watch (AGENTS.md section 15)

A second scheduled task for ChatGPT reads earnings calls for pricing. Setup and the full prompt: [EARNINGS_INSTRUCTIONS.md](EARNINGS_INSTRUCTIONS.md).

## If ChatGPT says it can't write to GitHub

Some plans or connector versions only allow reading. If so:

- **Option A:** Use **Codex** (in ChatGPT), which can commit to GitHub, with the same instructions.
- **Option B:** Let ChatGPT open a **pull request** instead of committing to `main`, and merge it with one click on GitHub. This also gives you a chance to review each briefing before it goes live.
- **Option C (last resort):** Have ChatGPT email you the Markdown file, and ask Claude to post it.

## Moving old briefings

To bring briefings over from the old ChatGPT site, ask ChatGPT:

> "Re-post each briefing from the Pricing Psychology briefing site to `UtpalDholakia/pricing-briefings`, one file per briefing, named `_briefings/<original-date>-chatgpt.md` and following AGENTS.md."
