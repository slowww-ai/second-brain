---
description: Ask a question and get an answer grounded in your wiki notes
argument-hint: <question>
---

Question: $ARGUMENTS

Answer the user's question using only information from `wiki/notes/`. Be concise and direct.

Steps:

1. Run `python scripts/search.py "<relevant keywords>"` with 2-3 query variations to find notes that address the question. Remember to load the env first: `set -a; source .env; set +a`.
2. Read the top 5-8 hits in full. Follow `[[wikilinks]]` one hop if they seem directly relevant to the question.
3. Answer the question in a few paragraphs. Cite notes inline using `[[note-id]]` so the user can dig deeper.
4. If the wiki has no relevant notes, say so clearly — do not hallucinate or pull from general knowledge. Suggest a `/jina-capture` or `/ingest` if the gap could be filled.
5. Keep the answer conversational and under ~300 words. Do not write to any file — just reply in chat.
