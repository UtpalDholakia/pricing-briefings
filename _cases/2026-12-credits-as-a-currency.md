---
title: "Credits are a currency, and vendors control the exchange rate"
date: 2026-11-15
author: claude
status: draft
question: "When does partitioning (tokens, line items) signal fairness rather than obfuscation?"
case_ids: [chatgpt-pro-allowance-2026, openai-per-job-pricing-2026, saas-credits-2026]
tracker_refs: [ai_product_pricing, hidden_increases, explanations, backlash, questions]
tags: ["Pricing Psychology", "consumer psychology", "Pricing AI products", "Credit-based pricing", "Token pricing", "Hidden Price Increases", "Usage-based pricing", "Price transparency", "SaaS pricing"]
---
_Draft for Utpal's review, written 15 November 2026. Planned publication: December 2026. Every number below comes from a source linked in the text and logged in the trackers or the AI pricing database. The ChatGPT Pro figures come from news coverage and will be checked against OpenAI's own pricing page at the database's first snapshot on 1 December 2026._

## The claim

AI products are increasingly sold in units the vendor defines: credits, message allowances, and multiples of another plan's usage. These units do something a dollar price cannot. They let the vendor change what the buyer gets without changing the number on the price tag. **When a vendor controls both the price of a unit and what the unit buys, the unit works like a private currency, and buyers need a published, stable exchange rate far more than they need a simpler price.** Partitioning signals fairness when the unit can be audited against the work it buys. It obscures when the conversion rate can move quietly.

## The evidence

**1. An allowance cut is a price rise that leaves the price unchanged.** OpenAI's $200-a-month ChatGPT Pro plan went from 20 times the Plus plan's usage to 10 times on 30 October 2026, at the same monthly price ([PCWorld](https://pcworld.com/article/3249113/chatgpt-pros-biggest-perk-just-got-cut-in-half-meet-the-new-ai-subscription-math.html); logged in `price_changes.yml` and `hidden_increases.yml` as case `chatgpt-pro-allowance-2026`). Per unit of usage, that roughly doubles the price. Two features of the change matter for buyer psychology:

- **The unit is defined by reference to another product.** "10x Plus" is only meaningful if the buyer knows what Plus allows, and that can change too. A buyer can't check the new price against the old one without knowing two allowances, either of which can change separately.
- **The change came with a reframing.** OpenAI argued that more efficient models mean users still get more done than before, and it softened the cut with one-time credits ([The New Stack](https://thenewstack.io/openai-halves-200-plan/); `explanations.yml`, category *Efficiency*). The backlash tracker records the outcome as *Partial*: the cut stood, mitigated by credits.

At the same time a new $500 tier appeared at about 25x Plus usage (`price_changes.yml`, *new-tier*). A new top tier recasts the old middle option, and the decoy literature predicts that this makes $200 look more reasonable even as it buys less.

**2. Credits move the price into a conversion rate.** In B2B software, Deepak Gupta argues that seat pricing breaks down once AI agents do the work. He warns that credit systems let vendors change exchange rates quietly and let unused balances expire ([Security Boulevard](https://securityboulevard.com/2026/10/how-to-buy-software-when-ai-breaks-pricing/); `ai_product_pricing.yml`, case `saas-credits-2026`). The PricingSaaS weekly tracker logged credit-based pricing in 22% of the pricing changes it recorded in late October ([PricingSaaS](https://pricingsaas.com/); briefing of 4 November). The author runs a vendor and the tracker's sample is self-selected, so treat both as signs of direction rather than measurements. Still, the direction is clear: enterprise software is rebuilding the token economy of mobile games, with three familiar features. Spending is decoupled from money, unused balances expire (breakage), and the exchange rate is opaque.

**3. Regulators already treat this as a pricing problem in games.** The EU's consumer-protection network opened coordinated action against nine game companies over prices shown mainly in in-game currency, currency bundles that don't match item prices, and hidden exchange rates ([Lewis Silkin](https://www.lewissilkin.com/insights/2026/10/15/eu-consumer-protection-network-launches-action-involving-nine-video-games-compani-102o5do); `stories.yml`, `eu-cpc-virtual-currencies-2026`). The Commission's Digital Fairness Act proposal of 11 November would require a real-money equivalent wherever items are sold for virtual currency ([Freshfields](https://www.freshfields.com/en/our-thinking/briefings/2026/11/digital-fairness-act-the-eus-new-consumer-protection-rulebook-takes-shape); `laws.yml`, European Union). Neither measure covers AI credits or business buyers. Yet the problem they target is the same: a unit whose money value the seller sets and can change.

**4. Buyers say what they want, and it is auditability.** When OpenAI tested a single per-job price in place of per-token metering, customers objected. They wanted to see what they were paying for, even though Sam Altman calls tokens a "fake unit," and OpenAI kept token pricing ([The New Stack](https://thenewstack.io/openai-token-pricing-reversal); `price_changes.yml`, *mechanism-change*; backlash tracker *Yes*). This is the most informative case in the set. Buyers turned down a simpler, bundled price in favor of a more granular unit, the opposite of what the usual flat-rate bias and pain-of-paying arguments predict. The token won because it is *countable against output*: a buyer can measure how many tokens a job took and compare that across vendors and over time. The per-job price lacked that, so it read as a black box.

Taken together, the cases suggest that partitioning by itself is neither fair nor unfair. The unit has to be auditable, so that a buyer can measure it against the work done, and stable, so that the vendor can't change what it buys without notice. A token passes the first test. "10x Plus" fails both. Credits pass or fail depending on whether the exchange rate is published and fixed.

## The counter-evidence

**The efficiency argument may be right.** If newer models finish a task in fewer messages or tokens, a 10x allowance may buy as much *work* as 20x did. The price per unit of output need not have doubled, even though the price per unit of allowance did. That would make the ChatGPT Pro change closer to repackaging than a hidden price increase. The trackers hold no measurement of output per unit, so this can't yet be ruled out.

**Tokens are also vendor-defined.** Altman's own point is that a token is an arbitrary unit. Tokenizers differ across providers and model versions, so "price per million tokens" can change in substance when a vendor ships a new tokenizer. If buyers trust tokens anyway, perhaps familiarity, not auditability, explains the per-job reversal.

**Market discipline may be enough.** Card data on 174 million US consumers show that buyers of generative-AI subscriptions are highly price-sensitive. Annual retention is 20 to 45%, and switching jumps around model releases ([Egan, Russel, Shi & Yao, NBER WP 35953](https://www.nber.org/papers/w35953); `ai_product_pricing.yml`). If buyers churn readily, a vendor that quietly devalues its credits will lose customers, and no exchange-rate rule is needed.

**Business buyers are not gamers.** The token-currency evidence comes mostly from consumer games, where spenders are often young and impulsive. Enterprise buyers have procurement teams, contracts and usage dashboards. The same opacity may not change their spending at all.

## What would change my mind

- **Stable published exchange rates with no change in behavior.** Suppose the providers in the AI pricing database publish fixed credit-to-output conversion rates with advance notice of changes. If churn and spending then look the same as under opaque credits, the claim that the exchange rate is what matters would be weakened.
- **Evidence that output per allowance unit rose enough to offset the cut.** For example, a benchmark showing that a typical Pro task needs about half the messages it needed before 30 October. That would recast the ChatGPT Pro change as repackaging rather than a price rise.

## What to watch next

- **1 December 2026:** the AI pricing database's first verified snapshot. It will confirm the ChatGPT Pro figures on OpenAI's own page and add verified subscription tiers from at least two other providers.
- **EU Digital Fairness Act:** whether the Parliament and Council keep the real-money rule for virtual currencies, and whether anyone proposes extending it to credits sold to businesses (`stories.yml`, `eu-digital-fairness-act-2026`).
- **EU CPC game-currency action:** whether the nine companies commit to showing real-money prices (`eu-cpc-virtual-currencies-2026`).
- **`price_changes.yml`:** any *credit-repricing* or *allowance-cut* entry. Each one tests whether buyers notice a change made through the exchange rate.

## Review notes

_For Meta AI and ChatGPT: add counter-cases here, especially non-Western credit or token pricing (e.g. prepaid mobile data, in-app currencies outside the EU) and any consumer-voice evidence on how buyers reacted to the ChatGPT Pro change. Please don't edit the sections above._

## Sources

- [ChatGPT Pro's biggest perk just got cut in half](https://pcworld.com/article/3249113/chatgpt-pros-biggest-perk-just-got-cut-in-half-meet-the-new-ai-subscription-math.html), PCWorld, 2 Oct 2026
- [OpenAI halves its $200 plan](https://thenewstack.io/openai-halves-200-plan/), The New Stack, Oct 2026
- [OpenAI's token pricing reversal](https://thenewstack.io/openai-token-pricing-reversal), The New Stack, Oct–Nov 2026
- [How to buy software when AI breaks pricing](https://securityboulevard.com/2026/10/how-to-buy-software-when-ai-breaks-pricing/), Deepak Gupta, Security Boulevard, 17 Oct 2026
- [PricingSaaS Pulse](https://pricingsaas.com/), PricingSaaS, Week 44 (19–25 Oct 2026)
- [EU consumer protection network launches action involving nine video games companies](https://www.lewissilkin.com/insights/2026/10/15/eu-consumer-protection-network-launches-action-involving-nine-video-games-compani-102o5do), Lewis Silkin, 15 Oct 2026
- [Digital Fairness Act: the EU's new consumer protection rulebook takes shape](https://www.freshfields.com/en/our-thinking/briefings/2026/11/digital-fairness-act-the-eus-new-consumer-protection-rulebook-takes-shape), Freshfields, 11 Nov 2026
- [Egan, Russel, Shi & Yao, NBER Working Paper 35953](https://www.nber.org/papers/w35953), NBER, Oct 2026
