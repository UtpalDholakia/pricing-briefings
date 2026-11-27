---
title: "Predicate AI: Pricing an AI-Native Deposition Tool at Launch"
subtitle: "A case study about a startup founder setting launch pricing for an AI tool while balancing customer value, unit economics, and conflicting investor philosophies, for use in MBA programs."
date: "2026-05-12"
slug: "predicate-ai-pricing-an-ai-native"
url: "https://thepricingconundrum.substack.com/p/predicate-ai-pricing-an-ai-native"
audience: "free"
post_id: 196961254
word_count: 4513
full_text: true
imported_from: "export"
---

![](https://substack-post-media.s3.amazonaws.com/public/images/078cf749-777c-4ec1-95f7-a48602fa26cf_1672x941.png)

#### A Founder’s Dilemma[^1]

Maya Okafor stared at the whiteboard in her office. Three columns of customer-value estimates ran down the left side, candidate pricing structures across the top, and a single date was circled twice in red in the upper-right corner. She had run out of reasons to delay her pricing decision. In ten days, at the end of March 2026, Predicate AI’s board would expect her to present a launch pricing strategy. On top of that, three of her beta-testing partner firms were waiting to hear from her about pricing going forward.

The messages from all three plaintiff firm partners had arrived over the past week or so. In their own way, each one had given Okafor a positive verdict on the product. They made it clear they liked Predicate AI and wanted to keep using it, and were ready to discuss terms. Two of these customers were managing partners at law firms Okafor had tried cases against in a previous job as a plaintiff litigator. She knew plaintiff attorneys talked to each other all the time, and word would get around quickly. Whatever price she quoted now could quickly become the price every law firm would associate with Predicate AI. She didn’t have room to experiment.

Okafor had spent the past three months working on the fundamental pricing strategy questions that every founder has to answer. What was Predicate AI worth to a plaintiff firm? What did it cost her to deliver the product to her customers? What were her competitors charging? She had some idea about the answers, but there were some inconsistencies and knowledge gaps that needed to be resolved.

There was one more complication. Every time Okafor sat down to work out the pricing strategy for Predicate AI, she found herself worrying about how her two largest investors would react, given that they held very different views about how a startup like hers should enter the market.

#### Company Background

Maya Okafor, 34, had founded Predicate AI in May 2024, after spending five years as a plaintiff-side litigator at a 22-attorney law firm in Brooklyn, working primarily on commercial fraud and product liability cases. She had been thinking about leaving for a while, but watching her firm’s senior partner spend three weekends in a row to prep for a single deposition was the straw that finally broke the camel’s back.

Deposition prep had always struck Okafor as the most peculiar aspect of litigation. It was enormously consequential, painstakingly detailed, and it was yet repetitive in ways that most attorneys did not notice consciously, even after doing the same work dozens of times. She had spent years building her own templates and checklists, and had watched colleagues do pretty much the same thing in slightly different forms. A system designed specifically for that work, she thought, could compress days’ worth of effort into hours. The existing legal AI tools she had used were general-purpose models adapted for legal tasks, and they showed it. She wanted to build something specific for deposition prep from the ground up (see Exhibit 1 for industry details).

[Embedded content: datawrapper.dwcdn.net](https://datawrapper.dwcdn.net/gis4V/1/)

Okafor built a prototype with a former Cornell classmate, raised a \$400,000 friends-and-family round, and quit her law firm in June 2024. A year later, she had closed a \$2.2 million seed round led by Northpath Ventures, with participation from Verity Capital and three angel investors. Predicate AI now had six employees: Okafor herself, two backend engineers, one ML engineer, a former paralegal who handled quality checks, and a part-time UX designer.

The firm’s fixed costs totaled about \$130,000 per month during this phase, and it also incurred significant variable costs, including AI inference costs[^2]. As of March 2026, Predicate AI had approximately \$900,000 in the bank, which amounted to about seven months of runway (excluding variable costs and additional hiring). Okafor planned to start Series A fundraising in October. Predicate AI had been in closed beta with eleven plaintiff-side firms since November 2025 (see Exhibit 2). The arrangement was that all firms could use the Predicate AI tool for free in exchange for providing detailed feedback. Now, the product was just about ready to ship.

[Embedded content: datawrapper.dwcdn.net](https://datawrapper.dwcdn.net/IdopQ/1/)

#### The Predicate AI Tool

The main product of Predicate AI was deposition preparation support. The tool took in all the information a litigation team had on a particular case. This included pleadings, documents produced during discovery, prior depositions, expert reports, medical records, and other relevant information, and produced a deposition preparation package for a specific witness in a specific legal case. The outputs generated by Predicate AI included a recommended deposition outline aligned with the legal theory of the case, anticipated witness responses with citations to source documents, impeachment material flagged by inconsistency, exhibit-by-exhibit question sequences, and a “soft spots” memo identifying where the witness was likely to be evasive.

Importantly, Predicate AI’s output was completely customized. A prep package generated for a deposition of a defendant’s chief safety officer in a product liability case would look completely different from that for an attending physician in a slip-and-fall case. The Predicate AI tool grounded every suggestion in specific document references. In beta testing, attorneys using it reported that the impeachment-flagging feature alone was finding inconsistencies their own teams had missed. It was clear to Okafor that Predicate AI provided real value to customers.

#### The Plaintiff Litigation Market

Okafor had given considerable thought to customer targeting. She had chosen small- to mid-size plaintiff firms, defined as those with three to 30 attorneys. Plaintiff firms operated primarily on a contingency basis. They took a percentage (typically 30-40%) of whatever the client won, either in settlement or at trial. They also paid most of a case’s expenses upfront, including expert witness fees, deposition costs, and filing fees, and were only reimbursed if they won the case. Their cash flow was unpredictable, they turned away far more cases than they took on, and their willingness to spend on technology was famously cautious. Furthermore, most firms of this size lacked formal procurement, IT, or firm-wide software standards. The managing partner usually made the buying decision, often basing it on an informal decision calculus. Sometimes, one phone call was all it took to make the sale.

This was different from Big Law firms, where Harvey AI, Legora, and similar tools had been making inroads for a while. Big Law firms had attorney headcounts in the hundreds or thousands, defended corporate clients using an hourly billing model, and could easily absorb \$800 or \$900 per attorney per month software bills as routine line items. The economic logic of plaintiff firms was entirely different because they had no mega-clients to pass on their software costs.

By Okafor’s estimate, there were approximately 4,200 plaintiff firms in the United States in her target size range, employing approximately 38,000 attorneys. Of these attorneys, perhaps around 60% regularly took or defended depositions. This was Predicate AI’s addressable market.

#### Customer Value

Okafor knew enough about pricing strategy to know that asking plaintiff attorneys what they would be willing to pay for the Predicate AI tool wouldn’t get her very far. A survey would only generate self-serving answers, or ones anchored to whatever they paid for Westlaw. She needed to triangulate customer value from multiple sources.

She started by working out the time savings. After getting permission from two of the firms in her beta test, she shadowed several deposition prep cycles from start to finish, including some where Predicate AI was used and others when it wasn’t. She used her phone’s stopwatch to conduct a time-and-motion study. Her meticulous tracking showed that the baseline, low-tech approach to preparing for depositions averaged 21 hours of attorney and paralegal time. Those using Predicate AI cut down their prep time to an average of 6 hours. After weighing the costs of attorneys and paralegals, she estimated a blended internal cost rate of \$290 per hour, resulting in an estimated cost savings of \$4,350 per deposition.

Her second approach was based on labor displacement, which involved asking how much it would cost to produce the same prep work without Predicate AI. The two senior partners she knew from her beta test firms helped her with this. Between the two, Okafor estimated that a junior associate, working at \$130-\$160 per hour, could produce something similar in 14-18 hours. This gave her a range of \$1,820-\$2,880, with a midpoint of \$2,350. She figured this number was conservative because junior associate time was cheaper than the partner time that Predicate AI actually displaced in practice.

Okafor’s third approach was to calculate the additional revenue generated by using Predicate AI. She did this by estimating case outcome lift, the economic value of a better-quality deposition for her customer because of Predicate AI use. She acknowledged there was greater uncertainty in this approach. A managing partner at one of her beta-test partner firms candidly told her that, of the approximately 40 depositions his firm took each year, perhaps 5 or 6 were really significant, materially affecting the outcome of the case. A meaningfully better prep on one of those depositions could increase the expected value of the case easily by 20 percent. Okafor decided to be cautious here and apply a 10% value in her calculation. Furthermore, the firm’s average case settled for \$340,000. This implied a conservative estimate of \$34,000 in value created from the consequential Predicate AI-aided deposition, at a rate of 1 in 8, leading to a revenue bump of \$4,250 and a profit increase of \$1,416 per deposition to the firm.

Okafor plotted all three numbers and carefully considered them. The first two were alternative estimates of the cost savings Predicate AI delivered to the law firm. The time-savings figure (\$4,350) was grounded in observed hours at the firm’s actual blended cost rate, making it the easiest to defend. The labor-displacement number (\$2,350) used a cheaper plausible substitute and gave her a more conservative floor, though it was vulnerable to the objection that partners, not junior associates, actually did this work. Which one made more sense and was more defensible?

The case-outcome number (\$1,416 in expected value per case to the customer) captured the revenue gain from Predicate AI’s use but had the greatest uncertainty. The expected value depended on a one-in-eight hit rate and a 20% increase in expected value, both of which were likely to vary across firms. Not only that, no managing partner could predict these things in advance, and even if the math held, no managing partner would admit in writing that his firm’s settlement values depended on a software vendor.

Finally, to round out her analysis, Okafor also conducted an informal willingness-to-pay exercise, engaging attorneys at five of the beta-test firms in pointed price conversations. Their answers clustered at \$400 and \$900 per attorney per month. She suspected the clustered responses were an artifact of the fees those firms paid for Westlaw, not a genuine willingness to pay. When she asked the same attorneys what they would pay per deposition, the range widened considerably, from \$200 to \$4,000.

#### Costs

Okafor recognized that Predicate AI’s variable cost per deposition prep was quite different from that of a traditional SaaS offering, so a pricing model couldn’t be taken straight from the SaaS shelf and used here. The biggest variable component for Okafor was AI inference costs. Predicate AI’s pipeline ran case documents through a combination of frontier-model API calls and Okafor’s own proprietary, fine-tuned models. These costs depended on case complexity. For example, a simple slip-and-fall lawsuit with 800 pages of discovery costs approximately \$35 in AI inference, while a complex product liability case with 50,000 pages of discovery and a deposition of a corporate designee could cost as much as \$220. Across the eleven beta firms, the average variable inference cost per deposition prep was just over \$74.

In addition, there was the cost of a paralegal’s review. During the beta test, a paralegal reviewed every output before delivery to customers. This added approximately \$85 per deposition prep to fully loaded labor costs. At full utilization, the paralegal could review approximately 100 deposition prep packages each month. During the beta test period, she averaged 35 reviews per month. Okafor expected the cost to decline to approximately \$30 per deposition prep as the AI output improved and met a quality threshold, allowing selective rather than full review of the product. However, she did not have a clear sense of how quickly this might happen. Okafor also had some confusion about whether to classify the paralegal cost in her pricing calculations as fixed or variable, and about the implications of that choice for her pricing decision.

There were also significant fixed costs that did not scale with each deposition but had to be recovered somehow. They included the engineering and ML staff salaries, the part-time UX designer’s salary, infrastructure, security, and compliance (legal data carried significant regulatory burdens), marketing and customer success expenses, and rent. These expenses added to approximately \$130,000 per month. The paralegal’s cost would need to be added to this, but only if it were treated as a fixed cost.

Two cost items deserved closer attention. The first was Okafor’s own compensation. She was currently drawing \$60,000 per year, well below market for a venture-backed founder-CEO with her experience. She expected investors to push her to a more standard salary range of \$200,000-\$250,000 by the Series A close. That implied \$12,000 to \$16,000 per month in additional fixed costs that pricing would eventually have to recover, even if it didn’t apply at the moment.

The second issue was the paralegal’s capacity. While the beta test was running, there was considerable slack. But as Predicate AI scaled up, she would need to hire additional reviewers, at a fully loaded cost of \$8,500 per month per reviewer. Both items meant that the \$130,000 figure understated steady-state fixed costs, and even a modest paying customer base would need to absorb significant overhead growth, not just current overhead.

If she modeled an aggressive year-end scenario, with 50 firms each running 5 deposition preps per month, and a variable cost of \$159 per deposition prep, the variable cost alone would run approximately \$40,000 per month. Whether that was a good thing or not depended entirely on the price she was about to set.

Pulling these numbers together gave Okafor a rough picture of her unit economics. At the current \$159 variable cost per deposition prep, a per-prep price of \$500 implied a gross margin of about 68 percent, \$1,000, about 84 percent, and \$1,500, about 89 percent. If the paralegal cost dropped to \$30 in the near future as Okafor expected, these margins would rise further. But if she went with per-seat pricing, the results would be different. At \$400 per attorney per month, a 10-attorney firm running 5 preps per month would generate \$4,000 in monthly revenue against \$795 in variable costs, resulting in an 80 percent gross margin. But if the same firm ran 20 preps per month, variable costs rose to \$3,180, and gross margin was squeezed to approximately 20 percent.

#### Competitor Pricing

When Okafor started researching her competitors, she found that getting reliable pricing data on legal AI tools was far harder than she had expected. No one in the industry published price lists. Vendors negotiated with each customer, RFP responses were kept confidential, and, where they existed, pricing web pages simply said, “Contact us for pricing.”

She gathered what she could through a combination of idiosyncratic and creative methods. Okafor joined a closed Slack community for legal operations professionals and listened to their conversations. She offered a 30% discount to one firm in her beta test for future pricing in exchange for a copy of a competing pricing proposal the firm had received recently. She had coffee with a former colleague who had moved to a legal-tech consultancy. She read every funding announcement and LinkedIn headcount analysis she could find. The disclosed customer counts and the ratio of sales to engineering staff from these sources let her work out competitors’ pricing within a rough range, even when no actual price was published. The picture that emerged was fragmented, and she was not confident in much of it.

After all this competitive intelligence work, Okafor concluded that Predicate AI’s most important competitor was the status quo, namely a senior attorney’s Sunday afternoon, plus a junior associate’s Tuesday and Wednesday. The status quo had advantages that no amount of positive ROI from Predicate AI’s use could fully overcome, because staying low tech required no cash outlay, no purchasing process, no software to learn, and no trust in a new vendor. In contrast, Predicate AI could deliver clear economic value relative to the labor it replaced (and pushed to other, presumably more productive uses), but converting that superior economic value into adoption remained a significant challenge. Senior attorneys had prepared for depositions the same way for years, and the prep was high-stakes enough that overhauling the process carried real professional risk.

Okafor had also briefly considered an outcome-based pricing model with which Predicate AI would charge its customers a percentage of case recoveries. It seemed like a lucrative model that could be easily explained as a “risk-sharing” approach to customers. However, state bar ethics rules in most jurisdictions prohibited fee-splitting between attorneys and non-lawyers, and more than one plaintiff partner she respected had recoiled even at the mention of this idea. After a 20-minute call with an ethics-focused law professor, Okafor ruled out outcome-based pricing.

#### Two Opposing Investor Perspectives

Okafor’s board had three members: Maya Okafor herself, and her two major investors, Daniel Reyes from Northpath, and Linda Park from Verity. The angels did not have board seats. Daniel had led Northpath’s investment and was Okafor’s lead board member. He had backed seven vertical SaaS companies in his career, three of them in the legal-tech space. One of those three, a contract-review tool he had championed, had launched at \$50,000 per year per firm in 2021 and had never gotten past nine customers before running out of money. The post-mortem from this debacle had stayed with him. The founders had insisted on premium pricing to signal value, and the sales cycle had stretched beyond 9 months per deal. By the time they were ready to lower the price, they had no time or momentum left. They ran out of runway and had to abandon ship. “Get to fifty paying firms by year-end as if your life depended on it,” Daniel had advised Okafor, citing this experience, “I would rather see you at \$300 per month with two hundred firms than \$40,000 per year with fifteen. Get the volume first.” He was not opposed to raising prices later, but was strongly against entering the market at a price that required a long, consultative sales process to close.

Linda was as battle-hardened as Daniel, but her experiences had led her to a very different conclusion regarding launch pricing. Her firm, Verity, had backed an AI-native marketing tool in 2023 that launched at \$99 per month, scaled to 1,800 customers, and then found out that (1) the gross margins were awful at this price level because of burgeoning AI inference costs, and (2) existing customers refused to take any meaningful price increases. These issues had been so severe that the startup shut down in 2025 after failing to raise a Series B. Linda’s reading was that the founders had anchored themselves to a “too-low” price that had sunk them. Her view was that in AI-native businesses, the significant variable cost per use made low launch pricing structurally dangerous. SaaS and AI were fundamentally different in this sense. “If they associate Predicate AI with a number,” she had counseled Okafor, “make sure it is a number you can live with for at least three years.”

Both views were genuine and came from experienced, battle-scarred venture capitalists. An even bigger challenge was that either one could be right, depending on what Predicate AI turned out to be. However, Okafor didn’t think she could split the difference. The two pricing visions implied entirely different, mutually exclusive sales strategies, target customer profiles, and monetization strategies.

#### Price Level and Price Structure

As Okafor laid out her thinking on a whiteboard, she realized she had been conflating two questions that needed to be answered separately: the price level and the price structure.

The first was a question of how much money Predicate AI should earn from a law firm each year. At the low end, \$400 per attorney per month for a 10-attorney firm came to \$48,000 per year. At the high end, a per-deposition prep price of \$1,500 with 40 depositions per year came to \$60,000. Two annual per-customer revenue numbers that were reached via entirely different pathways, with entirely different implications for selling, forecasting, and customer behavior.

The second was about how the payment should be structured. There were several reasonable pricing structure alternatives. A per-seat price structure charged each attorney at the firm a monthly subscription fee, regardless of usage. This was the structure plaintiff attorneys were used to from Westlaw and Lexis. For Predicate AI, this structure made it easy to forecast revenue. However, it decoupled the price from its value to the attorney. An attorney who took two depositions per year paid the same amount as one who took twenty, and that didn’t seem fair.

A per-deposition prep price structure charged the firm a fee each time it used Predicate AI to prepare for a deposition. This aligned tightly with both Predicate AI’s variable cost and the value delivered. But plaintiff firms (like most firms everywhere) hated unpredictable costs, and managing partners did not want to think about software pricing every time a new case opened. The fear of being nickel-and-dimed was real, even if you were a hard-charging lawyer.

A hybrid two-part pricing structure combined a low per-seat base (covering access, training, and platform availability) with a per-deposition prep usage fee. This captured some of the predictability of the first approach and the value alignment of the second approach, at the cost of being more complex to explain to customers.

Another possibility that favored simplicity was a flat firm-wide subscription price structure that charged a single annual price regardless of usage or seat count. This was administratively simple but exposed Predicate AI to firms running up enormous usage on a fixed price. It was the simplest of the price structures, but it had some serious weaknesses.

Okafor also needed to answer several structural questions about her pricing. First, should the contracts be annual or monthly (or should both options be offered)? Annual contracts would smooth Predicate AI’s revenue and impress Series A investors, but were harder to close at launch or soon thereafter. Monthly contracts would be far easier and align with launch pricing, but would quickly raise concerns about managing churn rates. Second, should there be a founding-customer pricing tier? For example, should the first ten or fifteen firms that signed on get a permanently locked-in “low” price (whatever that might be) as a reward for early adoption, or should pricing reset for everyone at some point? How often should that be?

Third, should Predicate AI publish prices publicly, say on their website, or quote each firm individually? There were pros and cons associated with price transparency. Fourth, what would be the best initial pricing approach at the time of launch? Some options on the table were a free trial for a set duration (7-30 days or capped at 1 deposition prep), a paid pilot, or a freemium tier. Each initial pricing approach had different things going for it. In a recent conversation, Daniel had favored a 30-day free trial, while Linda leaned toward paid pilots starting at \$7,500. Okafor’s instinct was to land somewhere in between, but she was not yet sure where.

What Okafor had begun to appreciate, as she stared at the whiteboard, was that the two questions of price level and price structure were not independent. A high price was easier to defend with a per-deposition prep structure, where each charge mapped to a visible deliverable. A low price was easier to deploy with a per-seat structure, where the small per-attorney price went unnoticed in a firm’s monthly software spend and would be an easy sell. Giving weight to one constrained the other.

#### The Decision

It was ten days to D-day. Maya Okafor had five questions to answer by then.

1.  **Price level.** What price should Predicate AI launch at, and what was the strategic case for the level she chose?

2.  **Price structure.** Per seat, per deposition prep, hybrid, or flat firm-wide subscription?

3.  **Launch staging.** What was the best way to stage the public launch, with a free trial, paid pilot, founding-customer pricing, or some combination thereof?

4.  **Investor alignment.** How should she navigate the core disagreement between Daniel and Linda, when she needed the support of both at least through Series A, if not longer?

5.  **Reducing uncertainty.** Was there anything she could do, in the ten days she had left, to tighten any of the inputs to her pricing decision before she had to commit?

Comprehensive teaching note for the case is available here:

[^1]: Professor Utpal Dholakia prepared this case solely for discussion to support the learning and application of pricing strategy concepts by entrepreneurs. It is not meant to serve as an endorsement, an advertisement, a source of primary data, or an illustration of effective or ineffective management, and has been written entirely using information available from public sources. Although based on a realistic context and business parameters, the case is fictitious, and any resemblance to actual persons, brands, or organizations is coincidental. Copyright ©Utpal Dholakia, 2026. This document may not be shared, posted, or transmitted without the permission of Professor Dholakia.
[^2]: AI inference costs are the fees charged by AI model providers (such as OpenAI or Anthropic) for each query run against their models. For Predicate AI, every deposition prep processed generated such fees.
