import os
import pandas as pd
import chromadb
import logging
import time
import sys

logger = logging.getLogger(__name__)

def wait_for_chromadb(max_retries: int = 30, retry_delay: int = 2) -> bool:
    """Wait for ChromaDB to be ready."""
    for attempt in range(max_retries):
        try:
            client = chromadb.HttpClient(
                host=os.getenv('CHROMA_SERVER_HOST', 'chromadb'),
                port=int(os.getenv('CHROMA_SERVER_PORT', 8000))
            )
            # Try a simple operation
            client.list_collections()
            logger.info("ChromaDB is ready")
            return True
        except Exception as e:
            logger.info(f"Waiting for ChromaDB to be ready (attempt {attempt + 1}/{max_retries})")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
    
    logger.error("ChromaDB failed to become ready")
    return False

def warmup_chromadb_model():
    """Trigger a dummy semantic query to force the model download and cache."""
    try:
        client = chromadb.HttpClient(
            host=os.getenv('CHROMA_SERVER_HOST', 'chromadb'),
            port=int(os.getenv('CHROMA_SERVER_PORT', 8000))
        )
        collection = client.get_collection("stock_universe")
        # Dummy query to trigger model download
        collection.query(query_texts=["warmup"], n_results=1)
        logger.info("ChromaDB model warmup query completed.")
    except Exception as e:
        logger.warning(f"ChromaDB warmup query failed: {e}")

def ingest_stock_universe() -> bool:
    """
    Ingest stock universe data into ChromaDB.
    Only creates the database if it doesn't exist.
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Wait for ChromaDB to be ready
    if not wait_for_chromadb():
        return False
        
    try:
        # Get ChromaDB client
        client = chromadb.HttpClient(
            host=os.getenv('CHROMA_SERVER_HOST', 'chromadb'),
            port=int(os.getenv('CHROMA_SERVER_PORT', 8000))
        )
        
        # Check if collection exists
        collections = client.list_collections()
        if any(c.name == "stock_universe" for c in collections):
            logger.info("Stock universe collection already exists")
            warmup_chromadb_model()
            return True
            
        # Read stock universe CSV
        csv_path = os.path.join(os.getenv('APP_DATA_DIR', '/app/data'), 'stock_universe.csv')
        logger.info(f"Reading stock universe from {csv_path}")
        if not os.path.exists(csv_path):
            logger.error(f"Stock universe CSV not found at {csv_path}")
            return False
            
        df = pd.read_csv(csv_path)
        
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
        warmup_chromadb_model()
        return True
        
    except Exception as e:
        logger.error(f"Error ingesting stock universe: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )
    
    # Run ingestion
    success = ingest_stock_universe()
    sys.exit(0 if success else 1) 