from django.contrib import admin
from .models import Signal, AnalyzedNews

# Register your models here.
admin.site.register(Signal)
admin.site.register(AnalyzedNews)
