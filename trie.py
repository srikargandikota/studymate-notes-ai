class TrieNode:
    __slots__ = ("children", "end")
    def __init__(self):
        self.children = {}
        self.end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.end = True

    def _collect(self, node, prefix, out, limit):
        if len(out) >= limit: return
        if node.end: out.append(prefix)
        for ch, nxt in node.children.items():
            self._collect(nxt, prefix+ch, out, limit)

    def search_prefix(self, prefix: str, limit=20):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        out = []
        self._collect(node, prefix, out, limit)
        return out
