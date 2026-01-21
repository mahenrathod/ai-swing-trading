import faiss
import numpy as np

class VectorStore:
    def __init__(self, dim: int): 
        self.index = faiss.IndexFlatL2(dim)
        self.documents = []

    def add(self, embeddings: np.ndarray, documents: list[dict]):
        self.index.add(embeddings)
        self.documents.extend(documents)

    def search(self, query_vector: np.ndarray, top_k: int = 3):
        distances, indices = self.index.search(query_vector, top_k)
        results = []
        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])
        return results
