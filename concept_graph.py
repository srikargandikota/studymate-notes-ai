import networkx as nx
import matplotlib.pyplot as plt
from text_utils import tokenize

def build_concept_graph(sentences, keywords, window=8, min_co=1):
    K = set(keywords)
    # Flatten tokens across the whole doc
    tokens = [tok for s in sentences for tok in tokenize(s)]
    G = nx.Graph()
    G.add_nodes_from(keywords)

    n = len(tokens)
    for i, wi in enumerate(tokens):
        if wi not in K:
            continue
        # look ahead within a sliding window
        for j in range(i+1, min(i+window, n)):
            wj = tokens[j]
            if wj not in K:
                continue
            # closer pairs get slightly higher weight
            inc = 1.0 / (j - i)
            if G.has_edge(wi, wj):
                G[wi][wj]["weight"] += inc
            else:
                G.add_edge(wi, wj, weight=inc)

    # prune weak edges
    to_remove = [(u,v) for u,v,w in G.edges(data="weight") if w < float(min_co)]
    G.remove_edges_from(to_remove)
    return G

def save_concept_map(G, out_path="concept_map.png"):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8,6))
    # scale node size by degree (visibility without custom colors)
    deg = dict(G.degree(weight="weight"))
    sizes = [300 + 120 * deg.get(n, 0) for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=sizes)
    nx.draw_networkx_labels(G, pos, font_size=9)
    widths = [max(1.0, G[u][v]["weight"] * 2.0) for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=widths)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()
    return out_path
