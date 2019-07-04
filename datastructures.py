import copy
from dataclasses import dataclass
from datetime import datetime
import glob
from typing import List

import markdown


@dataclass
class Page:
    title: str
    page_name: str
    root: str = None

    @property
    def link(self):
        if self.root:
            return self.root + '/' + self.page_name + '.html'
        else:
            return self.page_name + '.html'


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
    source_file: str
    popularity: int = 0
    root: str = None

    def __post_init__(self):
        if self.root:
            self.link = self.root + '/' + self.category + '/' + self.link
        else:
            self.link = self.category + '/' + self.link
        self.publication_date = datetime.strptime(self.publication_date, '%d-%m-%Y')


@dataclass
class HomeCard:
    title: str
    articles: List[ArticleSummary]


@dataclass
class SingleArticle:
    title: str
    body: str


class Articles:

    def __init__(self, path_to_search: str):
        self.root_path = path_to_search
        self.markdown_files = self.find_markdown_files()
        self.metadata = dict()
        self.summaries = list()

    def find_markdown_files(self):
        return [f for f in glob.glob(f'{self.root_path}/*.md')]

    def render_markdown_files(self):
        for in_file in self.markdown_files:
            extensions = ['codehilite', 'meta']
            kwargs = dict(
                input=in_file, 
                output=in_file.split('.md')[0]+'.html', 
                extensions=extensions, 
                encoding='utf-8',
            )
            md = markdown.Markdown(**kwargs)
            md.convertFile(kwargs.get('input', None),
                        kwargs.get('output', None),
                        kwargs.get('encoding', None))

            self.metadata[in_file] = md.Meta

            self.summaries.append(ArticleSummary(
                title=md.Meta['title'][0], 
                description=md.Meta['description'][0],
                link=md.Meta['page_name'][0],
                category=md.Meta['category'][0],
                publication_date=md.Meta['publication_date'][0],
                popularity=md.Meta['popularity'][0],
                source_file=in_file,
            ))

    def get_top_articles_by_attribute_and_category(self, attribute: str, category: str, top_x: int=None):
        summaries = copy.deepcopy(self.summaries)
        articles_in_category = [article for article in summaries if article.category == category]

        if attribute == 'publication_date':
            articles_in_category.sort(key=lambda article: article.publication_date, reverse=True)
        elif attribute == 'popularity':
            articles_in_category.sort(key=lambda article: article.popularity, reverse=True)
        else:
            raise ValueError(f'Sorting by {attribute} not supported!')

        if top_x:
            return articles_in_category[:top_x]
        else:
            return articles_in_category
