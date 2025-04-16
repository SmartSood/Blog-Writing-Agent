# import argparse
# import asyncio
# import textstat

# from agents.topic_agent import generate_subtopics
# from agents.research_agent import run_research
# from agents.writing_agent import generate_markdown_blog
# from agents.seo_agent import generate_metadata, estimate_reading_time
# from agents.export_agent import export_blog

# def generate_for_topic(topic: str, tone: str):
#     print(f"\n📝 Generating blog for topic: {topic}")

#     # Step 1: Understand Topic
#     topic_data = generate_subtopics(topic, tone)
#     subtopics = topic_data["subtopics"]
#     slug = topic_data["slug"]

#     # Step 2: Research
#     print("🔍 Conducting research...")
#     research_data = asyncio.run(run_research(topic))

#     # Step 3: Generate Blog Content
#     print("✍️ Writing blog...")
#     blog_md = generate_markdown_blog(topic, subtopics, research_data, tone)

#     # Step 4: SEO Metadata
#     print("📈 Generating SEO metadata...")
#     metadata = generate_metadata(topic, research_data.get("keywords", []))
#     metadata["reading_time"] = estimate_reading_time(blog_md)

#     # Step 5: Readability Score
#     print("📘 Calculating readability score...")
#     score = textstat.flesch_reading_ease(blog_md)
#     metadata["readability_score"] = score
#     print(f"📗 Readability Score: {score}")

#     # Step 6: Export
#     export_blog(blog_md, metadata, slug)
#     print(f"✅ Blog generation complete for: {topic}")


# def main():
#     parser = argparse.ArgumentParser(description="Autonomous Blog Writer Agent")
#     parser.add_argument("--topic", help="Single topic to write about")
#     parser.add_argument("--topics", help="Comma-separated list of topics")
#     parser.add_argument("--tone", default="educational", help="Writing tone (e.g., formal, creative, etc.)")
#     args = parser.parse_args()

#     # Validate input
#     if args.topics:
#         topics = [t.strip() for t in args.topics.split(",")]
#     elif args.topic:
#         topics = [args.topic.strip()]
#     else:
#         print("❌ Please provide --topic or --topics.")
#         return

#     # Generate for each topic
#     for topic in topics:
#         generate_for_topic(topic, args.tone)


# if __name__ == "__main__":
#     main()

import argparse
import asyncio
import os
import logging
import textstat
from tqdm import tqdm
from datetime import datetime

from agents.topic_agent import generate_subtopics
from agents.research_agent import run_research
from agents.writing_agent import generate_markdown_blog
from agents.seo_agent import generate_metadata, estimate_reading_time
from agents.export_agent import export_blog


# ✅ Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/output.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def generate_for_topic(topic: str, tone: str):
    try:
        logging.info(f"Started blog generation for: {topic}")
        print(f"\n📝 Generating blog for topic: {topic}")

        # Step 1: Understand Topic
        topic_data = generate_subtopics(topic, tone)
        subtopics = topic_data["subtopics"]
        slug = topic_data["slug"]

        # Step 2: Research
        print("🔍 Conducting research...")
        research_data = asyncio.run(run_research(topic))

        # Step 3: Generate Blog Content
        print("✍️ Writing blog...")
        blog_md = generate_markdown_blog(topic, subtopics, research_data, tone)

        # Step 4: SEO Metadata
        print("📈 Generating SEO metadata...")
        metadata = generate_metadata(topic, research_data.get("keywords", []))
        metadata["reading_time"] = estimate_reading_time(blog_md)

        # Step 5: Readability Score
        print("📘 Calculating readability score...")
        score = textstat.flesch_reading_ease(blog_md)
        metadata["readability_score"] = score
        print(f"📗 Readability Score: {score}")

        # Step 6: Export
        export_blog(blog_md, metadata, slug)
        print("📄 Blog Preview:\n" + blog_md[:300] + "...\n")
        print(f"✅ Blog generation complete for: {topic}")

        logging.info(f"Finished blog for: {topic}, slug: {slug}, readability: {score}")

    except Exception as e:
        logging.error(f"❌ Error generating blog for {topic}: {str(e)}")
        print(f"❌ An error occurred for {topic}. Check logs/output.log for details.")


def main():
    parser = argparse.ArgumentParser(description="Autonomous Blog Writer Agent")
    parser.add_argument("--topic", help="Single topic to write about")
    parser.add_argument("--topics", help="Comma-separated list of topics")
    parser.add_argument("--tone", default="educational", help="Writing tone (e.g., formal, creative, etc.)")
    args = parser.parse_args()

    # Parse topics
    if args.topics:
        topics = [t.strip() for t in args.topics.split(",")]
    elif args.topic:
        topics = [args.topic.strip()]
    else:
        print("❌ Please provide --topic or --topics.")
        return

    # Loop through topics with a progress bar
    for topic in tqdm(topics, desc="🚀 Generating Blogs", ncols=80):
        generate_for_topic(topic, args.tone)


if __name__ == "__main__":
    main()

