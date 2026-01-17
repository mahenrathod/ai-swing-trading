from fastapi import FastAPI

app = FastAPI(title="AI Swing Trading API", description="API for AI Swing Trading", version="0.1.0")

@app.get("/")
def read_root():
    return {"message": "Swing Trading API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)