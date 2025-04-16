import streamlit as st
import asyncio
import textstat

from agents.topic_agent import generate_subtopics
from agents.research_agent import run_research
from agents.writing_agent import generate_markdown_blog
from agents.seo_agent import generate_metadata, estimate_reading_time


def generate_blog(topic: str, tone: str):
    topic_data = generate_subtopics(topic, tone)
    subtopics = topic_data["subtopics"]
    slug = topic_data["slug"]

    research_data = asyncio.run(run_research(topic))
    blog_md = generate_markdown_blog(topic, subtopics, research_data, tone)

    metadata = generate_metadata(topic, research_data.get("keywords", []))
    metadata["reading_time"] = estimate_reading_time(blog_md)
    metadata["readability_score"] = textstat.flesch_reading_ease(blog_md)

    return blog_md, metadata, slug


# 🌐 Streamlit UI
st.set_page_config(page_title="AI Blog Writer", layout="wide")
st.title("🧠 Autonomous Blog Writing Agent")

with st.form("blog_form"):
    topic = st.text_input("Enter Blog Topic", value="AI in Healthcare")
    tone = st.selectbox("Select Writing Tone", ["educational", "formal", "creative", "casual", "inspirational"])
    submitted = st.form_submit_button("🚀 Generate Blog")

if submitted and topic:
    with st.spinner("Generating your blog..."):
        blog_md, metadata, slug = generate_blog(topic, tone)

    st.success("✅ Blog generated!")

    # Show blog content
    st.markdown("### ✍️ Blog Content")
    st.markdown(blog_md)

    # Show metadata
    st.markdown("### 📊 SEO Metadata")
    st.json(metadata)

    # Download buttons
    st.markdown("### 💾 Download")
    st.download_button("Download Markdown", blog_md, file_name=f"{slug}.md")
    st.download_button("Download Metadata (JSON)", str(metadata), file_name=f"{slug}.json")
