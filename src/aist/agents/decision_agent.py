from typing import Dict

def final_decision(
    ticker: str,
    last_close: float,
    tech: Dict,
    context: Dict,
) -> Dict:
    """
    Combines technical + context signals into a final trade decision.
    """

    tech_bias = tech.get("bias", "neutral")
    context_bias = context.get("bias", "neutral")

    # Default
    decision = "PASS"
    entry = None
    stop = None
    target = None
    confidence = 0.5

    # Simple decision rules
    if tech_bias == "bullish" and context_bias == "bullish":
        decision = "BUY"
        entry = round(last_close * 0.99, 2) # slight pullback entry
        stop = round(last_close * 0.95, 2) # 5% stop loss
        target = round(last_close * 1.08, 2) # 8% target
        confidence = 0.75

    elif tech_bias == "bullish" and context_bias == "neutral":
        decision = "HOLD"
        confidence = 0.60

    elif tech_bias == "bearish":
        decision = "PASS"
        confidence = 0.55

    return {
        "ticker": ticker.upper(),
        "decision": decision,
        "entry_zone": entry,
        "stop_loss": stop,
        "take_profit": target,
        "confidence": confidence,
        "technical_reasons": tech.get("reasons", []),
        "context_risks": context.get("risks", []),
    }