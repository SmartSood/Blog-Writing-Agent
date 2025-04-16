
import aiohttp
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWSDATA_API_KEY")


async def fetch_with_retries(session, url, max_retries=3):
    for attempt in range(max_retries):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"⚠️ API returned status {response.status}. Retrying...")
        except aiohttp.ClientError as e:
            print(f"⚠️ Client error: {e}. Retrying...")
        await asyncio.sleep(1)
    return {}


async def fetch_newsdata(topic: str) -> list:
    url = f"https://newsdata.io/api/1/news?apikey={NEWS_API_KEY}&q={topic}&language=en"
    async with aiohttp.ClientSession() as session:
        data = await fetch_with_retries(session, url)
        return [article["title"] for article in data.get("results", [])][:5]


async def fetch_datamuse(topic: str) -> list:
    url = f"https://api.datamuse.com/words?ml={topic}"
    async with aiohttp.ClientSession() as session:
        data = await fetch_with_retries(session, url)
        return [item["word"] for item in data][:10]


async def fetch_quotable(topic: str) -> list:
    url = f"https://api.quotable.io/search/quotes?query={topic}"
    async with aiohttp.ClientSession() as session:
        data = await fetch_with_retries(session, url)
        return [quote["content"] for quote in data.get("results", [])][:3]
