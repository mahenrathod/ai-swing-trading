import pandas as pd
import yfinance as yf

def get_price_data(ticker, period="6mo") -> pd.DataFrame:
    """
    Fetch OHLCV data for a ticker and normalize columns.
    """
    print(f"--- Getting price data for {ticker} from yfinance for period {period}")
    df = yf.download(ticker, period=period, auto_adjust=False)

    # df = yf.download(
    #     tickers=ticker,
    #     period=period,
    #     interval=interval,
    #     auto_adjust=auto_adjust,
    #     progress=False
    # )
    
    print(f"--- Price data for {ticker} from yfinance for period {period}: {df}")
    if df.empty:
        raise ValueError(f"No data found for ticker: {ticker}")
    
    print("0")
    df = df.reset_index()
    print("1")

    print("column names BEFORE normalising:")
    for c in df.columns:
        print(f"--- Column: {c}")
    
    # Handle MultiIndex columns (tuples) by joining them or taking first non-empty value
    def normalize_column_name(c):
        if isinstance(c, tuple):
            # Join tuple elements, filter out empty strings
            parts = [str(part) for part in c if part]
            c = parts[0] if parts else ''
        return c.lower() if c else c
    
    df.columns = [normalize_column_name(c) for c in df.columns]
    print("column names AFTER normalising:")
    for c in df.columns:
        print(f"--- Column: {c}")

    print(f"--- DataFrame size: {df.shape[0]} rows x {df.shape[1]} columns")
    print("2")
    return df

def get_price_data(ticker: str, period="11mo") -> pd.DataFrame:
    df = yf.download(ticker, period=period)
    df = df.reset_index()
    df.columns = [str(c[0]).lower() for c in df.columns]
    print(f"--- Column: {[c for c in df.columns]}")
    print(f"--- Price data for {ticker} from yfinance for period {period}: {df}")
    return df


def sanitize_for_json(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replace NaN / Inf values with None so FastAPI can serialize safely.
    """
    print("sanitize_for_json...")
    print(f"check if any cell is NaN: {df.isna().any().any()}")
    print(f"count NaN values: {df.isna().sum().sum()}")
    print(f"alternatively count using numpy values: {df.isna().values.any()}")
    return df.replace(
        {
            pd.NA: None,
            float("nan"): None,
            float("inf"): None,
            float("-inf"): None,
        }
    )



# second code base


def fetch_price_data(
    ticker: str,
    period: str = "6mo",
    interval: str = "1d",
    auto_adjust: bool = True
) -> pd.DataFrame:
    """
    Fetch historical price data for a given ticker.

    This is the core market data source for Layer 1 (Momentum).

    Args:
        ticker: Stock ticker symbol (e.g., "NVDA")
        period: Lookback window (e.g., "3mo", "6mo", "1y")
        interval: Data frequency ("1d", "1h", etc.)
        auto_adjust: Use adjusted prices (dividends/splits)

    Returns:
        Cleaned pandas DataFrame with OHLCV data.
    """

    ticker = ticker.upper().strip()

    df = yf.download(
        tickers=ticker,
        period=period,
        interval=interval,
        auto_adjust=auto_adjust,
        progress=False
    )

    if df is None or df.empty:
        raise ValueError(f"No price data found for ticker: {ticker}")

    # Standardize column names (helpful downstream)
    df = df.rename(columns={
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })

    # Ensure index is datetime
    df.index = pd.to_datetime(df.index)

    # Sort by time (oldest → newest)
    df = df.sort_index()

    return df


def get_latest_bar(df: pd.DataFrame) -> pd.Series:
    """
    Return the most recent daily bar.
    Useful for signals / UI display.
    """
    if df is None or df.empty:
        raise ValueError("Empty DataFrame passed to get_latest_bar()")

    return df.iloc[-1]


def ensure_minimum_history(
    df: pd.DataFrame,
    min_days: int = 200
) -> pd.DataFrame:
    """
    Ensure we have enough history for 200DMA calculations.

    If not enough data, raise an error.
    """

    if len(df) < min_days:
        raise ValueError(
            f"Insufficient history: got {len(df)} days, "
            f"need at least {min_days} days"
        )

    return df
