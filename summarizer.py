import numpy as np
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer

def summarize_text(text: str, ratio: float = 0.25, min_sent: int = 3):
    # 1) Sentence split
    from text_utils import split_sentences
    sents = split_sentences(text)
    if not sents:
        return []

    # number of sentences to keep
    k = max(min_sent, int(len(sents) * ratio))
    k = min(k, len(sents))

    # 2) TF-IDF on sentences
    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform(sents)              # shape: (num_sents, vocab)
    # 3) Cosine similarity matrix
    norm = np.linalg.norm(X.toarray(), axis=1, keepdims=True) + 1e-12
    M = (X @ X.T).toarray() / (norm @ norm.T)

    # 4) Graph + PageRank
    np.fill_diagonal(M, 0.0)
    G = nx.from_numpy_array(M)                # weighted, undirected
    scores = nx.pagerank(G, weight="weight")

    # 5) Pick top-k by score, keep original order
    idx_sorted = sorted(scores, key=scores.get, reverse=True)[:k]
    idx_keep = sorted(idx_sorted)
    return [sents[i] for i in idx_keep]
