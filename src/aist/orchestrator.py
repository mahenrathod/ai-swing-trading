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
    compute_trend_score,
    compute_moving_average
)

from aist.quant_momentum.signals import (
    breakout_signal, 
    pullback_signal,
    is_above_200dma
)

from aist.rag.v1.retriever import retrieve_context_v1
from aist.rag.v1.summarizer import summarize_for_trading_v1

from aist.agents.technical_agent import technical_assessment
from aist.agents.context_agent import context_assessment
from aist.agents.decision_agent import final_decision


from aist.models import Layer1Result

from aist.rag.v2.retriever import retrieve_context_v2
from aist.rag.v2.summarizer import summarize_for_trading_v2

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

    retrieved_docs = retrieve_context_v1(query, top_k=4)
    print(retrieved_docs)
    
    rag_summary = summarize_for_trading_v1(retrieved_docs)
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

def analyze_stock_full_pipeline_v1(ticker: str):
    # -------- Layer 1 --------
    # df = fetch_price_data(ticker, period="11mo")
    df = get_price_data(ticker, period="12mo")
    df = sanitize_for_json(df)
    df = ensure_minimum_history(df)

    latest = get_latest_bar(df)
    last_close = float(latest["close"]) if latest["close"] is not None else None

    # (Placeholder for now -- we'll computer release 200DMA/breakout later)
    dma_200 = compute_moving_average(df, 200)
    print(f"------ dma_200: {dma_200}")
    breakout = None
    volume_score = None
    
    tech_view = technical_assessment(
        last_close=last_close,
        dma_200=dma_200,
        breakout=breakout,
        volume_score=volume_score,
    )

    # -------- Layer 2 --------     
    query = f"{ticker.upper()} earnings, news, sector, macro, playbook"
    retrieved_docs = retrieve_context_v1(query, top_k=4)
    rag_summary = summarize_for_trading_v1(retrieved_docs)
    context_view = context_assessment(rag_summary)

    # -------- Layer 3 --------
    decision = final_decision(
        ticker=ticker,
        last_close=last_close,
        tech=tech_view,
        context=context_view,
    )
    
    return {
        "ticker": ticker.upper(),
        "last_close": last_close,
        "dma_200": round(dma_200, 2),
        "layer1_technical": tech_view,
        "layer2_rag": rag_summary,
        "layer3_decision": decision,
    }

def analyze_stock_full_pipeline_v2(ticker: str):
    query = f"{ticker.upper()} earnings outlook and rence news"
    docs = retrieve_context_v2(query, top_k=10)
    rag_summary = summarize_for_trading_v2(docs)
    return rag_summary