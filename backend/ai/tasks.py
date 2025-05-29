from celery import shared_task
from .openai_utils import analyze_news_with_gpt
from .stock_universe import StockUniverse
from scrapy.models import NewsStory
from .models import Signal, AnalyzedNews
from .yahoo_utils import get_latest_price
import os

# Initialize stock universe
STOCK_UNIVERSE_CSV = os.environ.get('STOCK_UNIVERSE_CSV', 'data/stock_universe.csv')
stock_universe = StockUniverse(STOCK_UNIVERSE_CSV)

@shared_task
def analyze_news_task(news_story_id):
    news_story = NewsStory.objects.get(id=news_story_id)
    news_data = {
        "title": news_story.title,
        "summary": getattr(news_story, 'summary', news_story.description),
        "content": news_story.description,
        "publishedAt": news_story.datetime.isoformat(),
        "source": getattr(news_story, 'source', ''),
        "url": news_story.link,
        "tags": {},
    }
    
    # Analyze news with GPT and map to stock universe
    result = analyze_news_with_gpt([news_data], stock_universe)
    
    # Process signals
    for signal in result.get("signals", []):
        symbol = signal.get("symbol")
        price = get_latest_price(symbol) if symbol else None
        Signal.objects.create(
            news_story=news_story,
            type=signal.get("type"),
            symbol=symbol,
            price=price,
            timestamp=signal.get("timestamp"),
            confidence=signal.get("confidence"),
            reason=signal.get("reason"),
        )
    
    # Process analyzed news
    for news in result.get("news", []):
        tags = news.get("tags", {})
        stocks = tags.get("stocks", [])
        matched_stocks = tags.get("matched_stocks", [])
        
        # Enrich each stock with its price
        stocks_with_prices = []
        for stock in matched_stocks:
            stock_price = get_latest_price(stock["symbol"])
            stocks_with_prices.append({
                "symbol": stock["symbol"],
                "price": stock_price,
                "company_name": stock["company_name"],
                "industry": stock["industry"],
                "isin": stock["isin"],
                "series": stock["series"]
            })
        
        tags["stocks"] = stocks_with_prices
        AnalyzedNews.objects.create(
            news_story=news_story,
            title=news.get("title"),
            summary=news.get("summary"),
            content=news.get("content"),
            published_at=news.get("publishedAt"),
            source=news.get("source"),
            url=news.get("url"),
            tags=tags,
        )
        