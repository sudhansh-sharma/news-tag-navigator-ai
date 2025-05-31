import chromadb
import logging
import os
import time
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class StockUniverse:
    def __init__(self):
        self.client = None
        self.collection = None
        self._connect_chromadb()

    def _connect_chromadb(self, max_retries: int = 3, retry_delay: int = 5):
        """
        Connect to the running ChromaDB server and get the stock_universe collection.
        This does NOT initialize or ingest data into ChromaDB; it only connects as a client.
        """
        for attempt in range(max_retries):
            try:
                self.client = chromadb.HttpClient(
                    host=os.getenv('CHROMA_SERVER_HOST', 'chromadb'),
                    port=int(os.getenv('CHROMA_SERVER_PORT', 8000))
                )
                self.collection = self.client.get_collection("stock_universe")
                logger.info("Successfully connected to ChromaDB collection")
                return
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1}/{max_retries} failed to connect to ChromaDB: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
        logger.error("Failed to connect to ChromaDB after all retries")
        self.client = None
        self.collection = None

    def get_relevant_stocks(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Query the ChromaDB server for relevant stocks based on query text."""
        if not self.collection:
            logger.error("ChromaDB collection not available.")
            return []
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            relevant_stocks = []
            for metadata in results['metadatas'][0]:
                relevant_stocks.append({
                    'Symbol': metadata['symbol'],
                    'CompanyName': metadata['company_name'],
                    'Industry': metadata['industry']
                })
            return relevant_stocks
        except Exception as e:
            logger.error(f"Error querying ChromaDB: {e}", exc_info=True)
            return []

    def get_stock_by_symbol(self, symbol: str) -> Dict[str, Any]:
        """Get stock information by symbol."""
        if not self.collection:
            logger.error("ChromaDB collection not available.")
            return None
        try:
            results = self.collection.query(
                query_texts=[symbol],
                n_results=1
            )
            if len(results['metadatas']) > 0 and len(results['metadatas'][0]) > 0:
                metadata = results['metadatas'][0][0]
                return {
                    'Symbol': metadata['symbol'],
                    'CompanyName': metadata['company_name'],
                    'Industry': metadata['industry']
                }
            return None
        except Exception as e:
            logger.error(f"Error querying ChromaDB: {e}", exc_info=True)
            return None 