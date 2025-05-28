import os
import openai

def analyze_news_with_gpt(news_list):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment")
    openai.api_key = api_key
    prompt = (
        "You are a financial news AI assistant. "
        "Analyze the following news items for stock market relevance and sentiment. "
        "For each news item, if it is related to the stock market or a company, extract trading signals and structured news info. "
        "Ignore and do not include any news that is not related to the stock market or a company.\n"
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
        "Use the following format strictly (no extra text):\n"
        "{"
        "  'signals': ["
        "    { 'id': '...', 'type': 'buy', 'symbol': '...', 'price': 0.0, 'timestamp': '...', 'confidence': '...', 'reason': '...' }"
        "  ],"
        "  'news': ["
        "    { 'id': '...', 'title': '...', 'summary': '...', 'content': '...', 'publishedAt': '...', 'source': '...', 'url': '...', 'tags': { 'sectors': [...], 'stocks': [...], 'sentiment': '...', 'impact': '...' } }"
        "  ]"
        "}\n"
        f"News: {news_list}"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    # You may need to parse the response content as JSON
    import json
    try:
        return json.loads(response.choices[0].message["content"])
    except Exception:
        return {"signals": [], "news": []} 