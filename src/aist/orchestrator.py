from aist.quant_momentum.data import (
    get_price_data,
    sanitize_for_json,
    fetch_price_data,
    ensure_minimum_history,
    get_latest_bar
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

from aist.rag.retriever import retrieve_context
from aist.rag.summarizer import summarize_for_trading

from aist.agents.technical_agent import technical_assessment
from aist.agents.context_agent import context_assessment
from aist.agents.decision_agent import final_decision


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

def analyze_stock_layer1_and_2(ticker: str):
    # ------- Layer 1 -------
    df = fetch_price_data(ticker, period="11mo")
    df = sanitize_for_json(df)
    df = ensure_minimum_history(df)
    # df = add_moving_averages(df)
    latest = get_latest_bar(df)
    

    print(f"Layer 1 Analysis for {ticker} is FINISHED...")
    # ------- Layer 2 -------
    
    query = f"{ticker.upper()} earnings, news, sector, macro, playbook"
    print(query)

    retrieved_docs = retrieve_context(query, top_k=4)
    print(retrieved_docs)
    
    rag_summary = summarize_for_trading(retrieved_docs)
    print(rag_summary)

    return {
        "ticker": ticker.upper(),
        "rows": len(df),
        "last_close": float(latest["close"]) if latest["close"] is not None else None,
        # "20dma": df["20dma"],
        # "50dma": df["50dma"],
        # "200dma": df["200dma"],
        "rag_summary": rag_summary,
    }

def analyze_stock_full_pipeline(ticker: str):
    # -------- Layer 1 --------
    df = fetch_price_data(ticker, period="11mo")
    df = sanitize_for_json(df)
    df = ensure_minimum_history(df)
    latest = get_latest_bar(df)
    print(latest["close"])
    last_close = float(latest["close"]) if latest["close"] is not None else None

    print(f"last_close: {last_close}")
    # (Placeholder for now -- we'll computer release 200DMA/breakout later)
    dma_200 = 180.00
    breakout = None
    volume_score = None
    
    tech_view = technical_assessment(
        last_close=last_close,
        dma_200=dma_200,
        breakout=breakout,
        volume_score=volume_score,
    )

    print(f"tech_view: {tech_view}")

    # -------- Layer 2 --------     
    query = f"{ticker.upper()} earnings, news, sector, macro, playbook"
    print(query)
    retrieved_docs = retrieve_context(query, top_k=4)
    print(f"retrieved_docs: {retrieved_docs}")
    rag_summary = summarize_for_trading(retrieved_docs)
    print(f"rag_summary: {rag_summary}")
    context_view = context_assessment(rag_summary)
    print(f"context_view: {context_view}")

    # -------- Layer 3 --------
    decision = final_decision(
        ticker=ticker,
        last_close=last_close,
        tech=tech_view,
        context=context_view,
    )
    print(f"decision: {decision}")
    
    return {
        "ticker": ticker.upper(),
        "last_close": last_close,
        "layer1_technical": tech_view,
        "layer2_rag": rag_summary,
        "layer3_decision": decision,
    }
    