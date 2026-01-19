from typing import Dict

def context_assessment(rag_summary: Dict) -> Dict:
    """
    Interpret RAG output into a trading bias.
    """

    sentiment = rag_summary.get("sentiment", "neutral")
    risks = []
    bias = "bullish" if sentiment == "bullish" else "neutral"
    if risks:
        bias = "neutral" if bias == "bullish" else bias

    return {

        "bias": bias,
        "key_points": rag_summary.get("key_points", []),
        "risks": risks,
    }    
    

