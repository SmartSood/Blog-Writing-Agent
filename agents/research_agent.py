import asyncio
from utils.api_clients import fetch_newsdata, fetch_datamuse, fetch_quotable

async def run_research(topic: str) -> dict:
    """
    Gathers news articles, keywords, and quotes concurrently.
    """
    news_task = fetch_newsdata(topic)
    keywords_task = fetch_datamuse(topic)
    quotes_task = fetch_quotable(topic)

    news, keywords, quotes = await asyncio.gather(news_task, keywords_task, quotes_task)

    return {
        "news": news,
        "keywords": keywords,
        "quotes": quotes
    }