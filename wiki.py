from config import config


def wiki_url_builder(label, base, end):
    return f"{config.blog_root_url}/{config.wiki_page}#{label.lower().replace(' ', '-')}"
