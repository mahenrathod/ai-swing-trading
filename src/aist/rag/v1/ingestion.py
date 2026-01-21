from typing import List, Dict

def load_sample_corpus() -> List[Dict]:
    """
    In a real system, this would pull:
    - Earnings transcripts
    - News articles
    - Sector reports
    - Your trading notes

    For now, we use a small LOCAL demo corpus.
    """

    docs = [
        {
            "ticker": "NVDA",
            "source": "earnings",
            "text": (
                "NVDA Q3 earnings showed strong data center demand driven by AI. "
                "Revenue beat expectations and guidance was raised for next quarter."
            ),
        },
        {
            "ticker": "NVDA",
            "source": "news",
            "text": (
                "U.S. government considering new export restrictions on advanced AI chips, "
                "which could impact Nvidia sales to China."
            ),
        },
        {
            "ticker": "SEMICONDUCTORS",
            "source": "sector",
            "text": (
                "The semiconductor sector remains in a strong uptrend driven by AI investment, "
                "cloud computing, and data center buildouts."
            ),
        },
        {
            "ticker": "MARKET",
            "source": "macro",
            "text": (
                "Market regime currently risk-on with strong liquidity and positive momentum "
                "across major indices."
            ),
        },
        {
            "ticker": "PLAYBOOK",
            "source": "playbook",
            "text": (
                "Your trading playbook: Buy breakouts above resistance after strong earnings, "
                "especially when volume is above average."
            ),
        },
    ]

    return docs
