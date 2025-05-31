import yfinance as yf
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

def get_stock_price(symbol: str) -> Dict[str, float]:
    """Get current stock price and price change."""
    try:
        # Add .NS suffix for NSE stocks
        if not symbol.endswith('.NS'):
            symbol = f"{symbol}.NS"
            
        # Get stock info
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # Get historical data for price change
        hist = stock.history(period='5d')
        if len(hist) > 1:
            price_change = hist['Close'][-1] - hist['Close'][0]
            percent_change = (price_change / hist['Close'][0]) * 100
        else:
            price_change = 0
            percent_change = 0
            
        return {
            'current_price': info.get('currentPrice', 0),
            'price_change': price_change,
            'percent_change': percent_change
        }
    except Exception as e:
        logger.error(f"Error getting price for {symbol}: {e}")
        return {
            'current_price': 0,
            'price_change': 0,
            'percent_change': 0
        } 