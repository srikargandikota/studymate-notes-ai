# StudyMate Notes AI

**Paste in messy lecture notes, and get back a summary, the key concepts, and a map of how they connect.**

StudyMate is a classical NLP study tool in Python that turns a raw `.txt` file of notes into three outputs, namely an extractive summary, ranked keywords, and a rendered concept graph. It needs no LLM and no API key, and every result is explainable.

## Why there is no LLM

I left the LLM out for two reasons. First, a study tool has to be trustworthy, and an extractive summary only contains sentences you actually wrote, so it cannot invent a fact the night before a test. Second, building the pipeline from classical parts like TF-IDF, PageRank, tries, and co-occurrence graphs means you can trace exactly why the tool chose a sentence or a keyword.

## What it does

```bash
python app.py --input sample.txt --ratio 0.25 --topk 15 --search "neur"
```

1. **Summarize.** Sentences are vectorized with TF-IDF in a TextRank-style approach, a cosine-similarity graph is built, and PageRank picks the most central sentences, which are kept in their original order.
2. **Extract keywords.** The top-k terms are ranked across the whole document.
3. **Map concepts.** Keywords that co-occur within a sliding window become weighted edges in a NetworkX graph, which is rendered to `concept_map.png`, and closer co-occurrence means a stronger edge.
4. **Search.** Keywords are loaded into a trie for instant prefix lookup, so `--search "neur"` returns every matching concept.

## Files

| File | Role |
|---|---|
| `summarizer.py` | TF-IDF, the cosine graph, and the PageRank extractive summary |
| `keywords.py` | Keyword ranking |
| `concept_graph.py` | Co-occurrence graph construction and PNG rendering |
| `trie.py` | The prefix-search trie |
| `text_utils.py` | Sentence splitting and tokenization |
| `app.py` | The CLI that ties it all together |

## Setup

```bash
pip install -r requirements.txt   # numpy, scikit-learn, networkx, matplotlib
python app.py --input your_notes.txt
```
