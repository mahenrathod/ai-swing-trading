from aist.rag.v2.news_loader import fetch_company_news
from aist.rag.v2.embedder import EmbeddingModel
from aist.rag.v2.vector_store import VectorStore    

def retrieve_context_v2(query: str, top_k: int = 3):
    """
    Full RAG retrieval pipeline
    """
    ticker = query.split()[0].upper()
    
    # 1. Load real news
    docs = fetch_company_news(ticker)

    if not docs:
        raise ValueError(f"No news found for ticker: {ticker}")

    # 2. Prepare texts
    texts = [
        f"{doc['title']} {doc['summary']}" for doc in docs
    ]

    # 3. Embed
    embedder = EmbeddingModel()
    embeddings = embedder.embed(texts)

    # 4. Vector store
    store = VectorStore(dim=embeddings.shape[1])
    store.add(embeddings, docs)
    
    # 5. Query
    query_vec = embedder.embed([query])
    return store.search(query_vec, top_k)