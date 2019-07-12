import os
from pathlib import Path
import sys

from jinja2 import Environment, FileSystemLoader, select_autoescape
import markdown
from markdown.extensions.wikilinks import WikiLinkExtension

from datastructures import Articles, ArticleCategory, ArticleSummary, HomeCard, NavbarItem, Page, SingleArticle
from utils import read_file_content
from wiki import wiki_url_builder


TOP_X_ARTICLES = 5
FINAL_PAGES_DIR = 'pages'


def generate_navbar_items(current_page: str):
    if current_page == 'home':
        root_path = os.environ['SITE_URL']
        article_category_path = f"{os.environ['SITE_URL']}/{FINAL_PAGES_DIR}"

    elif current_page == 'category':
        root_path = os.environ['SITE_URL']
        article_category_path = f"{os.environ['SITE_URL']}/{FINAL_PAGES_DIR}"

    elif current_page == 'article-details':
        root_path = os.environ['SITE_URL']
        article_category_path = '..'

    home = Page('Home', 'index', root_path)
    home = NavbarItem(home.title, home.link)
    wiki = Page('Wiki', 'wiki', root_path)
    wiki = NavbarItem(wiki.title, wiki.link)
    philosophy = Page('Philosophy', 'philosophy-articles', article_category_path)
    philosophy = NavbarItem(philosophy.title, philosophy.link)
    technical = Page('Technical', 'technical-articles', article_category_path)
    technical = NavbarItem(technical.title, technical.link)
    about = Page('About', 'about', root_path)
    about = NavbarItem(about.title, about.link)

    return (home, philosophy, technical, wiki, about)


def generate_home_page(articles):
    technical_articles = articles.get_top_articles_by_category_and_sorted_by_attribute('publication_date', 'technical')
    coder_card = HomeCard(title='Top 1% Coder', articles=technical_articles)

    philosophy_articles = articles.get_top_articles_by_category_and_sorted_by_attribute(
        'publication_date', 'philosophy'
    )
    thinker_card = HomeCard(title='Top 1% Thinker', articles=philosophy_articles)

    popular_articles = articles.get_top_articles_by_category_and_sorted_by_attribute('popularity', top_x=TOP_X_ARTICLES)
    home_template = env.get_template('home-template.html')
    rendered_tempalte = home_template.render(
        navbar_items=generate_navbar_items('home'),
        home_cards=[coder_card, thinker_card],
        header_link='index.html',
        popular_articles=popular_articles,
    )
    with open('index.html', 'w') as f:
        f.write(rendered_tempalte)


def generate_about_page(articles):
    popular_articles = articles.get_top_articles_by_category_and_sorted_by_attribute('popularity', top_x=TOP_X_ARTICLES)
    about_template = env.get_template('about-template.html')
    rendered_tempalte = about_template.render(
        navbar_items=generate_navbar_items('home'), header_link='index.html', popular_articles=popular_articles
    )
    with open('about.html', 'w') as f:
        f.write(rendered_tempalte)


def generate_wiki_page(articles):
    extensions = [WikiLinkExtension(build_url=wiki_url_builder), 'nl2br', 'extra']
    kwargs = dict(input='wiki.md', output='wiki.html', extensions=extensions, encoding='utf-8')
    md = markdown.Markdown(**kwargs)
    md.convertFile(kwargs.get('input', None), kwargs.get('output', None), kwargs.get('encoding', None))

    popular_articles = articles.get_top_articles_by_category_and_sorted_by_attribute('popularity', top_x=TOP_X_ARTICLES)
    wiki_template = env.get_template('wiki-template.html')
    rendered_tempalte = wiki_template.render(
        navbar_items=generate_navbar_items('home'),
        header_link='index.html',
        popular_articles=popular_articles,
        wiki_html=read_file_content('wiki.html'),
    )
    with open('wiki.html', 'w') as f:
        f.write(rendered_tempalte)


def generate_technical_articles_page(_articles):
    categories = [
        ArticleCategory('technical', 'Top 1% Code: Technical Articles', 'technical-articles', 'pages'),
        ArticleCategory('philosophy', 'Top 1% Thinker: Thinking Superpowers', 'philosophy-articles', 'pages'),
    ]
    for category in categories:
        navbar_items = generate_navbar_items('category')
        articles_chronological = _articles.get_top_articles_by_category_and_sorted_by_attribute(
            'publication_date', category.name
        )
        articles_popular = _articles.get_top_articles_by_category_and_sorted_by_attribute('popularity', category.name)
        technical_articles_template = env.get_template('articles-category-template.html')
        rendered_tempalte = technical_articles_template.render(
            navbar_items=navbar_items,
            technical_articles=articles_chronological,
            featured_article=_articles.get_featured_article(category.name),
            popular_articles=articles_popular,
            header_link='../index.html',
            page_title=category.page_title,
        )
        with open(category.link, 'w') as f:
            f.write(rendered_tempalte)


def generate_articles_pages(articles):
    for article in articles.summaries:
        out_file = article.output_file
        article.body = read_file_content(out_file)

        article_template = env.get_template('article-template.html')
        rendered_tempalte = article_template.render(
            article=article, navbar_items=generate_navbar_items('article-details'), header_link='../../index.html'
        )
        html_page = Path('.') / 'pages' / article.category / article.output_file.name
        with html_page.open('w', encoding='utf-8') as f:
            f.write(rendered_tempalte)


if __name__ == "__main__":
    env = Environment(loader=FileSystemLoader('templates'), autoescape=select_autoescape(['html', 'xml']))

    LOCAL_URL = 'file:///C:/Users/mokt/dev/blog'
    PROD_URL = 'https://mikaeilorfanian.github.io'
    if len(sys.argv) == 2:
        site_url = LOCAL_URL if sys.argv[1] == 'local' else PROD_URL
    else:
        site_url = LOCAL_URL
    os.environ['SITE_URL'] = site_url

    articles = Articles('articles', site_url)
    articles.render_markdown_files()

    generate_home_page(articles)
    generate_about_page(articles)
    generate_wiki_page(articles)
    generate_technical_articles_page(articles)
    generate_articles_pages(articles)
