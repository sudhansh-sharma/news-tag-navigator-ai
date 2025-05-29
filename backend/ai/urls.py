from rest_framework.routers import DefaultRouter
from .views import SignalViewSet, AnalyzedNewsViewSet

router = DefaultRouter()
router.register(r'signals', SignalViewSet)
router.register(r'analyzed-news', AnalyzedNewsViewSet)

urlpatterns = router.urls 