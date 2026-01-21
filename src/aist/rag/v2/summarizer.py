# Deterministic output (No Hallucination)

def summarize_for_trading_v2(docs: list[dict]) -> dict:
    """
    Convert retrieved documents into trading relevant context.
    """

    if not docs:
        return {
            "sentiment": "neutral",
            "key_points": [],
            "risks": []
        }

    key_points = []
    risks = []

    for doc in docs:
        text = f"{doc['title']} {doc['summary']}".lower()

        key_points.append(doc['title'])
        
        if any(word in text for word in ['risk', 'warning', 'caution', 'lawsuit', 'litigation', 'fraud', 'probe']):
            risks.append(doc['title'])

        sentiment = "bullish"
        if risks:
            sentiment = "mixed"

    return {
        "sentiment": sentiment,
        "key_points": key_points,
        "risks": risks
    }