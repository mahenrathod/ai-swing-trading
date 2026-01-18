from pydantic import BaseModel


class Layer1Result(BaseModel):
    ticker: str
    above_200dma: bool
    breakout: bool
    pullback: bool
    rs_score: float
    trend_score: float
    setup: str | None = None
