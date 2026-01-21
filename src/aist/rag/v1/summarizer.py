from typing import List, Dict

def summarize_for_trading_v1(results: List[Dict]) -> Dict:
    """
    Convert retrieved documents into a structured trading-friendly summary.
    """

    key_points = []
    risks = []

    for r in results:
        text = r["doc"]["text"]
        source = r["doc"]["source"]
        
        if "earnings" in source:
            key_points.append(text)
        
        if "news" in source:
            key_points.append(text)
        
        if "sector" in source:
            key_points.append(text)
        
        if "macro" in source:
            key_points.append(text)
        
        if "playbook" in source:
            key_points.append(text)

    return {
        "sentiment": "bullish" if any("beat" in kp.lower() for kp in key_points) else "neutral",
        "key_points": key_points,
        "risks": risks,
    }