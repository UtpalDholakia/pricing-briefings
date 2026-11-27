---
layout: default
title: Tracker methods
permalink: /tracker-methods/
---

# Tracker methods

These records are designed to make comparisons possible six months later. Start from public terms, research records, or an attributed account of a real transaction. Keep each source URL and, where available, a stable public archive or redacted exhibit. Leave unknowns blank. Never publish a customer identifier, account detail, private invoice, or personalized offer that reveals who received it.

## What customers actually pay {#price-panel}

Use `_data/trackers/price_panel.yml`. Keep the profile fixed: offer, market, eligibility, billing period, quantity or usage, and the scenario unit. For travel or other time-sensitive offers, also keep the relevant travel window and booking or payment conditions. Give a substantially different profile a new ID rather than rewriting history.

- **Recheck monthly** and after a meaningful change. Put the new observation under the same ID, newest first. Record unchanged prices, decreases, and offers that cannot be checked, not just increases. Update `next_check` after you log a check. It is an editorial due date, not a notification.
- **Keep the measurement basis visible.** State whether the record is posted terms, a checkout quote, a schedule calculation, a reconstructed historical schedule, a provider-reported amount, or a verified paid amount. The seed records are posted or modeled, not receipts. Leave `amount` blank when it is not defensible. Never call a component total an all-in price.
- **Separate posted price, checkout and renewal.** Record unavoidable fees and applicable taxes only if verified. In `amount`, sum the required charge for the stated scenario and period. State any exclusions in `note`. Do not net uncertain credits or rewards against the charge. For benefits lost or added, record the original units. Only state a replacement cost if it is observable.
- **Compare like with like.** Use `change: comparable` only when the previous and current observations use the same scenario, amount basis, currency, and boundary. A verified unchanged amount still gets a new row. Use `change: break` when comparison would be misleading and explain why. Use `change: baseline` for the first observation.

### The core basket {#basket}

Profiles marked `basket: core` are a fixed set of everyday offers (streaming and memberships, airline bag fees, bank and telecom prices, regulated prices such as the Ofgem cap and the Forever stamp, B2B seat prices, and Indian price points), chosen so the claims about subscription creep, fees and regulated prices can be tested on a series rather than on news. Each has a `why` line naming what it tests.

- **Every profile is checked every month**, on or after `next_check`, and gets a new observation even when nothing changed. A basket with gaps cannot show that prices did not move.
- **A failed check is recorded, not skipped.** If the page will not load, keep the profile, add a `note` saying what failed, and set `next_check` a few days out. After three failures, use a reported price with the provider page as `primary_terms`, and say so in the note.
- **Reported prices are labeled.** Use `basis: "Posted terms, as reported"` when the figure comes from coverage rather than the provider's own page.
- **Changing the basket** (adding, retiring or redefining a profile) is Utpal's decision. Retire a profile by setting `next_check: null` and a note; never delete it. AI subscriptions are not in the basket: they live in the AI pricing database (AGENTS.md section 8).

### Filling in history from archives {#backfill}

A new profile can start with a history rather than a single point. Look for earlier prices in, in order: the provider's own announcements, a dated archive copy of its price page (the Internet Archive's Wayback Machine, `web.archive.org/web/<date>/<url>`), then dated news reports of a change.

- Record each earlier price as its own observation with `basis: "Prior schedule, reconstructed"`, the date the price took effect (or the archive capture date, if that is all that is known), and the archive or report URL as `source`.
- Reconstruct only prices that were actually stated: a capture or report on a date. Never interpolate between two points or assume a price held in between.
- The earliest reconstructed observation is `change: baseline`; later ones are `comparable` only if the profile (plan, market, billing period, what is included) was the same.

## Pricing evidence and boundary conditions {#evidence}

Use `_data/trackers/pricing_evidence.yml`. Add one row per tested comparison and record the treatment, comparator, setting, design, outcome, and direction or size of the result. Cite the study or public data, not just reporting about it. Use the original study date or issue month rather than the day the briefing found it.

- Keep lab choices, stated purchase intentions, actual behavior, observational associations, and model outputs distinct. Report an effect size only with its unit and comparator. Use uncertainty intervals when the source reports them and they help interpretation.
- Record nulls, reversals, and failed replications. Link related work rather than overwriting the original result. Use `boundary` for the population, comparison, context, or other limit that matters to a pricing decision. Note whether a boundary was tested or is a practitioner hypothesis.

## Pricing model migrations {#migrations}

Use `_data/trackers/model_migrations.yml`. Create one record per change in what is charged for, what is included, or when the customer pays. Link any matching price-panel IDs. Record old and new models, new versus existing customer rules, and the first affected invoice or renewal window. Preserve published precision for dates rather than inventing a day.

- Check at announcement, effective date, and the first affected bill or renewal. Add dated updates rather than discarding old details. Move `next_check` to the next useful checkpoint.
- Use status labels that distinguish published terms, a pending transition, a provider-reported outcome, and independently verified billing outcomes. An announcement or an example invoice is not evidence that all customers paid the new amount.
- When the old and new bills can be compared, hold usage and customer eligibility fixed. Record differences from grandfathering, credits, or commitment separately.

[Back to the trackers]({{ '/trackers/' | relative_url }})
