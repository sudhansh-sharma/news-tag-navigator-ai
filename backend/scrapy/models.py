from django.db import models

class NewsStory(models.Model):
    title = models.CharField(max_length=500)
    link = models.URLField(unique=True)
    datetime = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return self.title 