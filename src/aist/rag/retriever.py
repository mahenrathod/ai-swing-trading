from typing import List, Dict
import numpy as np

from aist.rag.ingestion import load_sample_corpus
from aist.rag.embeddings import embed_corpus, embed_text
from aist.rag.vector_store import LocalVectorStore

# Build RAG index once (simple demo)
_DOCS = load_sample_corpus()
_VECTORS, _VOCAB = embed_corpus(_DOCS)
_VECTOR_STORE = LocalVectorStore(_DOCS, _VECTORS)

def retrieve_context(query: str, top_k: int = 3) -> List[Dict]:
    """
    Given a query (e.g., "NVDA earnings"), retrieve top_k most relevant documents.
    """
    query_vector = embed_text(query, _VOCAB)
    results = _VECTOR_STORE.search(query_vector, top_k)
    return results