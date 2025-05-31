from celery import shared_task
from ai.utils.openai_utils import analyze_news_with_gpt
from ai.utils.stock_universe import StockUniverse
from scrapy.models import NewsStory
from ai.models import Signal, AnalyzedNews
from ai.utils.yahoo_utils import get_stock_price
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Initialize stock universe for all tasks
stock_universe = StockUniverse()

@shared_task
def analyze_news_task(news_story_id):
    """
    Analyze a news story using GPT and save signals and analyzed news to the database.
    """
    try:
        news_story = NewsStory.objects.get(id=news_story_id)
        news_data = {
            "title": news_story.title,
            "description": news_story.description,
            "datetime": news_story.datetime.isoformat(),
            "source": getattr(news_story, 'source', ''),
            "link": news_story.link
        }
        result = analyze_news_with_gpt([news_data], stock_universe)

        # Save trading signals
        for signal in result.get("signals", []):
            symbol = signal.get("symbol")
            if not symbol:
                continue
            timestamp = signal.get("timestamp") or datetime.utcnow().isoformat()
            price_info = get_stock_price(symbol)
            price = price_info.get('current_price') if price_info else None
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

        # Save analyzed news
        for news in result.get("news", []):
            tags = news.get("tags", {})
            matched_stocks = tags.get("matched_stocks", [])
            stocks_with_prices = []
            for stock in matched_stocks:
                price_info = get_stock_price(stock["symbol"])
                price = price_info.get('current_price') if price_info else None
                if price is not None:
                    stocks_with_prices.append({
                        "symbol": stock["symbol"],
                        "price": price,
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
        