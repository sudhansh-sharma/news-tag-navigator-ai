import os
from openai_utils import analyze_news_with_gpt
from stock_universe import StockUniverse

def test_news_analysis():
    # Initialize stock universe
    stock_universe = StockUniverse('data/stock_universe.csv')
    
    # Test news articles
    test_news = [
        {
            "title": "Reliance Industries Reports Strong Q4 Results",
            "summary": "Reliance Industries Limited reported better-than-expected quarterly results driven by strong performance in its oil & gas and retail segments.",
            "content": "Reliance Industries Limited (RIL) has reported a significant increase in its quarterly profits, exceeding market expectations. The company's oil & gas segment showed robust growth, while its retail business continued to expand rapidly. The strong performance was attributed to improved operational efficiency and higher margins across businesses.",
            "publishedAt": "2024-03-21T10:00:00Z",
            "source": "Economic Times",
            "url": "https://example.com/news/1",
            "tags": {}
        },
        {
            "title": "TCS and Infosys Announce Major AI Partnership",
            "summary": "Tata Consultancy Services and Infosys have joined forces to develop advanced AI solutions for the banking sector.",
            "content": "In a significant development for the Indian IT sector, Tata Consultancy Services (TCS) and Infosys have announced a strategic partnership to develop cutting-edge artificial intelligence solutions. The collaboration will focus on creating AI-powered banking solutions, with initial projects targeting HDFC Bank and ICICI Bank.",
            "publishedAt": "2024-03-21T11:00:00Z",
            "source": "Business Standard",
            "url": "https://example.com/news/2",
            "tags": {}
        }
    ]
    
    # Analyze news
    result = analyze_news_with_gpt(test_news, stock_universe)
    
    # Print results
    print("\nAnalyzed News:")
    for news in result.get("news", []):
        print(f"\nTitle: {news['title']}")
        print(f"Summary: {news['summary']}")
        print("\nMatched Stocks:")
        for stock in news.get("tags", {}).get("matched_stocks", []):
            print(f"- {stock['company_name']} ({stock['symbol']})")
        print(f"Sentiment: {news['tags'].get('sentiment')}")
        print(f"Impact: {news['tags'].get('impact')}")
    
    print("\nTrading Signals:")
    for signal in result.get("signals", []):
        print(f"\nType: {signal['type']}")
        print(f"Symbol: {signal['symbol']}")
        print(f"Confidence: {signal['confidence']}")
        print(f"Reason: {signal['reason']}")

if __name__ == "__main__":
    # Ensure OPENAI_API_KEY is set
    if not os.environ.get("OPENAI_API_KEY"):
        print("Please set OPENAI_API_KEY environment variable")
        exit(1)
    
    test_news_analysis() 