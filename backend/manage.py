#!/usr/bin/env python
import os
import sys
import logging

logging.getLogger("grpc").setLevel(logging.WARNING)
logging.getLogger("grpc._cython.cygrpc").setLevel(logging.WARNING)
logging.getLogger("chromadb.telemetry").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main() 