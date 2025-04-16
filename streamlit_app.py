import streamlit as st
import asyncio
import textstat
import json
from deep_translator import GoogleTranslator

from agents.topic_agent import generate_subtopics
from agents.research_agent import run_research
from agents.writing_agent import generate_markdown_blog
from agents.seo_agent import generate_metadata, estimate_reading_time


def generate_blog(topic: str, tone: str, target_lang='none', progress=None):
    if progress:
        progress.progress(10, f"🔍 Generating subtopics for: {topic}")
    topic_data = generate_subtopics(topic, tone)
    subtopics = topic_data["subtopics"]
    slug = topic_data["slug"]

    if progress:
        progress.progress(40, f"📚 Running research for: {topic}")
    research_data = asyncio.run(run_research(topic))

    if progress:
        progress.progress(70, f"✍️ Writing blog for: {topic}")
    blog_md = generate_markdown_blog(topic, subtopics, research_data, tone)

    if progress:
        progress.progress(90, f"🧠 Generating metadata for: {topic}")
    metadata = generate_metadata(topic, research_data.get("keywords", []))
    metadata["reading_time"] = estimate_reading_time(blog_md)
    metadata["readability_score"] = textstat.flesch_reading_ease(blog_md)

    # Translation
    if target_lang != 'none':
        try:
            if progress:
                progress.progress(95, f"🌐 Translating blog to {target_lang.upper()}...")
            translated = GoogleTranslator(source='auto', target=target_lang).translate(blog_md)
            blog_md = translated
            metadata["translated_language"] = target_lang
        except Exception as e:
            st.warning(f"⚠️ Translation failed for '{topic}': {e}")

    if progress:
        progress.progress(100, f"✅ Done: {topic}")

    return blog_md, metadata, slug


# Streamlit UI
st.set_page_config(page_title="📝 AI Blog Agent", layout="wide")
st.title("🧠 Autonomous Blog Writing Agent")
st.markdown("Craft long-form blogs like a pro content writer — with AI & public data magic! 🔍🧠")

# Input Form
with st.form("blog_form"):
    st.markdown("Enter one or more blog topics below (one per line):")
    topics_input = st.text_area("💡 Blog Topics", value="AI in Healthcare\nAI in Education")
    tone = st.selectbox("🎨 Choose a writing tone", ["educational", "formal", "creative", "casual", "inspirational"])
    languages = ['none', 'hi', 'es', 'fr', 'de', 'zh', 'ar', 'ru', 'ja']
    target_lang = st.selectbox("🌐 Translate blog to:", languages, index=0)
    submitted = st.form_submit_button("🚀 Write My Blogs!")

# Blog Generation
if submitted and topics_input.strip():
    topics = [t.strip() for t in topics_input.strip().splitlines() if t.strip()]
    progress_bar = st.progress(0)
    st.session_state.results = []

    for i, topic in enumerate(topics):
        pct = int((i / len(topics)) * 100)
        progress_bar.progress(pct, f"Processing: {topic}")
        blog_md, metadata, slug = generate_blog(topic, tone, target_lang, progress=progress_bar)
        st.session_state.results.append({
            "topic": topic,
            "slug": slug,
            "markdown": blog_md,
            "metadata": metadata
        })

    progress_bar.empty()
    st.success("✅ All blogs are ready!")

# Display Results
if "results" in st.session_state:
    for idx, result in enumerate(st.session_state.results, start=1):
        st.markdown(f"## 📝 Blog {idx}: {result['topic']}")

        with st.expander("📄 View Blog Content", expanded=False):
            st.markdown(result["markdown"])

        with st.expander("📊 Metadata Snapshot", expanded=False):
            st.json(result["metadata"])

        st.download_button(
            label="📥 Download Blog (.md)",
            data=result["markdown"],
            file_name=f"{result['slug']}.md",
            mime="text/markdown",
            key=f"md_{idx}"
        )

        st.download_button(
            label="🧾 Download Metadata (.json)",
            data=json.dumps(result["metadata"], indent=2),
            file_name=f"{result['slug']}.json",
            mime="application/json",
            key=f"json_{idx}"
        )

        st.markdown("---")

    st.info("Want more blogs? Enter new topics above ☝️")
