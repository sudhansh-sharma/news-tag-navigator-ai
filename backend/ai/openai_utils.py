import os
import json
import logging
from typing import List, Dict, Any
from openai import OpenAI
from ai.stock_universe import StockUniverse
from datetime import datetime

logger = logging.getLogger(__name__)

def get_gpt_response(prompt: str) -> str:
    """Get response from GPT-4 model."""
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
        
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=2000  # Limit response size
    )
    return response.choices[0].message.content

def analyze_news_with_gpt(news_items: List[Dict], stock_universe: StockUniverse) -> Dict[str, Any]:
    """Analyze news items using GPT and map companies to stocks in the universe."""
    # Format news items for GPT analysis
    news_text = "\n\n".join([
        f"Title: {item.get('title', '')}\n"
        f"Description: {item.get('description', '')}\n"
        f"Published: {item.get('datetime', datetime.utcnow().isoformat())}\n"
        f"Source: {item.get('source', 'News Source')}\n"
        f"URL: {item.get('link', '')}"
        for item in news_items
    ])
    
    # Get relevant stocks using ChromaDB
    relevant_stocks = stock_universe.get_relevant_stocks(news_text, n_results=5)  # Reduced from 10 to 5
    
    # Format stock data more concisely
    stock_list = [f"{s['Symbol']}: {s['CompanyName']}" for s in relevant_stocks]  # Removed industry to save tokens
    stock_universe_text = "\n".join(stock_list)
    
    # Create prompt for GPT
    prompt = f"""Analyze news and identify trading signals. Map companies to these stocks:

{stock_universe_text}

News:
{news_text}

Return JSON with:
1. Trading signals (buy/sell) with confidence (0-1)
2. Matched companies to stocks
3. Key points and metrics

Format:
{{
    "signals": [
        {{
            "type": "buy/sell",
            "symbol": "STOCK_SYMBOL",
            "confidence": 0.0-1.0,
            "reason": "Brief explanation",
            "timestamp": "ISO8601 timestamp"
        }}
    ],
    "news": [
        {{
            "title": "Original title",
            "summary": "Brief summary",
            "content": "Full content",
            "publishedAt": "ISO8601 timestamp",
            "source": "Source name",
            "url": "URL",
            "tags": {{
                "stocks": ["Stock symbols"],
                "matched_stocks": [
                    {{
                        "symbol": "STOCK_SYMBOL",
                        "company_name": "COMPANY_NAME",
                        "industry": "INDUSTRY"
                    }}
                ],
                "sentiment": "positive/negative/neutral",
                "impact": "high/medium/low",
                "key_points": ["Key points"],
                "financial_metrics": {{
                    "revenue": "value if mentioned",
                    "profit": "value if mentioned",
                    "growth": "value if mentioned"
                }}
            }}
        }}
    ]
}}

Rules:
1. Use exact stock symbols from the list
2. Include current timestamp for signals
3. Map all companies to stocks in the list
4. Provide confidence (0-1) for signals
5. Extract key metrics and points
6. Keep all text fields on a single line
7. Return only valid JSON"""

    try:
        response_text = get_gpt_response(prompt)
        # Clean the response text to ensure valid JSON
        response_text = response_text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Parse and validate the response
        result = json.loads(response_text)
        
        # Validate the structure
        if not isinstance(result, dict):
            raise ValueError("Response is not a dictionary")
        if "signals" not in result or "news" not in result:
            raise ValueError("Missing required fields in response")
        if not isinstance(result["signals"], list) or not isinstance(result["news"], list):
            raise ValueError("Signals and news must be lists")
            
        # Validate string fields
        for signal in result["signals"]:
            for field in ["type", "symbol", "reason", "timestamp"]:
                if not isinstance(signal.get(field), str):
                    raise ValueError(f"Invalid type for signal field {field}")
                if "\n" in signal[field]:
                    raise ValueError(f"Line break found in signal field {field}")
                    
        for news_item in result["news"]:
            for field in ["title", "summary", "content", "publishedAt", "source", "url"]:
                if not isinstance(news_item.get(field), str):
                    raise ValueError(f"Invalid type for news field {field}")
                if "\n" in news_item[field]:
                    raise ValueError(f"Line break found in news field {field}")
            
        return result
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error in GPT response: {e}")
        logger.error(f"Response text: {response_text}")
        return {"signals": [], "news": []}
    except Exception as e:
        logger.error(f"Error in analyze_news_with_gpt: {e}")
        return {"signals": [], "news": []} 