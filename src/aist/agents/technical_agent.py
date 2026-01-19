from typing import Dict, Any


def technical_assessment(
    last_close: float,
    dma_200: float | None = None,
    breakout: bool | None = None,
    volume_score: float | None = None,
    ) -> Dict:
    """
    Simple rule-based technical analysis agent.
    """
    bias = "neutral"
    reasons = []

    print(f"last_close: {last_close}")
    print(f"dma_200: {dma_200}")
    print(f"breakout: {breakout}")
    print(f"volume_score: {volume_score}")
    
    if dma_200 and last_close > dma_200:
        bias = "bullish"
        reasons.append("Price is above 200DMA")
    
    if breakout:
        bias = "bullish"
        reasons.append("Breakout detected")

    if volume_score and volume_score > 1.2:
        reasons.append("Above average volume")

    if last_close and last_close < dma_200:
        bias = "bearish"
        reasons.append("Price is below 200DMA")

    return {
        "bias": bias,
        "reasons": reasons
    }