import math
import re

def estimate_reading_time(text: str) -> str:
    word_count = len(re.findall(r'\w+', text))
    minutes = math.ceil(word_count / 200)
    return f"{minutes} min read"

def generate_metadata(topic: str, keywords: list) -> dict:
    """
    Generate title, meta, keywords, slug, and estimated reading time.
    """
    title = topic.title()
    meta = f"Read this blog to learn about {topic.lower()} and key insights."
    slug = topic.lower().replace(" ", "-")
    return {
        "title": title,
        "meta_description": meta[:160],
        "slug": slug,
        "tags": keywords[:5],
    }
