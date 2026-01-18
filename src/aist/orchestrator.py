from aist.quant_momentum.data import (
    get_price_data,
    sanitize_for_json
)
from aist.quant_momentum.indicators import (
    add_moving_averages, 
    compute_relative_strength, 
    compute_trend_score
)

from aist.quant_momentum.signals import (
    breakout_signal, 
    pullback_signal,
    is_above_200dma
)

from aist.models import Layer1Result

def analyze_stock_layer1(ticker: str) -> Layer1Result:
    ticker = ticker.upper()

    # Get data
    df = get_price_data(ticker)

    # Sanitize
    df = sanitize_for_json(df)

    # Get moving averages
    df = add_moving_averages(df)

    # Benchmark for RS
    spy = get_price_data("SPY")
    spy = add_moving_averages(spy)

    rs = compute_relative_strength(df, spy)
    trend = compute_trend_score(df)
    print(f"trend: {trend}")

    breakout = breakout_signal(df)
    pullback = pullback_signal(df)

    # Determine primary setup
    if breakout:
        setup = "breakout"
    elif pullback:
        setup = "pullback"
    else:
        setup = None

    print(f"Layer 1 Analysis for {ticker}: setup: {setup}")

    return Layer1Result(
        ticker=ticker,
        above_200dma=is_above_200dma(df),
        breakout=breakout,
        pullback=pullback,
        rs_score=round(rs, 4),
        trend_score=trend,
        setup=setup,
    )