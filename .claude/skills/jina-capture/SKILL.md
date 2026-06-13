---
name: jina-capture
description: Fetch a web page as clean markdown via r.jina.ai and save it directly into wiki/raw/ as a new capture. Use whenever the user gives a URL and wants it added to their second brain, or says things like "capture this", "save this article", "add this link to raw", or pastes a URL in the context of the wiki.
---

# Jina Capture

Turn any URL into a stamped markdown file in `wiki/raw/` using the Jina Reader service (`https://r.jina.ai/<url>`), which returns a clean markdown version of the page.

## When to use

- User provides a URL and wants it captured into the second brain.
- User says "save this", "capture this", "add to raw", "read this later", etc., alongside a link.
- Bulk import of a list of URLs.

## How it works

`https://r.jina.ai/<full-url>` returns the target page rendered as markdown. No API key is required for basic use. Just fetch it and save the body.

## Steps

1. **Confirm target folder.** Default is `wiki/raw/` in the current project (the second brain repo). If the user is not in that repo, ask where to save.

2. **Fetch the markdown.** For each URL:
   - Construct `https://r.jina.ai/<url>` (do not URL-encode the target — Jina expects the raw URL appended).
   - Use the WebFetch tool to retrieve it. Ask for the full markdown body.
   - If WebFetch summarizes instead of returning raw content, fall back to:
     ```bash
     curl -sL "https://r.jina.ai/<url>" -o /tmp/jina.md
     ```
     and read `/tmp/jina.md`.

3. **Extract a title and slug.** Jina's output usually starts with `Title: ...` and `URL Source: ...` lines followed by `Markdown Content:`. Parse the title from there; slugify it to max 50 chars, lowercase, hyphen-separated.

4. **Write the file.** Save to `wiki/raw/<YYYY-MM-DD>-<slug>.md` with frontmatter prepended:
   ```yaml
   ---
   id: <YYYY-MM-DD>-<slug>
   date: <YYYY-MM-DD>
   source: <original url>
   tags: []
   status: draft
   ---
   ```
   Followed by the markdown body Jina returned. Keep the body intact — do NOT summarize or edit it. The point of raw/ is fidelity.

5. **Report back.** Print the new file path (as a `computer://` link) and a one-line summary of what the article is about. Do not run `/ingest` automatically — the user decides when to distill.

## Rules

- Never overwrite an existing file in `wiki/raw/`. If the slug collides, append `-2`, `-3`, etc.
- Never modify or delete other files in `wiki/raw/`.
- If Jina returns an error page or empty body, tell the user and do not create the file.
- For multiple URLs, process them in sequence and print one summary line per saved file at the end.

## Example

User: "save this https://example.com/article-about-llms"

Claude:
1. WebFetch `https://r.jina.ai/https://example.com/article-about-llms`
2. Parses title "Article About LLMs" → slug `article-about-llms`
3. Writes `wiki/raw/2026-04-09-article-about-llms.md` with frontmatter + body
4. Replies with the file link and a one-sentence description.
