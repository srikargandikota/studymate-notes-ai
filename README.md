# 📚 StudyMate Notes AI

**Paste in messy lecture notes. Get back a summary, the key concepts, and a map of how they connect.**

A classical-NLP study tool (Python) that turns a raw `.txt` of notes into three artifacts: an extractive summary, ranked keywords, and a rendered concept graph — no LLM, no API key, fully explainable.

## Why no LLM?

Two reasons. First, study tools should be *trustworthy*: an extractive summary only contains sentences you actually wrote, so it can't hallucinate. Second, building the pipeline from classical components (TF-IDF, PageRank, tries, co-occurrence graphs) means every output is explainable — you can trace exactly why a sentence or keyword was chosen.

## What it does

```bash
python app.py --input sample.txt --ratio 0.25 --topk 15 --search "neur"
```

1. **Summarize** — TextRank-style: sentences are vectorized with TF-IDF, a cosine-similarity graph is built, and PageRank picks the most central sentences (kept in original order)
2. **Extract keywords** — top-k terms ranked across the document
3. **Map concepts** — keywords that co-occur within a sliding window become weighted edges in a NetworkX graph, rendered to `concept_map.png` — closer co-occurrence, stronger edge
4. **Search** — keywords are loaded into a trie for instant prefix lookup (`--search "neur"` → all matching concepts)

## Files

| File | Role |
|---|---|
| `summarizer.py` | TF-IDF + cosine graph + PageRank extractive summary |
| `keywords.py` | Keyword ranking |
| `concept_graph.py` | Co-occurrence graph construction + PNG rendering |
| `trie.py` | Prefix-search trie |
| `text_utils.py` | Sentence splitting / tokenization |
| `app.py` | CLI tying it together |

## Setup

```bash
pip install -r requirements.txt   # numpy, scikit-learn, networkx, matplotlib
python app.py --input your_notes.txt
```
