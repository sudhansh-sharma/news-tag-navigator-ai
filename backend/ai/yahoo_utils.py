import yfinance as yf
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def get_latest_price(symbol: str) -> Optional[float]:
    """
    Returns the last traded price or latest closing price for a given NSE symbol.
    Appends '.NS' to the symbol for NSE stocks if not already present.
    Returns None if price cannot be fetched or symbol is empty.
    
    Args:
        symbol: Stock symbol to fetch price for
        
    Returns:
        Latest price as float or None if price cannot be fetched
    """
    if not symbol or not isinstance(symbol, str):
        logger.warning(f"Invalid symbol provided: {symbol}")
        return None
        
    if not symbol.endswith('.NS'):
        symbol = f"{symbol}.NS"
        
    try:
        logger.info(f"Fetching price for {symbol}")
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        
        if not data.empty:
            price = float(data['Close'].iloc[-1])
            logger.info(f"Successfully fetched price for {symbol}: {price}")
            return price
        else:
            logger.warning(f"No price data available for {symbol}")
            return None
            
    except Exception as e:
        logger.error(f"Error fetching price for {symbol}: {e}")
        return None