---
description: Gather relevant notes on a topic and produce a written brief
argument-hint: <topic> [--format md|docx|pdf]
---

Topic: $ARGUMENTS

Your job is to produce a brief on the given topic using only information from `wiki/notes/` (and `wiki/raw/` for citations when needed).

Steps:

1. Run `python scripts/search.py "<topic keywords>"` with several query variations to find relevant notes.
2. Also try `python scripts/search.py --tag <likely-tag>` if a tag seems obvious.
3. Read the top ~10 hits in full. Follow `[[wikilinks]]` one hop when useful.
4. Before writing, first ask the user (using AskUserQuestion) to confirm:
   - the intended audience and tone
   - desired length (one-pager, deep dive, etc.)
   - output format (markdown, docx, pdf) — default markdown
   unless these are already clear from the arguments.
5. Draft the brief in `wiki/outputs/<date>-<slug>.md` with sections: TL;DR, Key points, Details, Open questions, Sources.
6. In "Sources", list the note IDs you used as a bulleted list.
7. If the user asked for `.docx` or `.pdf`, use the appropriate skill to render the final file alongside the markdown.
8. Share the output file with a `computer://` link and a one-sentence summary. Do not restate the whole brief in chat.
