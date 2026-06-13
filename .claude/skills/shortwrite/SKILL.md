---
name: shortwrite
description: Derive a SHORT piece from a long source article, taking a specific angle, through shortwrite.html — a two-pane canvas (left = long source, read-only reference; right = short draft, editable). The user picks a long article + a short draft; Claude reads BOTH and writes/edits the short draft to take the angle declared in the draft's frontmatter, applying the SNS hook playbook. Use when the user says /shortwrite, "open shortwrite", "write a short version", "spin this into an SNS post", "이 관점으로 짧게 써줘", "이 긴 글에서 ___ 관점으로 뽑아줘", or wants to compress a long-form note/guide into a short angled post.
---

# Shortwrite — long source → short angled piece

`shortwrite.html` (repo root) is a two-pane canvas:
- **Left = SOURCE** — a long article (e.g. `wiki/outputs/ko/skillopt-guide.md`), opened read-only as reference, with a TOC.
- **Right = DRAFT** — the new *short* piece, edited in the browser and saved to its own `.md` via the File System Access API.

The user and Claude meet through the **draft file**; the source file is shared read-only context for both. Turn-based, like [[cowrite]].

## The draft file contract

Every short draft carries this frontmatter — the **`angle` and `hook_type` fields are the whole point**:

```
---
title:
angle:        # the specific perspective/hook this piece takes
hook_type:    # 고백+깨달음 / 숫자+반전 / 변신 스토리 / Listicle / 정면반박
source:       # filename of the long source article
format: short
status: draft
---
```

## The loop

1. **Confirm both files.** Identify the long **source** and the short **draft** for the session. Read the `source:` field in the draft frontmatter; if set, that's the long article to compress from.
2. **When the user says "이 관점으로 써줘 / 다듬어줘":**
   - **Read the source article in full** — it's the ground truth for facts.
   - **Read the draft** — especially `angle` and `hook_type`. The angle decides what to keep and what to cut. *One angle per piece.*
   - **Write the short draft** so it pulls only what serves that angle from the source. Don't restate the whole source; a short piece makes ONE point well.
   - Apply the **SNS hook playbook** (see the `cowrite` skill, or `wiki/notes/viral-content-hook-patterns.md`): scroll-stopping first line matched to `hook_type`, concrete evidence (a number/workflow from the source), mirror-question or either/or close, criticize systems not people, no "follow/save" CTA.
   - **Keep it tight.** Target body ~600–800 chars (the corpus save sweet-spot the HTML counts). If the angle needs more, say so rather than padding.
   - Preserve frontmatter; keep `angle`/`hook_type`/`source` accurate.
3. The user hits **초안 열기 / ⟳** in the browser to see your edit. Take turns: they save before handing to you; they reload after you edit.

## Rules

- **Korean first**, matching `wiki/outputs/ko/` voice (same convention as `slowai` and `cowrite`). English only when the user confirms the Korean is final.
- **Faithful to the source.** Never invent facts the long article doesn't support — the short piece is a *compression with a viewpoint*, not new claims.
- **Don't touch `wiki/raw/`.** Short drafts belong in `wiki/outputs/` (disposable, not indexed → no reindex needed).
- One short piece = one angle = one hook. If the user wants a second angle, that's a second draft file.
- Pairs with [[cowrite]] (long-form authoring) and the SNS hook playbook it carries.
