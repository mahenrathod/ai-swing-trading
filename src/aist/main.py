from fastapi import FastAPI, HTTPException
import uvicorn
from aist.orchestrator import analyze_stock_layer1

app = FastAPI(title="AI Swing Trading API", description="API for AI Swing Trading", version="0.1.0")

@app.get("/")
def read_root():
    return {"message": "Swing Trading API is running"}

@app.get("/analyze/{ticker}")
def analyze(ticker: str):
    try:
        result = analyze_stock_layer1(ticker)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

