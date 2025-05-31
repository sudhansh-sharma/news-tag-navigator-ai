import logging
from ai.stock_universe_chromadb_ingest import ingest_stock_universe, get_chroma_paths
import os

logger = logging.getLogger(__name__)

def initialize_ai(test_mode: bool = False) -> bool:
    """
    Initialize AI components.
    Only creates ChromaDB if it doesn't exist.
    
    Args:
        test_mode: Whether to run in test mode
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info("Initializing AI components...")
    
    # Check if ChromaDB needs to be created
    _, chroma_path = get_chroma_paths(test_mode)
    if not os.path.exists(chroma_path):
        logger.info("ChromaDB not found, creating new database...")
        if not ingest_stock_universe(test_mode=test_mode):
            logger.error("Failed to create ChromaDB")
            return False
        logger.info("Successfully created ChromaDB")
    else:
        logger.info("ChromaDB already exists, skipping creation")
    
    return True
