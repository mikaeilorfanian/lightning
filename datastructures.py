import copy
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List

import markdown
from markdown.extensions.wikilinks import WikiLinkExtension

from wiki import wiki_url_builder


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
class ArticleCategory:
    name: str
    page_title: str
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
    output_file: str
    popularity: int = 0
    html_body: str = None
    featured: bool = False

    def __post_init__(self):
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
    def __init__(self, path_to_search: str, site_url: str):
        self.root_path = path_to_search
        self.markdown_files = self.find_markdown_files()
        self.metadata = dict()
        self.summaries = list()
        self.site_url = site_url

    def find_markdown_files(self):
        path = Path('.') / self.root_path
        return [f for f in path.glob('*.md')]

    def render_markdown_files(self):
        for in_file in self.markdown_files:
            out_file = in_file.with_suffix('.html')
            extensions = ['codehilite', 'meta', WikiLinkExtension(build_url=wiki_url_builder), 'nl2br']
            kwargs = dict(input=in_file.as_posix(), output=out_file.as_posix(), extensions=extensions, encoding='utf-8')
            md = markdown.Markdown(**kwargs)
            md.convertFile(kwargs.get('input', None), kwargs.get('output', None), kwargs.get('encoding', None))

            self.metadata[in_file] = md.Meta

            featured = True if md.Meta.get('featured', ['no'])[0] == 'true' else False
            self.summaries.append(
                ArticleSummary(
                    title=md.Meta['title'][0],
                    description=md.Meta['description'][0],
                    link=md.Meta['link'][0].format(url=self.site_url, category=md.Meta['category'][0]),
                    category=md.Meta['category'][0],
                    publication_date=md.Meta['publication_date'][0],
                    popularity=md.Meta['popularity'][0],
                    source_file=in_file,
                    output_file=out_file,
                    featured=featured,
                )
            )

    def get_articles_by_category(self, category: str = None):
        summaries = copy.deepcopy(self.summaries)
        if category:
            return [article for article in summaries if article.category == category]
        else:
            return summaries

    def get_top_articles_by_category_and_sorted_by_attribute(
        self, attribute: str, category: str = None, top_x: int = None
    ):
        articles_in_category = self.get_articles_by_category(category)
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

    def get_featured_article(self, category):
        articles_in_category = self.get_articles_by_category(category)
        featured_articles = [article for article in articles_in_category if article.featured]

        assert len(featured_articles) == 1

        return featured_articles[0]
