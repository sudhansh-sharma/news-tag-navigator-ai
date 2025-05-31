from celery import shared_task
from .openai_utils import analyze_news_with_gpt
from .stock_universe import StockUniverse
from scrapy.models import NewsStory
from .models import Signal, AnalyzedNews
from .yahoo_utils import get_latest_price
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Initialize stock universe
STOCK_UNIVERSE_CSV = os.environ.get('STOCK_UNIVERSE_CSV', 'data/stock_universe.csv')
stock_universe = StockUniverse(STOCK_UNIVERSE_CSV)

@shared_task
def analyze_news_task(news_story_id):
    """Analyze a news story using GPT and save signals and analyzed news to the database."""
    try:
        news_story = NewsStory.objects.get(id=news_story_id)
        
        # Convert NewsStory to dict format for GPT analysis
        news_data = {
            "title": news_story.title,
            "description": news_story.description,
            "datetime": news_story.datetime.isoformat(),
            "source": getattr(news_story, 'source', ''),
            "link": news_story.link
        }
        
        # Analyze news with GPT and map to stock universe
        result = analyze_news_with_gpt([news_data], stock_universe)
        
        # Process signals
        for signal in result.get("signals", []):
            symbol = signal.get("symbol")
            if not symbol:
                continue
                
            # Get current timestamp if not provided
            timestamp = signal.get("timestamp") or datetime.utcnow().isoformat()
            
            # Fetch price from Yahoo Finance
            price = get_latest_price(symbol)
            if price is None:
                continue
                
            Signal.objects.create(
                news_story=news_story,
                type=signal.get("type"),
                symbol=symbol,
                price=price,
                timestamp=timestamp,
                confidence=signal.get("confidence"),
                reason=signal.get("reason"),
            )
        
        # Process analyzed news
        for news in result.get("news", []):
            tags = news.get("tags", {})
            matched_stocks = tags.get("matched_stocks", [])
            
            # Enrich each stock with its price
            stocks_with_prices = []
            for stock in matched_stocks:
                stock_price = get_latest_price(stock["symbol"])
                if stock_price is not None:
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
                
    except NewsStory.DoesNotExist:
        logger.error(f"News story with ID {news_story_id} not found")
    except Exception as e:
        logger.error(f"Error in analyze_news_task: {e}")
        