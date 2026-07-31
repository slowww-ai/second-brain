---
description: Process new files in wiki/raw/ into distilled notes in wiki/notes/
---

Your job is to turn new raw captures into clean, linked wiki notes.

Steps:

1. Run `python scripts/ingest.py list-new` to find raw files not yet referenced by any note. Also list any images or PDFs in `wiki/raw/` that don't yet have a companion `.md` file — those need to be processed too.
2. **Non-text captures first.** For every image or PDF in `raw/` without a companion `.md`:
   - Read the file directly (Claude can see images and PDFs natively).
   - Create `raw/<same-name>.md` with frontmatter, a description, a full transcription of any visible text/tables, and an `image:` or `pdf:` reference line.
   - Do NOT modify or delete the original binary file.
   - Treat the new companion `.md` as a raw capture and continue with the normal flow below.
3. For each new raw markdown file (including companions just created):
   a. **Read it according to its length.** First check line count (`wc -l <path>` or the file header from Read). Then:
      - **Under 500 lines** — read the entire file in one pass. No shortcuts.
      - **500–2000 lines** — read the entire file, in sequential chunks if needed. Distill aggressively into short notes, but do not skip sections.
      - **Over 2000 lines** — read the first ~200 lines to get structure and thesis, scan the table of contents / headers, then read in full the sections most relevant for distillation and linking. It's fine to skip appendices, repetitive examples, or sections clearly tangential to the core concepts.
      - **Always report read-coverage** in your final summary as `read X/Y lines of <file>` so shallow reads are never silent. If coverage is under 100%, note which sections you skipped and why, so the user can request a follow-up deep pass.
   b. Run `python scripts/ingest.py stamp <path>` if it has no frontmatter yet.
   c. Identify the 1–3 core concepts in the file.
   d. For each concept, decide: does a matching note already exist in `wiki/notes/`? Use `python scripts/search.py "<concept>"` to check.
   e. If yes → append a distilled paragraph to that note and cite the raw file (`see raw/<filename>`).
   f. If no → create a new note in `wiki/notes/<slug>.md` with proper frontmatter, a short summary, and `[[wikilinks]]` to any related existing notes. If the source was an image or PDF, embed it inline with `![](../raw/<name>.png)`.
4. Add backlinks: if note A now references note B, make sure B has an entry pointing back to A when it's meaningful.
5. Never modify or delete original files in `wiki/raw/` (companion `.md` files you just created are fine to edit).
6. **Record each processed raw file in the ledger.** After you finish distilling a raw file, run:
   ```
   python scripts/ingest.py record <raw-filename> <note1,note2,...>
   ```
   where the second argument is a comma-separated list of note IDs (filenames without `.md`) produced or updated from that raw file. This is how the ledger tracks what's been ingested — without it, the file will show up as "new" on every run.
7. At the end, print a short summary: how many raw files processed, how many notes created, how many notes updated, and which decisions you're least sure about so the user can correct you.

Remember: small, focused notes are better than big ones. Split when in doubt.
