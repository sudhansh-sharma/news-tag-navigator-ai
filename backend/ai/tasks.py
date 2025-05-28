from celery import shared_task
from .openai_utils import analyze_news_with_gpt
from scrapy.models import NewsStory
from .models import Signal, AnalyzedNews

@shared_task
def analyze_news_task(news_story_id):
    news_story = NewsStory.objects.get(id=news_story_id)
    news_data = {
        "title": news_story.title,
        "description": news_story.description,
        "datetime": news_story.datetime.isoformat(),
        "link": news_story.link,
    }
    result = analyze_news_with_gpt([news_data])
    for signal in result.get("signals", []):
        Signal.objects.create(
            news_story=news_story,
            type=signal["type"],
            symbol=signal["symbol"],
            price=signal["price"],
            timestamp=signal["timestamp"],
            confidence=signal["confidence"],
            reason=signal["reason"],
        )
    for news in result.get("news", []):
        AnalyzedNews.objects.create(
            news_story=news_story,
            title=news["title"],
            summary=news["summary"],
            content=news["content"],
            published_at=news["publishedAt"],
            source=news["source"],
            url=news["url"],
            tags=news["tags"],
        )
        