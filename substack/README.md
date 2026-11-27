# The Pricing Conundrum archive

Every published piece of [The Pricing Conundrum](https://thepricingconundrum.substack.com), one Markdown file per piece, so the agents working in this repository can read what Utpal has already written before suggesting new pieces. Rules: AGENTS.md section 16. Catalogue (themes, kind, versions): `_data/substack/published.yml`; on the site at /writing/.

- **Not published on the website.** This folder is excluded from the site build. It is readable on GitHub.
- **Front matter** on each file: `title`, `subtitle`, `date`, `slug`, `url`, `audience` (`free` / `paid`), `post_id`, `word_count`, `full_text` (false for a paid piece that so far has only the feed preview) and `imported_from` (`export` / `feed`).
- **Images** stay on Substack's servers and are linked, not copied. Embedded charts and videos appear as links; a few embedded social posts were not included in Substack's export and are marked.
- **Drafts and the subscriber list are never imported.**

## Keeping it up to date

- **Automatically:** `.github/workflows/substack.yml` runs every morning, reads the public feed and adds new pieces. Free pieces arrive in full; paid pieces arrive as the preview Substack puts in the feed (`full_text: false`).
- **Full text of paid pieces:** every few months, download a new export from Substack (Settings → Import/Export → Create new export), give it to Claude, or run `python3 scripts/substack_import.py --export <unzipped folder>`. It fills in full text and never overwrites a file with shorter text.
