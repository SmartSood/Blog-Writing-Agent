def format_quote_block(quote: str) -> str:
    return f"> _{quote}_\n\n"

def wrap_subsection(title: str, content: str) -> str:
    return f"## {title}\n\n{content.strip()}\n\n"

def add_bullet_points(items: list) -> str:
    return "\n".join([f"- {item}" for item in items]) + "\n\n"


def generate_header(title: str, tone: str) -> str:
    return f"# {title}\n\n**Tone**: {tone}\n\n"


def wrap_blog_body(intro: str, body_sections: list, outro: str) -> str:
    blog = intro + "\n\n"
    for section in body_sections:
        blog += section + "\n"
    blog += outro + "\n"
    return blog


### Remaining agent and api_clients code remains unchanged from previous state.
