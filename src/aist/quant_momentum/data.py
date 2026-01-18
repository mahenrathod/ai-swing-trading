import pandas as pd
import yfinance as yf

# def get_price_data(ticker, period="6mo") -> pd.DataFrame:
#     """
#     Fetch OHLCV data for a ticker and normalize columns.
#     """
#     print(f"--- Getting price data for {ticker} from yfinance for period {period}")
#     df = yf.download(ticker, period=period, auto_adjust=False)
    
#     print(f"--- Price data for {ticker} from yfinance for period {period}: {df}")
#     if df.empty:
#         raise ValueError(f"No data found for ticker: {ticker}")
    
#     print("0")
#     df = df.reset_index()
#     print("1")

#     print("column names BEFORE normalising:")
#     for c in df.columns:
#         print(f"--- Column: {c}")
    
#     # Handle MultiIndex columns (tuples) by joining them or taking first non-empty value
#     def normalize_column_name(c):
#         if isinstance(c, tuple):
#             # Join tuple elements, filter out empty strings
#             parts = [str(part) for part in c if part]
#             c = parts[0] if parts else ''
#         return c.lower() if c else c
    
#     df.columns = [normalize_column_name(c) for c in df.columns]
#     print("column names AFTER normalising:")
#     for c in df.columns:
#         print(f"--- Column: {c}")

#     print(f"--- DataFrame size: {df.shape[0]} rows x {df.shape[1]} columns")
#     print("2")
#     return df

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
