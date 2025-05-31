import pandas as pd
import chromadb
from chromadb.config import Settings
import logging
from typing import Dict, List, Optional, Tuple, Any
import os
from .stock_universe_chromadb_ingest import ingest_stock_universe
import time

logger = logging.getLogger(__name__)

class StockUniverse:
    def __init__(self, csv_path: str):
        """
        Initialize the stock universe from a CSV file.
        
        Args:
            csv_path: Path to the CSV file containing stock information
        """
        logger.info(f"Loading stock universe from {csv_path}")
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Stock universe CSV not found at {csv_path}")
        
        self.csv_path = csv_path
        self.stocks_df = pd.read_csv(csv_path)
        logger.info(f"Loaded {len(self.stocks_df)} stocks")
        self.stocks_df['CompanyName'] = self.stocks_df['CompanyName'].str.lower()
        self.stocks_df['Industry'] = self.stocks_df['Industry'].str.lower()
        
        # Initialize ChromaDB client
        self.client = None
        self.collection = None
        self._init_chromadb()
        
    def _init_chromadb(self, max_retries: int = 3, retry_delay: int = 5):
        """Initialize ChromaDB connection with retries."""
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
        
    def find_matching_stocks(self, company_names: List[str], industries: List[str] = None) -> List[Dict]:
        """
        Find matching stocks from the universe based on company names and industries.
        
        Args:
            company_names: List of company names to match
            industries: Optional list of industries to match
            
        Returns:
            List of dictionaries containing matched stock information
        """
        matches = []
        company_names = [name.lower() for name in company_names]
        logger.info(f"Searching for companies: {company_names}")
        
        # Debug: Print all available company names
        logger.info("Available company names in universe:")
        for name in self.stocks_df['CompanyName'].unique():
            logger.info(f"- {name}")
        
        # Match by company name
        for name in company_names:
            logger.info(f"\nSearching for company: {name}")
            # Remove common suffixes and words
            clean_name = name.replace('limited', '').replace('ltd', '').replace('inc', '').replace('corporation', '').replace('corp', '').strip()
            logger.info(f"Cleaned company name: {clean_name}")
            
            # Debug: Try exact match first
            exact_matches = self.stocks_df[self.stocks_df['CompanyName'] == clean_name]
            if not exact_matches.empty:
                logger.info(f"Found exact match for {clean_name}")
                for _, row in exact_matches.iterrows():
                    match = {
                        'symbol': row['Symbol'],
                        'company_name': row['CompanyName'],
                        'industry': row['Industry'],
                        'isin': row['ISIN Code'],
                        'series': row['Series']
                    }
                    logger.info(f"Exact match: {match}")
                    matches.append(match)
                continue
            
            # Try partial match
            logger.info("No exact match, trying partial match...")
            name_matches = self.stocks_df[
                self.stocks_df['CompanyName'].str.contains(clean_name, case=False, na=False)
            ]
            
            if not name_matches.empty:
                logger.info(f"Found {len(name_matches)} partial matches for {clean_name}")
                for _, row in name_matches.iterrows():
                    match = {
                        'symbol': row['Symbol'],
                        'company_name': row['CompanyName'],
                        'industry': row['Industry'],
                        'isin': row['ISIN Code'],
                        'series': row['Series']
                    }
                    logger.info(f"Partial match: {match}")
                    matches.append(match)
            else:
                logger.info(f"No matches found for {clean_name}")
                # Debug: Show closest matches
                logger.info("Closest matches in universe:")
                for universe_name in self.stocks_df['CompanyName'].unique():
                    if clean_name in universe_name or universe_name in clean_name:
                        logger.info(f"- {universe_name}")
        
        # If industries provided, filter matches by industry
        if industries:
            industries = [ind.lower() for ind in industries]
            logger.info(f"Filtering by industries: {industries}")
            matches = [
                match for match in matches 
                if any(ind in match['industry'].lower() for ind in industries)
            ]
            logger.info(f"After industry filtering: {len(matches)} matches")
            
        return matches
    
    def get_stock_info(self, symbol: str) -> Optional[Dict]:
        """
        Get information for a specific stock symbol.
        
        Args:
            symbol: Stock symbol to look up
            
        Returns:
            Dictionary containing stock information or None if not found
        """
        logger.info(f"Looking up stock info for symbol: {symbol}")
        
        # Remove .NS suffix if present
        clean_symbol = symbol.replace('.NS', '')
        logger.info(f"Cleaned symbol: {clean_symbol}")
        
        match = self.stocks_df[self.stocks_df['Symbol'] == clean_symbol]
        if not match.empty:
            row = match.iloc[0]
            info = {
                'symbol': row['Symbol'],
                'company_name': row['CompanyName'],
                'industry': row['Industry'],
                'isin': row['ISIN Code'],
                'series': row['Series']
            }
            logger.info(f"Found stock info: {info}")
            return info
        logger.info(f"No stock info found for symbol: {clean_symbol}")
        return None 

    def get_relevant_stocks(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Get relevant stocks based on query text using ChromaDB."""
        if not self.collection:
            logger.warning("ChromaDB collection not available, falling back to full stock list")
            return self.stocks_df.to_dict('records')
            
        try:
            # Query ChromaDB
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            
            # Extract metadata from results
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
            return self.stocks_df.to_dict('records')
    
    def get_stock_by_symbol(self, symbol: str) -> Dict[str, Any]:
        """Get stock information by symbol."""
        stock = self.stocks_df[self.stocks_df['Symbol'] == symbol]
        if not stock.empty:
            return stock.iloc[0].to_dict()
        return None 