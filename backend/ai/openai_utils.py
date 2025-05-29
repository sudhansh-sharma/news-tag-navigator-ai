import os
import openai
from .stock_universe import StockUniverse
from typing import List, Dict, Optional

def analyze_news_with_gpt(news_list: List[Dict], stock_universe: Optional[StockUniverse] = None):
    """
    Analyze news articles using GPT and map them to stock universe if provided.
    
    Args:
        news_list: List of news articles to analyze
        stock_universe: Optional StockUniverse instance for mapping companies to stocks
        
    Returns:
        Dictionary containing analyzed signals and news
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment")
    client = openai.OpenAI(api_key=api_key)
    
    # Create a prompt that includes instructions for company name extraction
    prompt = (
        "You are a financial news AI assistant. "
        "Analyze the following news items for stock market relevance and sentiment. "
        "For each news item, if it is related to the stock market or a company, extract trading signals and structured news info. "
        "Ignore and do not include any news that is not related to the stock market or a company.\n"
        "IMPORTANT: Extract company names mentioned in the news. These should be the full, official company names.\n"
        "Return your answer as a single JSON object with two keys: 'signals' and 'news'.\n"
        "For each signal, extract and highlight these fields and their values: "
        "- id: unique string for the signal\n"
        "- type: 'buy' or 'sell'\n"
        "- symbol: stock ticker symbol (e.g., 'AAPL', 'TSLA')\n"
        "- price: float\n"
        "- timestamp: ISO8601 datetime string\n"
        "- confidence: string (e.g., 'high', 'medium', 'low')\n"
        "- reason: short text explaining the signal\n"
        "For each news item, extract and highlight these fields and their values: "
        "- id: unique string for the news\n"
        "- title: headline\n"
        "- summary: short summary\n"
        "- content: full article content\n"
        "- publishedAt: ISO8601 datetime string\n"
        "- source: news source\n"
        "- url: link to the news\n"
        "- tags: object with\n"
        "    - sectors: list of sectors\n"
        "    - stocks: list of stock symbols\n"
        "    - sentiment: string (e.g., 'positive', 'negative', 'neutral')\n"
        "    - impact: string (e.g., 'high', 'medium', 'low')\n"
        "    - companies: list of company names mentioned in the news\n"
        "Use the following format strictly (no extra text):\n"
        "{"
        "  'signals': ["
        "    { 'id': '...', 'type': 'buy', 'symbol': '...', 'price': 0.0, 'timestamp': '...', 'confidence': '...', 'reason': '...' }"
        "  ],"
        "  'news': ["
        "    { 'id': '...', 'title': '...', 'summary': '...', 'content': '...', 'publishedAt': '...', 'source': '...', 'url': '...', 'tags': { 'sectors': [...], 'stocks': [...], 'sentiment': '...', 'impact': '...', 'companies': [...] } }"
        "  ]"
        "}\n"
        f"News: {news_list}"
    )
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    
    import json
    try:
        result = json.loads(response.choices[0].message.content)
        
        # If stock universe is provided, map companies to stock symbols
        if stock_universe:
            for news_item in result.get("news", []):
                companies = news_item.get("tags", {}).get("companies", [])
                if companies:
                    # Find matching stocks for the companies mentioned
                    matched_stocks = stock_universe.find_matching_stocks(companies)
                    if matched_stocks:
                        # Update the stocks list with matched symbols
                        news_item["tags"]["stocks"] = [stock["symbol"] for stock in matched_stocks]
                        # Add matched stock info to the news item
                        news_item["tags"]["matched_stocks"] = matched_stocks
                    else:
                        # If no matches found, remove the news item
                        result["news"].remove(news_item)
            
            # Filter out signals that don't match any stocks in our universe
            result["signals"] = [
                signal for signal in result.get("signals", [])
                if stock_universe.get_stock_info(signal.get("symbol"))
            ]
        
        return result
    except Exception as e:
        print(f"Error parsing GPT response: {e}")
        return {"signals": [], "news": []} 