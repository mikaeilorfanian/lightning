import codecs
from dataclasses import dataclass
from datetime import datetime
import glob
from typing import List

from jinja2 import Environment, FileSystemLoader, select_autoescape
import markdown


env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


@dataclass
class NavbarItem:
    title: str
    link: str = '#'


@dataclass
class ArticleSummary:
    title: str
    description: str
    link: str
    category: str
    publication_date: str
    popularity: int = 0

    def __post_init__(self):
        self.link = self.category + '/' + self.link
        self.publication_date = datetime.strptime(self.publication_date, '%d-%m-%Y')


@dataclass
class HomeCard:
    title: str
    articles: List[ArticleSummary]


def generate_index_page():
    # TODO: filenames "index.html" should be turned into variables
    intro = NavbarItem(title='Home', link='index.html')
    technical = NavbarItem(title='Technical', link='pages/technical-articles.html')
    employment = NavbarItem(title='Employment')
    index_navbar_items = (intro, technical, employment)

    article1 = ArticleSummary(
        title='Types versus Classes', 
        description='The type of an object differs from its class and OOP relies a lot on this difference!',
        link='types-versus-classes.html',
        category='technical',
        publication_date='02-07-2019',
    )
    coder_card = HomeCard(title='Top 1% coder', articles=[article1])
    
    home_template = env.get_template('home2-template.html')
    rendered_tempalte = home_template.render(
        navbar_items=index_navbar_items, 
        home_cards=[coder_card],
        header_link='index.html',
    )
    with open('index.html', 'w') as f:
        f.write(rendered_tempalte)
generate_index_page()


def generate_technical_articles_page():
    # TODO: filenames "index.html" should be turned into variables
    intro = NavbarItem(title='Home', link='../index.html')
    technical = NavbarItem(title='Technical', link='technical-articles.html')
    employment = NavbarItem(title='Employment')
    article_category_navbar_items = (intro, technical, employment)

    # TODO: where do these strings (title, desc, link, etc.) come from so 
    # they're not hard coded
    article1 = ArticleSummary(
        title='Types versus Classes', 
        description='The type of an object differs from its class and OOP relies a lot on this difference!',
        link='types-versus-classes.html',
        category='technical',
        publication_date='02-07-2019',
    )
    latest_article = article1

    technical_articles_template = env.get_template('technical-articles-template.html')
    rendered_tempalte = technical_articles_template.render(
        navbar_items=article_category_navbar_items, 
        technical_articles=[article1],
        latest_article=latest_article,
        header_link='../index.html',
    )
    with open('pages/technical-articles.html', 'w') as f:
        f.write(rendered_tempalte)
generate_technical_articles_page()


@dataclass
class Article:
    title: str
    body: str


def generate_article():
    in_file = 'articles/self-driving-vehicle.md'
    out_file = 'articles/self-driving-vehicle-out.html'
    extensions = ['codehilite', 'meta']
    # markdown.markdownFromFile(input=in_file, extensions=extensions, output=out_file, encoding='utf-8')
    kwargs = dict(input=in_file, extensions=extensions, output=out_file, encoding='utf-8')

    md = markdown.Markdown(**kwargs)
    md.convertFile(kwargs.get('input', None),
                   kwargs.get('output', None),
                   kwargs.get('encoding', None))

    out_file_handle = codecs.open(out_file, mode='r', encoding='utf-8')
    body = out_file_handle.read()
    out_file_handle.close()

    intro = NavbarItem(title='Intro', link='../../index.html')
    technical = NavbarItem(title='Technical', link='../technical-articles.html')
    employment = NavbarItem(title='Employment')
    article_navbar_items = (intro, technical, employment)
    
    article = Article(title='Types versus Classes', body=body)

    article_template = env.get_template('article-template.html')
    rendered_tempalte = article_template.render(
        article=article, 
        navbar_items=article_navbar_items,
        header_link='../../index.html',
    )
    with open('pages/technical/types-versus-classes.html', 'w', encoding='utf-8') as f:
        f.write(rendered_tempalte)
generate_article()


def find_article_files():
    return [f for f in glob.glob('articles/*.md')]


def render_articles_and_get_their_metadata(filenames):
    metadata = []

    for in_file in filenames:
        in_file = 'articles/self-driving-vehicle.md'
        extensions = ['codehilite', 'meta']
        kwargs = dict(input=in_file, output=in_file.split('.md')[0]+'.html', extensions=extensions, encoding='utf-8')
        md = markdown.Markdown(**kwargs)
        md.convertFile(kwargs.get('input', None),
                    kwargs.get('output', None),
                    kwargs.get('encoding', None))
        metadata.append(md.Meta)

    return metadata


def make_article_summary_from_article_metadata(meta_data):
    return ArticleSummary(
        title=meta_data['title'][0], 
        description=meta_data['description'][0],
        link=meta_data['page_name'][0],
        category=meta_data['category'][0],
        publication_date=meta_data['publication_date'][0],
        popularity=meta_data['popularity'][0],
    )

def find_latest_article():
    md_files  = find_article_files()
    metadata = render_articles_and_get_their_metadata(md_files)
    articles = [
        make_article_summary_from_article_metadata(mtdata)
        for mtdata in metadata
    ]
    articles.sort(key=lambda article: article.publication_date, reverse=True)
find_latest_article()


def find_popular_articles(top_x: int, category: str=None):
    md_files  = find_article_files()
    metadata = render_articles_and_get_their_metadata(md_files)
    articles = [
        make_article_summary_from_article_metadata(mtdata)
        for mtdata in metadata
    ]

    if category:
        articles = [article for article in articles if article.category == category]

    articles.sort(key=lambda article: article.popularity, reverse=True)
    
    return articles[:top_x]
popular_articles = find_popular_articles(2, 'technical')
