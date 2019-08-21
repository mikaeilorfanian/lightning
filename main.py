import dataclasses
import logging
import os
from pathlib import Path
import sys
from typing import List

from jinja2 import Environment, FileSystemLoader, select_autoescape
import markdown
from markdown.extensions.wikilinks import WikiLinkExtension

from config import config
from datastructures import Articles, ArticleCategory, ArticleSummary, HomeCard, NavbarItem
from utils import read_file_content
from wiki import wiki_url_builder


@dataclasses.dataclass
class Category:
    technical: str = 'technical'
    philosophy: str = 'philosophy'
    scifi_book: str = 'scifi-documentary'


categories = Category()


def generate_navbar_items():
    '''
    To add a navbar item (button + link), create a NavbarItem instance here.
    '''
    root_path = config.blog_root_url
    article_category_path = f"{config.blog_root_url}/{config.FINAL_PAGES_DIR}"

    return (
        NavbarItem('Home', 'index', root_path),
        NavbarItem('Philosophy', 'philosophy-articles', article_category_path),
        NavbarItem('Technical', 'technical-articles', article_category_path),
        NavbarItem('Software Dev in 2040', categories.scifi_book, article_category_path),
        NavbarItem('Wiki', 'wiki', root_path),
        NavbarItem('Projects', 'projects', root_path),
        NavbarItem('About', 'about', root_path),
    )


navbar_items = generate_navbar_items()


@dataclasses.dataclass
class SortingAttr:
    pub_date: str = 'publication_date'
    popularity: str = 'popularity'


sorting_attributes = SortingAttr()


def generate_home_page(articles: Articles):
    '''
    '''
    technical_articles = articles.get_top_articles_by_category_and_sorted_by_attribute(
        sorting_attributes.pub_date, categories.technical
    )
    coder_card = HomeCard(title='Top 1% Coder', articles=technical_articles)

    scifi_book_articles = articles.get_top_articles_by_category_and_sorted_by_attribute(
    sorting_attributes.pub_date, categories.scifi_book
    )
    scifi_book_card = HomeCard(title='Software Dev in 2040', articles=scifi_book_articles)

    philosophy_articles = articles.get_top_articles_by_category_and_sorted_by_attribute(
        sorting_attributes.pub_date, categories.philosophy
    )
    thinker_card = HomeCard(title='Top 1% Thinker', articles=philosophy_articles)

    popular_articles = articles.get_top_articles_by_category_and_sorted_by_attribute(
        sorting_attributes.popularity, top_x=config.TOP_X_ARTICLES
    )
    home_template = env.get_template(config.home_page_template)
    rendered_tempalte = home_template.render(
        navbar_items=navbar_items,
        home_cards=[coder_card, scifi_book_card, thinker_card],
        header_link=config.index_page,
        popular_articles=popular_articles,
    )
    with open(config.index_page, 'w') as f:
        f.write(rendered_tempalte)


def generate_page(
    articles: Articles, template_filename: str, page_output_filename: str, **template_context_params
):
    template = env.get_template(template_filename)
    rendered_tempalte = template.render(
        navbar_items=navbar_items,
        header_link=config.index_page,
        popular_articles=top_x_popular_articles,
        **template_context_params,
    )
    with open(page_output_filename, 'w') as f:
        f.write(rendered_tempalte)

    logging.info(f'Generated and rendered {page_output_filename}!')


def generate_wiki_page(articles: Articles):
    extensions = [WikiLinkExtension(build_url=wiki_url_builder), 'nl2br', 'extra']
    kwargs = dict(
        input=config.wiki_page_md, output=config.wiki_page, extensions=extensions, encoding='utf-8'
    )
    md = markdown.Markdown(**kwargs)
    md.convertFile(kwargs['input'], kwargs['output'], kwargs['encoding'])

    generate_page(
        articles,
        config.wiki_page_template,
        config.wiki_page,
        wiki_html=read_file_content(config.wiki_page),
    )


def generate_article_categories_pages(_articles: Articles):
    categories = [
        ArticleCategory(
            'technical',
            'Top 1% Code: Technical Articles',
            'technical-articles',
            config.FINAL_PAGES_DIR,
        ),
        ArticleCategory(
            'philosophy',
            'Top 1% Thinker: Thinking Superpowers',
            'philosophy-articles',
            config.FINAL_PAGES_DIR,
        ),
        ArticleCategory(
            'scifi-documentary',
            'Software in 2040',
            'scifi-documentary',
            config.FINAL_PAGES_DIR,
        )
    ]
    for category in categories:
        articles_chronological = _articles.get_top_articles_by_category_and_sorted_by_attribute(
            'publication_date', category.name
        )
        articles_popular = _articles.get_top_articles_by_category_and_sorted_by_attribute(
            'popularity', category.name
        )
        template = env.get_template('articles-category-template.html')
        rendered_tempalte = template.render(
            navbar_items=navbar_items,
            technical_articles=articles_chronological,
            featured_article=_articles.get_featured_article(category.name),
            popular_articles=articles_popular,
            header_link='../index.html',
            page_title=category.page_title,
        )
        with open(category.link, 'w') as f:
            f.write(rendered_tempalte)


def generate_page_for_each_article(articles):
    for article in articles.summaries:
        out_file = article.output_file
        article.body = read_file_content(out_file)

        article_template = env.get_template('article-template.html')
        rendered_tempalte = article_template.render(
            article=article, navbar_items=navbar_items, header_link='../../index.html'
        )
        html_page = Path('.') / config.FINAL_PAGES_DIR / article.category / article.output_file.name
        with html_page.open('w', encoding='utf-8') as f:
            f.write(rendered_tempalte)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    env = Environment(
        loader=FileSystemLoader(config.templates_folder),
        autoescape=select_autoescape(['html', 'xml']),
    )

    logging.info('Environment setup complete!')

    articles = Articles(config.RAW_ARTICLES_DIR, config.blog_root_url)
    articles.render_markdown_files()

    top_x_popular_articles = articles.get_top_articles_by_category_and_sorted_by_attribute(
        sorting_attributes.popularity, top_x=config.TOP_X_ARTICLES
    )

    logging.info('Converted Markdown articles to HTML!')
    logging.info('---------- Rendering Blog ----------')

    generate_home_page(articles)
    generate_page(articles, config.about_page_template, config.about_page)
    generate_page(articles, config.projects_page_template, config.projects_page)
    generate_wiki_page(articles)
    generate_article_categories_pages(articles)
    generate_page_for_each_article(articles)
