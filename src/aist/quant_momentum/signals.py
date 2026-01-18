# src/msip/momentum/signals.py

import pandas as pd


def is_above_200dma(df: pd.DataFrame) -> bool:
    print(f"--- Checking if close is above 200 day moving average")
    # print df columns
    print(f"--- DataFrame columns: {df.columns}")
    most_recent_closing_price = 0 if pd.isna(df["close"].iloc[-1]) else df["close"].iloc[-1]
    most_recent_ma200_price = 0 if pd.isna(df["ma200"].iloc[-1]) else df["ma200"].iloc[-1]
    boolval = bool(most_recent_closing_price > most_recent_ma200_price)
    print(f"boolval: {boolval}")
    return boolval


def breakout_signal(df: pd.DataFrame) -> bool:
    print(f"--- Checking for breakout signal")
    """
    Breakout: today's close > 20-day high + volume surge.
    """
    recent_high = df["high"].rolling(20).max().iloc[-2]
    today_close = df["close"].iloc[-1]

    avg_vol = df["volume"].rolling(20).mean().iloc[-1]
    vol_surge = df["volume"].iloc[-1] > 1.5 * avg_vol

    return bool(today_close > recent_high and vol_surge)


def pullback_signal(df: pd.DataFrame) -> bool:
    print(f"--- Checking for pullback signal")
    """
    Pullback: 3–10% drawdown + near 50DMA.
    """
    recent_high = df["high"].rolling(20).max().iloc[-1]
    today_close = df["close"].iloc[-1]

    drawdown = (recent_high - today_close) / recent_high

    ma50_value = df["ma50"].iloc[-1]
    # Handle NaN: if ma50 is NaN, can't determine if near 50DMA
    if pd.isna(ma50_value):
        return False
    
    near_50dma = (
        abs(today_close - ma50_value) / ma50_value < 0.02
    )

    return bool(0.03 <= drawdown <= 0.10 and near_50dma)
