import codecs

from jinja2 import Environment, FileSystemLoader, select_autoescape
import markdown

from datastructures import Articles, ArticleSummary, HomeCard, NavbarItem, Page, SingleArticle


env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


def find_latest_article():
    articles = Articles('articles')
    articles.render_markdown_files()
    return articles.get_top_articles_by_attribute_and_category('publication_date', 'technical')
find_latest_article()


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


def generate_index_page():
    article1 = ArticleSummary(
        title='Types versus Classes', 
        description='The type of an object differs from its class and OOP relies a lot on this difference!',
        root='pages',
        link='types-versus-classes.html',
        category='technical',
        publication_date='02-07-2019',
        source_file='self-driving-vehicle.md',
    )
    coder_card = HomeCard(title='Top 1% coder', articles=[article1])
    
    home_template = env.get_template('home2-template.html')
    rendered_tempalte = home_template.render(
        navbar_items=generate_navbar_items('home'), 
        home_cards=[coder_card],
        header_link='index.html',
    )
    with open('index.html', 'w') as f:
        f.write(rendered_tempalte)
generate_index_page()


def generate_technical_articles_page():
    article1 = ArticleSummary(
        title='Types versus Classes', 
        description='The type of an object differs from its class and OOP relies a lot on this difference!',
        link='types-versus-classes.html',
        category='technical',
        publication_date='02-07-2019',
        source_file='self-driving-vehicle.md',
    )
    featured_article = article1

    technical_articles_template = env.get_template('technical-articles-template.html')
    rendered_tempalte = technical_articles_template.render(
        navbar_items=generate_navbar_items('category'), 
        technical_articles=[article1],
        featured_article=featured_article,
        header_link='../index.html',
    )
    with open('pages/technical-articles.html', 'w') as f:
        f.write(rendered_tempalte)
generate_technical_articles_page()


def generate_article():
    out_file = 'articles/self-driving-vehicle.html'
    out_file_handle = codecs.open(out_file, mode='r', encoding='utf-8')
    body = out_file_handle.read()
    out_file_handle.close()

    article = SingleArticle(title='Types versus Classes', body=body)

    article_template = env.get_template('article-template.html')
    rendered_tempalte = article_template.render(
        article=article, 
        navbar_items=generate_navbar_items('article-details'),
        header_link='../../index.html',
    )
    with open('pages/technical/types-versus-classes.html', 'w', encoding='utf-8') as f:
        f.write(rendered_tempalte)
generate_article()


def find_popular_articles(top_x: int, category: str=None):
    articles = Articles('articles')
    articles.render_markdown_files()
    return articles.get_top_articles_by_attribute_and_category('popularity', category, top_x)
popular_articles = find_popular_articles(2, 'technical')
