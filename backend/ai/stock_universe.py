import pandas as pd
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

class StockUniverse:
    def __init__(self, csv_path: str):
        """
        Initialize the stock universe from a CSV file.
        
        Args:
            csv_path: Path to the CSV file containing stock information
        """
        self.stocks_df = pd.read_csv(csv_path)
        self.stocks_df['CompanyName'] = self.stocks_df['CompanyName'].str.lower()
        self.stocks_df['Industry'] = self.stocks_df['Industry'].str.lower()
        
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
        
        # Match by company name
        for name in company_names:
            name_matches = self.stocks_df[
                self.stocks_df['CompanyName'].str.contains(name, case=False, na=False)
            ]
            
            if not name_matches.empty:
                for _, row in name_matches.iterrows():
                    matches.append({
                        'symbol': row['Symbol'],
                        'company_name': row['CompanyName'],
                        'industry': row['Industry'],
                        'isin': row['ISIN Code'],
                        'series': row['Series']
                    })
        
        # If industries provided, filter matches by industry
        if industries:
            industries = [ind.lower() for ind in industries]
            matches = [
                match for match in matches 
                if any(ind in match['industry'].lower() for ind in industries)
            ]
            
        return matches
    
    def get_stock_info(self, symbol: str) -> Optional[Dict]:
        """
        Get information for a specific stock symbol.
        
        Args:
            symbol: Stock symbol to look up
            
        Returns:
            Dictionary containing stock information or None if not found
        """
        match = self.stocks_df[self.stocks_df['Symbol'] == symbol]
        if not match.empty:
            row = match.iloc[0]
            return {
                'symbol': row['Symbol'],
                'company_name': row['CompanyName'],
                'industry': row['Industry'],
                'isin': row['ISIN Code'],
                'series': row['Series']
            }
        return None 