import codecs
from pathlib import Path
import sys

from jinja2 import Environment, FileSystemLoader, select_autoescape
import markdown

from datastructures import Articles, ArticleSummary, HomeCard, NavbarItem, Page, SingleArticle


def generate_navbar_items(current_page: str):
    if current_page == 'home':
        root_path = None
        article_category_path = 'pages'

    elif current_page == 'category':
        root_path = '..'
        article_category_path = None
    
    elif current_page == 'article-details':
        root_path = '../..'
        article_category_path = '..'

    intro = Page('Home', 'index', root_path)
    intro = NavbarItem(intro.title, intro.link)
    technical = Page('Technical', 'technical-articles', article_category_path)
    technical = NavbarItem(technical.title, technical.link)
    about = Page('About', 'about', root_path)
    about = NavbarItem(about.title, about.link)

    return (intro, technical, about)


def generate_index_page(articles):
    technical_articles = articles.get_top_articles_by_attribute_and_category(
        'publication_date', 
        'technical',
    )
    coder_card = HomeCard(title='Top 1% coder', articles=technical_articles)
    popular_articles = articles.get_top_articles_by_attribute_and_category(
        'popularity', 
        'technical', 
        5,
    )
    home_template = env.get_template('home-template.html')
    rendered_tempalte = home_template.render(
        navbar_items=generate_navbar_items('home'), 
        home_cards=[coder_card],
        header_link='index.html',
        popular_articles=popular_articles,
    )
    with open('index.html', 'w') as f:
        f.write(rendered_tempalte)


def generate_technical_articles_page(articles):
    navbar_items = generate_navbar_items('category')

    technical_articles_template = env.get_template('articles-category-template.html')
    rendered_tempalte = technical_articles_template.render(
        navbar_items=navbar_items, 
        technical_articles=articles.summaries,
        featured_article=articles.summaries[0],
        header_link='../index.html',
        page_title='Top 1% Code: Technical Articles'
    )
    with open('pages/technical-articles.html', 'w') as f:
        f.write(rendered_tempalte)


def generate_articles_pages(articles):
    for article in articles.summaries:
        out_file = article.output_file
        out_file_handle = codecs.open(out_file, mode='r', encoding='utf-8')
        article.body = out_file_handle.read()
        out_file_handle.close()

        article_template = env.get_template('article-template.html')
        rendered_tempalte = article_template.render(
            article=article, 
            navbar_items=generate_navbar_items('article-details'),
            header_link='../../index.html',
        )
        html_page = Path('.') / 'pages' / article.category / article.output_file.name
        with html_page.open('w', encoding='utf-8') as f:
            f.write(rendered_tempalte)


if __name__ == "__main__":
    env = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    
    LOCAL_URL = 'file:///C:/Users/mokt/dev/blog'
    PROD_URL = 'https://mikaeilorfanian.github.io'
    site_url = LOCAL_URL if sys.argv[1] == 'local' else PROD_URL
    articles = Articles('articles', site_url)
    articles.render_markdown_files()
    
    generate_index_page(articles)
    generate_technical_articles_page(articles)
    generate_articles_pages(articles)
