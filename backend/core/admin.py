from django.contrib import admin
from .models import NewsStory, ScheduledTask

admin.site.register(NewsStory)
admin.site.register(ScheduledTask) 