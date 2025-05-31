import os
import sys
import logging
import shutil
import yfinance as yf
from datetime import datetime, timedelta
from ai.stock_universe import StockUniverse
from ai.openai_utils import analyze_news_with_gpt

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_test_environment():
    """Set up test environment with necessary data."""
    # Create test data directory
    os.makedirs('test_data', exist_ok=True)
    
    # Copy stock universe CSV to test data directory
    if not os.path.exists('test_data/stock_universe.csv'):
        shutil.copy('data/stock_universe.csv', 'test_data/stock_universe.csv')
    
    # Initialize ChromaDB in test mode
    from ai.stock_universe_chromadb_ingest import ingest_stock_universe
    if not ingest_stock_universe(test_mode=True):
        logger.error("Failed to initialize ChromaDB in test mode")
        return False
    return True

def get_stock_price(symbol: str) -> dict:
    """Get current stock price and recent price history."""
    try:
        # Add .NS suffix for NSE stocks if not present
        if not symbol.endswith('.NS'):
            symbol = f"{symbol}.NS"
            
        stock = yf.Ticker(symbol)
        
        # Get current price
        current_price = stock.info.get('regularMarketPrice', None)
        
        # Get historical data for last 5 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5)
        hist = stock.history(start=start_date, end=end_date)
        
        # Calculate price change
        if not hist.empty:
            price_change = hist['Close'].iloc[-1] - hist['Close'].iloc[0]
            price_change_pct = (price_change / hist['Close'].iloc[0]) * 100
        else:
            price_change = None
            price_change_pct = None
            
        return {
            'symbol': symbol,
            'current_price': current_price,
            'price_change': price_change,
            'price_change_pct': price_change_pct,
            'last_updated': datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching price for {symbol}: {e}")
        return {
            'symbol': symbol,
            'error': str(e)
        }

def test_news_analysis():
    """Test news analysis functionality."""
    logger.info("Setting up test environment...")
    if not setup_test_environment():
        return
    
    logger.info("Loading stock universe...")
    stock_universe = StockUniverse('test_data/stock_universe.csv', test_mode=True)
    
    # Test news items
    test_news = [
        {
            'title': 'Reliance Industries announces Q4 results with 15% profit growth',
            'description': 'Reliance Industries reported a 15% increase in quarterly profits, driven by strong performance in retail and digital services.',
            'datetime': datetime.utcnow().isoformat(),
            'source': 'Economic Times',
            'link': 'https://example.com/news1'
        },
        {
            'title': 'TCS wins major IT contract from European bank',
            'description': 'Tata Consultancy Services has secured a $500 million contract from a leading European bank for digital transformation services.',
            'datetime': datetime.utcnow().isoformat(),
            'source': 'Business Standard',
            'link': 'https://example.com/news2'
        }
    ]
    
    logger.info("Analyzing news...")
    result = analyze_news_with_gpt(test_news, stock_universe)
    
    # Print analysis results
    logger.info("\nAnalysis Results:")
    logger.info("=" * 50)
    
    # Print signals
    logger.info("\nTrading Signals:")
    for signal in result['signals']:
        logger.info(f"\nSignal for {signal['symbol']}:")
        logger.info(f"Type: {signal['type']}")
        logger.info(f"Confidence: {signal['confidence']}")
        logger.info(f"Reason: {signal['reason']}")
        
        # Get and print price information
        price_info = get_stock_price(signal['symbol'])
        logger.info("\nPrice Information:")
        if 'error' in price_info:
            logger.info(f"Error: {price_info['error']}")
        else:
            logger.info(f"Current Price: ₹{price_info['current_price']:.2f}")
            if price_info['price_change'] is not None:
                logger.info(f"5-day Change: ₹{price_info['price_change']:.2f} ({price_info['price_change_pct']:.2f}%)")
    
    # Print news analysis
    logger.info("\nNews Analysis:")
    for news in result['news']:
        logger.info(f"\nTitle: {news['title']}")
        logger.info(f"Summary: {news['summary']}")
        logger.info(f"Sentiment: {news['tags']['sentiment']}")
        logger.info(f"Impact: {news['tags']['impact']}")
        logger.info("\nMatched Stocks:")
        for stock in news['tags']['matched_stocks']:
            logger.info(f"- {stock['symbol']}: {stock['company_name']}")
            
            # Get and print price information for matched stocks
            price_info = get_stock_price(stock['symbol'])
            if 'error' in price_info:
                logger.info(f"  Price Error: {price_info['error']}")
            else:
                logger.info(f"  Current Price: ₹{price_info['current_price']:.2f}")
                if price_info['price_change'] is not None:
                    logger.info(f"  5-day Change: ₹{price_info['price_change']:.2f} ({price_info['price_change_pct']:.2f}%)")
        
        logger.info("\nKey Points:")
        for point in news['tags']['key_points']:
            logger.info(f"- {point}")
        
        if news['tags']['financial_metrics']:
            logger.info("\nFinancial Metrics:")
            for metric, value in news['tags']['financial_metrics'].items():
                if value:
                    logger.info(f"- {metric}: {value}")

if __name__ == "__main__":
    try:
        test_news_analysis()
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
    finally:
        # Clean up test data
        if os.path.exists('test_data'):
            shutil.rmtree('test_data') 