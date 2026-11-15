# Instructions to paste into ChatGPT

## Step 1: Connect GitHub in ChatGPT (one time)

1. In ChatGPT, open **Settings → Apps & Connectors** (on some plans this is **Connectors**).
2. Connect **GitHub**. When GitHub asks which repositories to allow, choose **Only select repositories → `pricing-briefings`**.
3. Make sure write access is turned on for the GitHub connector.

## Step 2: Update your scheduled briefing task

Open **Scheduled** in the ChatGPT sidebar, edit your existing pricing-briefing task (or create a new one), and paste in the following. Replace `<OWNER>` with your GitHub username.

---

> Every day, research and write a pricing strategy briefing, then publish it to my GitHub repository `<OWNER>/pricing-briefings` using the GitHub connector.
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
>   tags: [tag1, tag2, tag3]
>   ---
>   ```
> - Body sections, in order: `## Key takeaways`, `## What happened`, `## Why it matters`, `## Ideas to apply`, `## Sources`. Every factual claim needs a source with a working URL. Aim for 400–900 words.
> - Commit directly to `main` with the message `Add chatgpt briefing for YYYY-MM-DD`.
> - Change no other files. Never edit or delete files written by other agents (for example `*-claude.md`).
> - If a file for today already exists from you, update it rather than creating a duplicate.
>
> Focus: pricing psychology and pricing strategy. That means behavioral pricing (anchoring, decoys, framing, charm pricing), SaaS and subscription pricing, dynamic pricing, and notable price changes by companies.
>
> After committing, reply with the file path and the page URL:
> `https://<OWNER>.github.io/pricing-briefings/briefings/YYYY-MM-DD-chatgpt/`

---

## If ChatGPT says it can't write to GitHub

Some plans or connector versions only allow reading. If so:

- **Option A:** Use **Codex** (in ChatGPT), which can commit to GitHub, with the same instructions.
- **Option B:** Let ChatGPT open a **pull request** instead of committing to `main`, and merge it with one click on GitHub. This also gives you a chance to review each briefing before it goes live.
- **Option C (last resort):** Have ChatGPT email you the Markdown file, and ask Claude to post it.

## Moving old briefings

To bring briefings over from the old ChatGPT site, ask ChatGPT:

> "Re-post each briefing from the Pricing Psychology briefing site to `<OWNER>/pricing-briefings`, one file per briefing, named `_briefings/<original-date>-chatgpt.md` and following AGENTS.md."
