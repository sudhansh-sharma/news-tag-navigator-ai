import requests
from bs4 import BeautifulSoup
from django.utils.dateparse import parse_datetime
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)



def fetch_economic_times_news():
    HEADERS = {
        "sec-ch-ua": '"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"19.0.0"',
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
    }
    logger.info("Fetching Economic Times news...")
    try:
        resp = requests.get("https://economictimes.indiatimes.com/news/india", headers=HEADERS)
        resp.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to fetch Economic Times page: {e}")
        return []
    soup = BeautifulSoup(resp.text, 'html.parser')
    stories = soup.find_all('div', class_='eachStory')
    logger.info("Found %d stories on the page.", len(stories))
    news_list = []
    for story in stories:
        a = story.find('a')
        time_tag = story.find('time')
        p = story.find('p')
        title = a.get_text(strip=True) if a else ''
        link = a['href'] if a and a.has_attr('href') else ''
        dt_str = time_tag['datetime'] if time_tag and time_tag.has_attr('datetime') else ''
        dt = parse_datetime(dt_str) if dt_str else timezone.now()
        description = p.get_text(strip=True) if p else ''
        news_list.append({
            'title': title,
            'link': link,
            'datetime': dt,
            'description': description
        })
    logger.info("Returning %d parsed news stories.", len(news_list))
    return news_list