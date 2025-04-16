# 🧠 Autonomous Blog Writing Agent

A Python-based AI-powered content generation tool that mimics a junior blog writer + SEO optimizer.  
It uses public APIs and LLMs to autonomously plan, research, write, and export long-form Markdown blogs with SEO metadata.

---
# Live Demo
```link
https://ai-blog-wri.streamlit.app/
```
## 🚀 Features

- 🧠 Understands the topic and tone
- 📰 Gathers research using:
  - NewsData.io for recent news highlights
  - Datamuse for SEO keyword suggestions
  - Quotable for quotes
- ✍️ Uses Google Gemini 1.5 Pro to write well-structured blogs
- 📈 Generates SEO metadata:
  - Title, meta-description, keywords, estimated reading time, slug
- 📘 Calculates readability score (Flesch Reading Ease)
- 💾 Exports:
  - `.md` blog file
  - `.json` structured metadata
- 🧰 CLI-powered with progress bars, logging, and batch processing

---

## 🛠 Setup Instructions

### 1. Clone this repo
```bash
git clone https://github.com/yourusername/blog-writing-agent.git
cd blog-writing-agent
```
### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Create a .env file in the root directory
Add your API keys:

```env
NEWSDATA_API_KEY=your_newsdata_api_key
GEMINI_API_KEY=your_gemini_api_key
```
## 🧪 How to Use


##  Front End Deployment
```bash
streamlit run streamlit_app.py
```

## Backend only

### Single topic:
```bash
python main.py --topic "AI in Healthcare"
```
### Multiple topics (batch mode):
```bash
python main.py --topics "AI in Healthcare, Blockchain in Finance, Data Privacy" --tone "formal"
```
You can change tone with --tone flag:
educational (default), formal, creative, casual, etc.

## 📁 Output Files
All blogs and metadata are saved in the outputs/ folder:

outputs/ai-in-healthcare.md — full blog

outputs/ai-in-healthcare.json — SEO metadata

## 📊 Logs & Debugging
All activity is logged to:

```lua
logs/output.log
```
Example:
```yaml
2025-04-16 20:02:45 [INFO] Started blog generation for: AI in Healthcare
2025-04-16 20:02:55 [INFO] Finished blog for: AI in Healthcare, slug: ai-in-healthcare, readability: 66.2
```
### 📸 Sample Output Preview
Markdown Blog:
```markdown
# AI in Healthcare
Artificial intelligence is revolutionizing healthcare by improving diagnostics, personalizing treatment, and optimizing hospital operations...
```
Metadata JSON:
```json
{
  "title": "AI In Healthcare",
  "meta_description": "Read this blog to learn about AI in healthcare and key insights.",
  "slug": "ai-in-healthcare",
  "tags": ["AI", "healthcare", "diagnostics", "robotics", "personalized medicine"],
  "reading_time": "4 min read",
  "readability_score": 66.2
}
```

### 👨‍💻 @SmartSood
This project was built as part of a Python internship project at Flowgic.

