# src/msip/momentum/indicators.py

import pandas as pd


def add_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    print(f"--- Adding moving averages")
    if "close" in df.columns:
        print("Contains 'close' column")
    else:
        raise KeyError(f"'close' column not found. Available columns: {list(df.columns)}")

    print(f"--- Adding 200 day moving average")
    df["ma200"] = df["close"].rolling(window=200).mean()
    print(f"--- 200 day moving average: {df['ma200']}")
    print("|*************")
    for col in df.columns:
        print(f"  - Column: '{col}' (type: {type(col).__name__})")

    return df


def compute_relative_strength(
    stock_df: pd.DataFrame, market_df: pd.DataFrame, lookback_days: int = 63
) -> float:
    """
    Simple RS: stock return minus market return over lookback period.
    """

    print("compute_relative_strength...")
    if len(stock_df) < lookback_days or len(market_df) < lookback_days:
        return 0.0

    stock_ret = stock_df["close"].iloc[-1] / stock_df["close"].iloc[-lookback_days] - 1
    mkt_ret = market_df["close"].iloc[-1] / market_df["close"].iloc[-lookback_days] - 1

    return float(stock_ret - mkt_ret)


def compute_trend_score(df: pd.DataFrame) -> float:
    """
    TODO: rework
    A simple composite trend score (0–1) based on:
    - distance from 200DMA
    - slope of 50DMA
    """
    print("compute_trend_score...")
    if df["ma200"].iloc[-1] is None or df["ma50"].iloc[-1] is None:
        return 0.0
    
    price = df["close"].iloc[-1]
    ma200 = df["ma200"].iloc[-1]

    # 1) Price vs 200DMA component
    dist_200 = (price - ma200) / ma200
    dist_score = min(max((dist_200 + 0.1) * 5, 0), 1)  # normalize to ~0-1

    # 2) 50DMA slope component
    ma50_now = df["ma50"].iloc[-1]
    ma50_prev = df["ma50"].iloc[-5] if len(df) > 5 else ma50_now

    slope = (ma50_now - ma50_prev) / ma50_prev if ma50_prev != 0 else 0
    slope_score = min(max((slope + 0.01) * 10, 0), 1)

    # Composite
    # return round((dist_score * 0.6 + slope_score * 0.4), 3)
    print(f"price: {price}, ma200: {ma200}")
    return price;

def compute_moving_average(df: pd.DataFrame, dma: int = 20) -> pd.DataFrame:

    print(f"compute_moving_averages... {dma}")
    ma = df["close"].rolling(window=dma).mean().iloc[-1]
    print(f"ma: {ma}")
    return ma