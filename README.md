# ai-swing-trading
Step-1: Create an empty github repo and follow:
- Create an empty folder in your macboo called "ai-swing-trading"
- cd ai-swing-trading
- echo "# ai-swing-trading" >> README.md
- git init
- git add README.md
- git commit -m "first commit Mahen"
- git branch -M main
- git remote add origin https://github.com/mahenrathod/ai-swing-trading.git
- git push -u origin main

Step-2: Create project structure
- uv --version
- uv init command will create initial project with pyproject.toml
- add below dependencies in pyproject.toml
    fastapi
    uvicorn
    pandas
    numpy
    yfinance
- uv sync command will install all depenencies provided in pyproject.toml inside .venv folder
- create .env file to store secrets and api keys

# Architecture

Layer 1 (quant_momentum)
- Price, 200DMA, breakout, volume
        
Layer 2 (RAG)   
- Create a pipeline that:
    - Collects documents: Earnings transcripts, News articles, Sector reports, Your trading notes
    - Chunks them into small pieces
    - Creates embeddings
    - Stores them in a vector database
      - Example: 
        - FAISS - Facebook AI Similarity Search, 
        - Pinecone
        - ChromaDB
        - Weaviate
        - Qdrant
    
- Query: "Stock earnings + recent news + sector context"
- Retrieve top relevant documents
- Summarize for trading decision
- Example:
    - Input: "NVDA"
    - Convert to query: "Latest NVDA earnings, guidance, and relevant news"
    - Retrieve top 5 most similar documents from vector DB with cosine similarity. 
    - The formual is as follows:
      - cos_sim = dot_product(v1, v2) / (norm(v1) * norm(v2))
    - Pythonic way: 
        ```python
        sims = self.vectors @ query_vector
        ```

    - LLM summarizes them in trading-friendly format:
        - Bullish / Bearish
        - Key risks
        - Key drivers
- Json:
```json
{
  "ticker": "NVDA",
  "rag_summary": {
    "sentiment": "bullish",
    "key_points": [
      "Data center revenue beat expectations",
      "Guidance raised for next quarter",
      "Strong demand from cloud providers"
    ],
    "risks": [
      "Potential China export restrictions"
    ]
  }
}
```

**Code Structure:**
```
src/
└── aist/
    ├── quant_momentum/   # Layer 1 (you already started)
    │
    ├── rag/              # NEW: Layer 2
    │   ├── __init__.py
    │   ├── ingestion.py      # Load & chunk docs
    │   ├── embeddings.py     # Create embeddings
    │   ├── vector_store.py   # Pinecone / FAISS wrapper
    │   ├── retriever.py      # Query logic
    │   └── summarizer.py     # LLM summarization
    │
    ├── agents/           # Layer 3 (later)
    │
    ├── orchestrator.py   # Coordinates L1 → L2 → L3
    └── main.py
```

Layer 3 (Agents) 
- Entry, Stop, Target

# Commands
- uv init
- uv sync
- uv pip list
- uv run uvicorn src.aist.main:app --reload
