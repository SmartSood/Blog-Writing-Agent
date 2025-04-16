import os
import json

def export_blog(blog_md: str, metadata: dict, slug: str):
    os.makedirs("outputs", exist_ok=True)

    md_path = f"outputs/{slug}.md"
    json_path = f"outputs/{slug}.json"

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(blog_md)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"\n✅ Exported blog to {md_path} and metadata to {json_path}")