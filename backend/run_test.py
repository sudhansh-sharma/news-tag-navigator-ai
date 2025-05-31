import logging
import os
import sys
from ai.stock_universe import StockUniverse
from ai.news_analyzer import NewsAnalyzer
from ai.utils.yahoo_utils import get_stock_price

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Run test analysis on sample news."""
    # Sample news text
    news_text = """
    Reliance Industries Ltd. reported strong Q3 results with 15% revenue growth.
    The company's digital services segment showed robust performance.
    Meanwhile, TCS announced a new partnership with Microsoft for cloud services.
    In the banking sector, HDFC Bank's net profit rose by 20% in the latest quarter.
    """
    
    # Initialize components
    csv_path = os.path.join(os.getenv('APP_DATA_DIR', 'data'), 'stock_universe.csv')
    if not os.path.exists(csv_path):
        logger.error(f"Stock universe CSV not found at {csv_path}")
        sys.exit(1)
        
    universe = StockUniverse(csv_path)
    analyzer = NewsAnalyzer()
    
    # Get trading signals
    logger.info("\n=== Trading Signals ===")
    signals = analyzer.get_trading_signals(news_text)
    for signal in signals:
        price_info = get_stock_price(signal['symbol'])
        logger.info(f"\nSignal: {signal['signal']}")
        logger.info(f"Company: {signal['company_name']}")
        logger.info(f"Symbol: {signal['symbol']}")
        logger.info(f"Current Price: ₹{price_info['current_price']:.2f}")
        logger.info(f"5-day Change: ₹{price_info['price_change']:.2f} ({price_info['percent_change']:.1f}%)")
        logger.info(f"Confidence: {signal['confidence']:.2f}")
        logger.info(f"Explanation: {signal['explanation']}")
    
    # Get news analysis
    logger.info("\n=== News Analysis ===")
    analysis = analyzer.analyze_news(news_text)
    
    # Print key points
    logger.info("\nKey Points:")
    for point in analysis['key_points']:
        logger.info(f"- {point}")
    
    # Print matched stocks with prices
    logger.info("\nMatched Stocks:")
    for stock in analysis['matched_stocks']:
        price_info = get_stock_price(stock['symbol'])
        logger.info(f"\nCompany: {stock['company_name']}")
        logger.info(f"Symbol: {stock['symbol']}")
        logger.info(f"Current Price: ₹{price_info['current_price']:.2f}")
        logger.info(f"5-day Change: ₹{price_info['price_change']:.2f} ({price_info['percent_change']:.1f}%)")
        logger.info(f"Relevance: {stock['relevance']:.2f}")
    
    # Print financial metrics
    logger.info("\nFinancial Metrics:")
    for metric in analysis['financial_metrics']:
        logger.info(f"- {metric}")

if __name__ == "__main__":
    main() 