import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def top_keywords(sentences, topk=15):
    if not sentences:
        return []
    vec = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),                # ← allow phrases
        token_pattern=r"(?u)\b[a-zA-Z]{2,}\b",  # ignore 1-char tokens
        max_features=200                   # cap vocab for small docs
    )
    X = vec.fit_transform(sentences)
    scores = np.asarray(X.sum(axis=0)).ravel()
    terms = np.array(vec.get_feature_names_out())
    order = scores.argsort()[::-1]
    return terms[order][:topk].tolist()
