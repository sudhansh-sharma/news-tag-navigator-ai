from django.db import models
from scrapy.models import NewsStory

# Create your models here.

class Signal(models.Model):
    SIGNAL_TYPES = (('buy', 'Buy'), ('sell', 'Sell'), ('entry', 'Entry'))
    news_story = models.ForeignKey(NewsStory, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=SIGNAL_TYPES)
    symbol = models.CharField(max_length=10)
    price = models.FloatField()
    timestamp = models.DateTimeField()
    confidence = models.CharField(max_length=20)
    reason = models.TextField()

class AnalyzedNews(models.Model):
    news_story = models.ForeignKey(NewsStory, on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    summary = models.TextField()
    content = models.TextField()
    published_at = models.DateTimeField()
    source = models.CharField(max_length=100)
    url = models.URLField()
    tags = models.JSONField()
