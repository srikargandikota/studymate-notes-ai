import argparse
from pathlib import Path
from summarizer import summarize_text
from keywords import top_keywords
from trie import Trie
from concept_graph import build_concept_graph, save_concept_map
from text_utils import split_sentences

def main():
    p = argparse.ArgumentParser(description="StudyMate: summarize notes + keywords + concept map")
    p.add_argument("--input", required=True, help="Path to a .txt file with notes")
    p.add_argument("--ratio", type=float, default=0.25, help="Summary ratio (0..1)")
    p.add_argument("--topk", type=int, default=15, help="Top keywords")
    p.add_argument("--min_co", type=int, default=2, help="Min co-occurrence for concept edges")
    p.add_argument("--search", type=str, default="", help="Keyword prefix to search (Trie)")
    p.add_argument("--map_out", type=str, default="concept_map.png", help="Output PNG for concept map")
    args = p.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    sentences = split_sentences(text)

    summary_sents = summarize_text(text, ratio=args.ratio)
    keywords = top_keywords(sentences, topk=args.topk)

    # Build Trie for prefix lookup
    trie = Trie()
    for w in keywords:
        trie.insert(w)

    # Build & save concept map
    G = build_concept_graph(sentences, keywords, min_co=args.min_co)
    img = save_concept_map(G, out_path=args.map_out)

    # Output
    print("\n=== SUMMARY ===")
    print(" ".join(summary_sents))
    print("\n=== KEYWORDS ===")
    print(", ".join(keywords))

    if args.search:
        print(f"\n=== PREFIX SEARCH: '{args.search}' ===")
        print(", ".join(trie.search_prefix(args.search, limit=20)))

    print(f"\nConcept map saved -> {img}")

if __name__ == "__main__":
    main()
