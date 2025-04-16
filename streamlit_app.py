import streamlit as st
import asyncio
import textstat
import json

from agents.topic_agent import generate_subtopics
from agents.research_agent import run_research
from agents.writing_agent import generate_markdown_blog
from agents.seo_agent import generate_metadata, estimate_reading_time


def generate_blog(topic: str, tone: str,progress=None):
    if progress: progress.progress(10, "🔍 Generating subtopics...")
    topic_data = generate_subtopics(topic, tone)
    subtopics = topic_data["subtopics"]
    slug = topic_data["slug"]

    if progress: progress.progress(40, "📚 Running research...")
    research_data = asyncio.run(run_research(topic))
    if progress: progress.progress(70, "✍️ Writing your blog...")
    blog_md = generate_markdown_blog(topic, subtopics, research_data, tone)
    if progress: progress.progress(90, "🧠 Generating metadata...")
    metadata = generate_metadata(topic, research_data.get("keywords", []))
    metadata["reading_time"] = estimate_reading_time(blog_md)
    metadata["readability_score"] = textstat.flesch_reading_ease(blog_md)
    if progress: progress.progress(100, "✅ Done!")
    return blog_md, metadata, slug



st.set_page_config(page_title="📝 AI Blog Agent", layout="wide")
st.title("🧠 Autonomous Blog Writing Agent")

st.markdown("Craft long-form blogs like a pro content writer — with AI & public data magic! 🔍🧠")


with st.form("blog_form"):
    topic = st.text_input("💡 What’s your blog topic?", value="AI in Healthcare")
    tone = st.selectbox("🎨 Choose a writing tone", ["educational", "formal", "creative", "casual", "inspirational"])
    submitted = st.form_submit_button("🚀 Write My Blog!")


if submitted and topic:
    with st.spinner("⌛️ Thinking, researching, and writing..."):
        progress_bar = st.progress(0)
        blog_md, metadata, slug = generate_blog(topic, tone,progress=progress_bar)
        progress_bar.empty()
        # Store in session state to persist
        st.session_state.blog_md = blog_md
        st.session_state.metadata = metadata
        st.session_state.slug = slug


if "blog_md" in st.session_state and "metadata" in st.session_state:
    
    st.success("✅ Your blog is ready!")

    st.markdown("### 📄 Blog Content Preview")
    st.markdown(st.session_state.blog_md)

    st.markdown("### 📊 Blog Metadata Snapshot")
    st.json(st.session_state.metadata)

    st.markdown("### 📥 Save Your Work")

    st.download_button(
        label="📥 Download Blog (.md)",
        data=st.session_state.blog_md,
        file_name=f"{st.session_state.slug}.md",
        mime="text/markdown"
    )

    st.download_button(
        label="🧾 Download Metadata (.json)",
        data=json.dumps(st.session_state.metadata, indent=2),
        file_name=f"{st.session_state.slug}.json",
        mime="application/json"
    )

    st.info("Need another blog? Just enter a new topic above ☝️")
