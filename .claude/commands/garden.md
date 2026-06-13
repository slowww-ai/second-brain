---
description: Weekly cleanup — find orphans, duplicates, broken links, stale drafts
---

Your job is to keep `wiki/notes/` healthy. Do NOT make destructive changes without user approval.

Steps:

1. **Orphans** — notes with no incoming backlinks. Use `scripts/search.py --backlinks <note>` for a sample; or scan directly.
2. **Near-duplicates** — notes covering the same concept. Search for overlapping titles and key terms.
3. **Broken links** — `[[wikilinks]]` pointing to files that don't exist in `wiki/notes/`.
4. **Stale drafts** — notes with `status: draft` older than 30 days.
5. **Tag inconsistencies** — similar tags like `llm-eval` vs `llm-evals`.

For each issue found, propose a specific fix (merge A into B, rename tag X to Y, promote draft Z to stable, etc.). Present the list to the user and wait for approval before editing. After approvals, apply the fixes, then print a short summary.
