import os
from django.core.wsgi import get_wsgi_application
import logging

logging.getLogger("grpc").setLevel(logging.WARNING)
logging.getLogger("grpc._cython.cygrpc").setLevel(logging.WARNING)
logging.getLogger("chromadb.telemetry").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
 
application = get_wsgi_application() 