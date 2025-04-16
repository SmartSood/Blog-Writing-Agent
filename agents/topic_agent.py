def generate_subtopics(topic: str, tone: str = "educational") -> dict:
    """
    Generate a blog outline/subtopics based on the input topic.
    Currently uses hardcoded logic, can be upgraded with LLM prompt.
    """
    import hashlib

    hashed = int(hashlib.md5(topic.encode()).hexdigest(), 16)
    example_subtopics = [
        "Introduction to the Topic",
        "Historical Background",
        "Current Applications",
        "Challenges & Limitations",
        "Future Prospects",
        "Conclusion"
    ]
    return {
        "tone": tone,
        "subtopics": example_subtopics,
        "slug": topic.lower().replace(" ", "-")[:50]
    }