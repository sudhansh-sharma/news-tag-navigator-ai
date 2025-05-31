import os
import pandas as pd
import chromadb
from chromadb.config import Settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def get_chroma_paths(test_mode: bool = False) -> tuple[str, str]:
    """Get paths for CSV and ChromaDB based on mode."""
    if test_mode:
        return 'test_data/stock_universe.csv', 'test_data/chroma_stock_universe'
    # Use shared volume path for production
    return '/shared_data/stock_universe.csv', '/shared_data/chroma_stock_universe'

def ingest_stock_universe(test_mode: bool = False) -> bool:
    """
    Ingest stock universe data into ChromaDB.
    Only creates the database if it doesn't exist.
    
    Args:
        test_mode: Whether to use test data paths
        
    Returns:
        bool: True if successful, False otherwise
    """
    csv_path, chroma_path = get_chroma_paths(test_mode)
    
    # Check if ChromaDB already exists
    if os.path.exists(chroma_path):
        logger.info(f"ChromaDB already exists at {chroma_path}")
        return True
        
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(chroma_path), exist_ok=True)
        
        # Read stock universe CSV
        logger.info(f"Reading stock universe from {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Initialize ChromaDB
        logger.info(f"Initializing ChromaDB at {chroma_path}")
        client = chromadb.Client(Settings(persist_directory=chroma_path))
        
        # Create collection
        collection = client.create_collection(
            name="stock_universe",
            metadata={"description": "Stock universe data for semantic search"}
        )
        
        # Prepare documents and metadata
        documents = []
        metadatas = []
        ids = []
        
        for _, row in df.iterrows():
            # Create document text from relevant fields
            doc_text = f"{row['CompanyName']} {row['Industry']} {row['Symbol']}"
            
            # Create metadata
            metadata = {
                "symbol": row['Symbol'],
                "company_name": row['CompanyName'],
                "industry": row['Industry'],
                "isin": row['ISIN Code'],
                "series": row['Series']
            }
            
            documents.append(doc_text)
            metadatas.append(metadata)
            ids.append(row['Symbol'])
        
        # Add documents to collection
        logger.info(f"Adding {len(documents)} documents to ChromaDB")
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info("Successfully ingested stock universe into ChromaDB")
        return True
        
    except Exception as e:
        logger.error(f"Error ingesting stock universe: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    ingest_stock_universe() 