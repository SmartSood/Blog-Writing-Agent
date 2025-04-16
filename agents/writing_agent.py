# agents/writing_agent.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def generate_markdown_blog(topic: str, subtopics: list, research_data: dict, tone: str = "educational") -> str:
    """
    Generates a full markdown blog using Google Gemini.
    """
    model = genai.GenerativeModel("gemini-1.5-pro-latest")

    research_summary = ""
    if research_data.get("news"):
        research_summary += "News Highlights:\n" + "\n".join(f"- {item}" for item in research_data["news"]) + "\n\n"
    if research_data.get("keywords"):
        research_summary += "Related Keywords:\n" + ", ".join(research_data["keywords"]) + "\n\n"
    if research_data.get("quotes"):
        research_summary += "Inspirational Quotes:\n" + "\n".join(f"> {quote}" for quote in research_data["quotes"]) + "\n\n"

    prompt = f"""
Act as a professional blog writer with a {tone} tone.

Topic: {topic}
Subtopics: {', '.join(subtopics)}
Research Data: 
{research_summary}

Task:
- Write a complete markdown blog.
- Start with a compelling introduction.
- Use the subtopics as section headers.
- Integrate news, keywords, and at least one quote.
- End with a conclusion that encourages engagement.
- Keep it human-like and SEO-friendly.

Output: Markdown format.
    """

    response = model.generate_content(prompt)
    blog_md = response.text.strip()

    return blog_md
