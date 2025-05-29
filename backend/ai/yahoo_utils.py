import yfinance as yf
import logging

logger = logging.getLogger(__name__)

def get_latest_price(symbol):
    """
    Returns the last traded price or latest closing price for a given NSE symbol.
    Appends '.NS' to the symbol for NSE stocks if not already present.
    Returns None if price cannot be fetched or symbol is empty.
    """
    if not symbol or not isinstance(symbol, str):
        return -1
    if not symbol.endswith('.NS'):
        symbol = f"{symbol}.NS"
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if not data.empty:
            return float(data['Close'].iloc[-1])
    except Exception as e:
        logger.error(f"Error fetching price for {symbol}: {e}")
        return -1
    return -1