from IPython.lib.pretty import pprint
from IPython.lib.pretty import pretty
import yfinance as yf
from datetime import datetime
from typing import List, Dict

def fetch_company_news(ticker: str, limit: int = 10) -> List[Dict]:
    stock = yf.Ticker(ticker.upper())
    print(stock)
    
    # --- INSPECTION ---
    # print("TYPE:", type(stock))
    # print("VARS (Fields):", vars(stock)) 
    # print("DIR (All Attributes):", dir(stock)) # Uncomment to see methods too
    # ------------------

    # NOTE: stock.news is usually a list property, NOT a function. 
    # Calling stock.news() would crash if it's a list.
    news_items = stock.news
    # print("News Items Type:", type(news_items))
    

    """
    {'id': 'd3292c7c-be07-4408-b272-80868428db8a',
 'content': {'id': 'd3292c7c-be07-4408-b272-80868428db8a',
  'contentType': 'STORY',
  'title': 'Nvidia, Tesla lead tech stocks lower as Trump trade war threats rattle market',
  'description': '',
  'summary': 'Tech stocks led broader market declines as investors grew skittish over geopolitical tensions and fears of an AI bubble continued.',
  'pubDate': '2026-01-20T16:29:28Z',
  'displayTime': '2026-01-20T21:40:54Z',
  'isHosted': True,
  'bypassModal': False,
  'previewUrl': None,
  'thumbnail': {'originalUrl': 'https://s.yimg.com/os/creatr-uploaded-images/2026-01/d9e9f850-f619-11f0-b7f3-82aa17ff9d59',
   'originalWidth': 2808,
   'originalHeight': 1872,
   'caption': '',
   'resolutions': [{'url': 'https://s.yimg.com/uu/api/res/1.2/sAPEep6MH5tJCwff2Y4__g--~B/aD0xODcyO3c9MjgwODthcHBpZD15dGFjaHlvbg--/https://s.yimg.com/os/creatr-uploaded-images/2026-01/d9e9f850-f619-11f0-b7f3-82aa17ff9d59',
     'width': 2808,
     'height': 1872,
     'tag': 'original'},
    {'url': 'https://s.yimg.com/uu/api/res/1.2/0Sqeq.Lrjr2lczTz1qMXgQ--~B/Zmk9c3RyaW07aD0xMjg7dz0xNzA7YXBwaWQ9eXRhY2h5b24-/https://s.yimg.com/os/creatr-uploaded-images/2026-01/d9e9f850-f619-11f0-b7f3-82aa17ff9d59',
     'width': 170,
     'height': 128,
     'tag': '170x128'}]},
  'provider': {'displayName': 'Yahoo Finance',
   'url': 'http://finance.yahoo.com/'},
  'canonicalUrl': {'url': 'https://finance.yahoo.com/news/nvidia-tesla-lead-tech-stocks-lower-as-trump-trade-war-threats-rattle-market-162928073.html',
   'site': 'finance',
   'region': 'US',
   'lang': 'en-US'},
  'clickThroughUrl': {'url': 'https://finance.yahoo.com/news/nvidia-tesla-lead-tech-stocks-lower-as-trump-trade-war-threats-rattle-market-162928073.html',
   'site': 'finance',
   'region': 'US',
   'lang': 'en-US'},
  'metadata': {'editorsPick': True},
  'finance': {'premiumFinance': {'isPremiumNews': False,
    'isPremiumFreeNews': False}},
  'storyline': {'storylineItems': [{'content': {'id': '466027d2-1a5c-4582-9527-ca340494f088',
      'contentType': 'STORY',
      'isHosted': True,
      'title': 'Apple will ship millions of $2,000 foldable iPhones this year: Citi',
      'thumbnail': {'originalUrl': 'https://s.yimg.com/os/creatr-uploaded-images/2026-01/03f47170-f60b-11f0-b1fd-1adc98ef3a7c',
       'originalWidth': 8256,
       'originalHeight': 5504,
       'caption': '',
       'resolutions': None},
      'provider': {'displayName': 'Yahoo Finance',
       'sourceId': 'yahoofinance.com'},
      'previewUrl': None,
      'providerContentUrl': '',
      'canonicalUrl': {'url': 'https://finance.yahoo.com/news/apple-will-ship-millions-of-2000-foldable-iphones-this-year-citi-153849468.html'},
      'clickThroughUrl': {'url': 'https://finance.yahoo.com/news/apple-will-ship-millions-of-2000-foldable-iphones-this-year-citi-153849468.html'}}},
    {'content': {'id': '06e5062b-fdc8-4bc8-8668-71d3640486a4',
      'contentType': 'STORY',
      'isHosted': True,
      'title': "Trump's battle for Greenland: Why the stock market hates it all",
      'thumbnail': {'originalUrl': 'https://s.yimg.com/os/creatr-uploaded-images/2026-01/c575b4a0-f5fa-11f0-b3ff-99784c0c86a8',
       'originalWidth': 3753,
       'originalHeight': 4691,
       'caption': '',
       'resolutions': None},
      'provider': {'displayName': 'Yahoo Finance',
       'sourceId': 'yahoofinance.com'},
      'previewUrl': None,
      'providerContentUrl': '',
      'canonicalUrl': {'url': 'https://finance.yahoo.com/news/trumps-battle-for-greenland-why-the-stock-market-hates-it-all-145802180.html'},
      'clickThroughUrl': {'url': 'https://finance.yahoo.com/news/trumps-battle-for-greenland-why-the-stock-market-hates-it-all-145802180.html'}}}]}}}

---------
"""
    docs = []
    for news_item in news_items[:limit]:
        doc = {
            "ticker": ticker.upper(),
            "source": "yfinance",
            "title": news_item["content"]["title"],
            "summary": news_item["content"]["summary"],
            "pubDate": news_item["content"]["pubDate"],
        }
        docs.append(doc)
    return docs