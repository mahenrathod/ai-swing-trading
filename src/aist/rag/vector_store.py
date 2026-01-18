import numpy as np  
from typing import List, Dict   

class LocalVectorStore:
    def __init__(self, docs: List[Dict], vectors: List[np.ndarray]):
        self.docs = docs
        self.vectors = vectors

    def search(self, query_vector: np.ndarray, top_k: int = 3):
        """
        Cosine similarity search.
        Returns top_k most relevant documents.
        """

        # Compute cosine similarity between query and all documents (dot products since vectors are normalized)
        sims = self.vectors @ query_vector  

        # Get indices of top matches
        top_indices = np.argsort(sims)[-top_k:][::-1]

        """
        Example:

        # Similarity scores for 5 documents
        sims = np.array([0.42, 0.96, 0.79, 0.15, 0.88])
                         ↑     ↑     ↑     ↑     ↑
                       idx 0   1     2     3     4
        top_k = 3
        
        Step 1: np.argsort(sims) - indices that sort ascending
        argsort_result = np.argsort(sims)
         [3, 0, 2, 4, 1]
         Meaning: sims[3]=0.15 < sims[0]=0.42 < sims[2]=0.79 < sims[4]=0.88 < sims[1]=0.96
        
        Step 2: [-top_k:] - take last 3 elements
        last_k = argsort_result[-3:]
         [2, 4, 1]
         These are indices of the 3 highest scores (but in ascending order)
        
        Step 3: [::-1] - reverse to get descending order
        top_indices = last_k[::-1]
         [1, 4, 2]
         Final result: indices in order of highest to lowest similarity
        """
    
        results = []
        for i in top_indices:
            results.append({
                "doc": self.docs[i],
                "score": float(sims[i])
                })

        return results