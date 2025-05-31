from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)


class AiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai'

    def ready(self):
        """Initialize AI components only when running the server."""
        import sys
        # Skip initialization during migrations
        if 'migrate' in sys.argv or 'makemigrations' in sys.argv or 'collectstatic' in sys.argv:
            return
            
        try:
            from . import initialize_ai
            initialize_ai()
        except Exception as e:
            logger.error(f"Error initializing AI components: {e}")
