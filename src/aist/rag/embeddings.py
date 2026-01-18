import numpy as np
from typing import List, Dict, Tuple

def build_vocabulary(docs: List[Dict]) -> List[str]:
    """
    Build a simple vocabulary from all documents.
    """
    vocab = set()

    for d in docs:
        words = d["text"].lower().replace(".", "").replace(",", "").split()
        vocab.update(words)

    return sorted(list(vocab))


def embed_text(text: str, vocab: List[str]) -> np.ndarray:
    """
    Convert text into a simple bag-of-words vector.
    """
    words = text.lower().replace(".", "").replace(",", "").split()
    vec = np.zeros(len(vocab))

    for i, term in enumerate(vocab):
        vec[i] = words.count(term)

    # Normalize for cosine similarity
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm

    return vec


def embed_corpus(docs: List[Dict]) -> Tuple[List[np.ndarray], List[str]]:
    """
    Create embeddings for all documents.
    Returns:
      - list of vectors
      - shared vocabulary
    """
    vocab = build_vocabulary(docs)

    vectors = []
    for d in docs:
        vectors.append(embed_text(d["text"], vocab))

    return vectors, vocab
