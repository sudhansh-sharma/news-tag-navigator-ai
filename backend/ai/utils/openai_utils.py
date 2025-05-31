import openai
import logging
from typing import List, Dict, Any
import os

logger = logging.getLogger(__name__)

def analyze_news_with_gpt(news_text: str) -> Dict[str, Any]:
    """Analyze news text using GPT."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial news analyzer."},
                {"role": "user", "content": news_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error analyzing news with GPT: {e}")
        return {} 