from dataclasses import dataclass
from typing import List

from jinja2 import Environment, FileSystemLoader, select_autoescape


env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

@dataclass
class NavbarItem:
    title: str
    link: str = '#'

    # def __post_init__(self):
    #     self.link = 'pages/' + self.link


@dataclass
class HomeArticle:
    title: str
    description: str
    link: str
    category: str

    def __post_init__(self):
        self.link = self.category + '/' + self.link


@dataclass
class HomeCard:
    title: str
    articles: List[HomeArticle]


intro = NavbarItem(title='Intro', link='home.html')
technical = NavbarItem(title='Technical', link='technical-articles-list.html')
employment = NavbarItem(title='Employment')
navbar_items = (intro, technical, employment)

article1 = HomeArticle(
    title='Types versus Classes', 
    description='The type of an object differs from its class and OOP relies a lot on this difference!',
    link='types-versus-classes.html',
    category='top-coder-technical',
)
coder_card = HomeCard(title='Top 1% coder', articles=[article1])
home_template = env.get_template('home2-template.html')
rendered_tempalte = home_template.render(navbar_items=navbar_items, home_cards=[coder_card])
with open('pages/home.html', 'w') as f:
    f.write(rendered_tempalte)


article1 = HomeArticle(
    title='Types versus Classes', 
    description='The type of an object differs from its class and OOP relies a lot on this difference!',
    link='types-versus-classes.html',
    category='top-coder-technical',
)
latest_article = article1
technical_articles_template = env.get_template('technical-articles-list-template.html')
rendered_tempalte = technical_articles_template.render(
    navbar_items=navbar_items, 
    technical_articles=[article1], 
    latest_article=latest_article
)

with open('pages/technical-articles-list.html', 'w') as f:
    f.write(rendered_tempalte)


technical_articles_template = env.get_template('technical-articles-list-template.html')
rendered_tempalte = technical_articles_template.render(navbar_items=navbar_items)

with open('pages/technical-articles-list.html', 'w') as f:
    f.write(rendered_tempalte)
