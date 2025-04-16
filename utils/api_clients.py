
import aiohttp
import os
import asyncio
from dotenv import load_dotenv
import ssl
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


# async def fetch_quotable(topic: str) -> list:
#     url = f"https://api.quotable.io/search/quotes?query={topic}"

#     ssl_context = ssl.create_default_context()
#     ssl_context.check_hostname = False
#     ssl_context.verify_mode = ssl.CERT_NONE  

#     async with aiohttp.ClientSession() as session:
#         async with session.get(url, ssl=ssl_context) as response:
#             data = await response.json()
#             return [quote["content"] for quote in data.get("results", [])][:3]


async def fetch_quotable(topic: str, n: int = 3) -> list:
    url = "https://zenquotes.io/api/quotes"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            all_quotes = await response.json()

            # Filter quotes by topic keyword (case-insensitive)
            filtered = [
                f"{q['q']} — {q['a']}" 
                for q in all_quotes 
                if topic.lower() in q['q'].lower()
            ]

            # Fallback: if no match found, return first few quotes anyway
            if not filtered:
                filtered = [f"{q['q']} — {q['a']}" for q in all_quotes[:n]]

            return filtered[:n]
