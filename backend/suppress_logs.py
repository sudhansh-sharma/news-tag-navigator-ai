import logging
logging.getLogger("grpc").setLevel(logging.WARNING)
logging.getLogger("grpc._cython.cygrpc").setLevel(logging.WARNING)
logging.getLogger("chromadb.telemetry").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING) 