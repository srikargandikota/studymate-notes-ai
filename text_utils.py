import re

WORD_RE = re.compile(r"[A-Za-z']+")

def split_sentences(text: str):
    # Simple rule-based splitter: keeps ., !, ? as sentence ends
    text = text.strip()
    if not text:
        return []
    return re.split(r"(?<=[.!?])\s+", text)

def tokenize(text: str):
    return [w.lower() for w in WORD_RE.findall(text)]

def sentences_tokens(sentences):
    return [tokenize(s) for s in sentences]
