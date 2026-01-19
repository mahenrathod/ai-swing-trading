from aist.orchestrator import analyze_stock_full_pipeline
from fastapi import FastAPI, HTTPException
import uvicorn
from aist.orchestrator import (
    analyze_stock_layer1, 
    analyze_stock_layer1_and_2
)

app = FastAPI(title="AI Swing Trading Recommendation Engine API", version="0.1.0")

@app.get("/")
def read_root():
    return {"message": "AI Swing Trading Recommendation Engine API is running"}

@app.get("/analyze/{ticker}")
def analyze(ticker: str):
    try:
        # result = analyze_stock_layer1(ticker)
        # result = analyze_stock_layer1_and_2(ticker)
        result = analyze_stock_full_pipeline(ticker)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

