import os


def wiki_url_builder(label, base, end):
    return f"{os.environ['SITE_URL']}/wiki.html#{label.lower().replace(' ', '-')}"
