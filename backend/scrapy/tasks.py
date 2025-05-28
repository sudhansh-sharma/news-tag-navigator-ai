from celery import shared_task
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from scrapy.models import NewsStory
from django.core.cache import cache
from scrapy.economictimes import fetch_economic_times_news
from ai.tasks import analyze_news_task
import logging

logger = logging.getLogger(__name__)

REDIS_KEY = "et_latest_timestamp"

@shared_task
def scrape_economic_times():
    logger.info("Starting Economic Times scraping task.")
    last_timestamp = cache.get(REDIS_KEY)
    if last_timestamp:
        last_timestamp = parse_datetime(last_timestamp)
        logger.info(f"Last timestamp from cache: {last_timestamp}")
    else:
        last_timestamp = timezone.make_aware(timezone.datetime.min)
        logger.info("No last timestamp found, using minimum datetime.")

    try:
        news_list = fetch_economic_times_news()
        logger.info(f"Fetched {len(news_list)} stories from Economic Times.")
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return

    new_latest = last_timestamp
    new_count = 0
    for news in news_list:
        dt = news['datetime']
        if dt > last_timestamp:
            news_story, created = NewsStory.objects.update_or_create(
                link=news['link'],
                defaults={
                    'title': news['title'],
                    'datetime': dt,
                    'description': news['description']
                }
            )
            new_count += 1
            if created:
                analyze_news_task.delay(news_story.id)
            if dt > new_latest:
                new_latest = dt
    if new_latest > last_timestamp:
        cache.set(REDIS_KEY, new_latest.isoformat())
        logger.info(f"Updated latest timestamp in cache: {new_latest}")
    logger.info(f"Scraping task complete. {new_count} new stories saved.") 