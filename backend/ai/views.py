from django.shortcuts import render
from rest_framework import viewsets
from .models import Signal, AnalyzedNews
from .serializers import SignalSerializer, AnalyzedNewsSerializer

# Create your views here.

class SignalViewSet(viewsets.ModelViewSet):
    queryset = Signal.objects.all().order_by('-timestamp')
    serializer_class = SignalSerializer

class AnalyzedNewsViewSet(viewsets.ModelViewSet):
    queryset = AnalyzedNews.objects.all().order_by('-published_at')
    serializer_class = AnalyzedNewsSerializer
