import dataclasses
import logging
import sys
from typing import List


logging.basicConfig(level=logging.INFO)


@dataclasses.dataclass
class Config:
    cmd_args: List[str]
    cmd_arg_local_env: str = 'local'

    TOP_X_ARTICLES: int = 5

    FINAL_PAGES_DIR: str = 'pages'
    RAW_ARTICLES_DIR: str = 'articles'

    ROOT_BLOG_URL_LOCAL: str = 'file:///C:/Users/mokt/dev/blog'
    ROOT_BLOG_URL_PROD: str = 'https://mikaeilorfanian.github.io'

    templates_folder: str = 'templates'

    home_page_template: str = 'home-template.html'
    about_page_template: str = 'about-template.html'
    wiki_page_template: str = 'wiki-template.html'
    projects_page_template: str = 'projects-template.html'

    blog_root_url: str = ''

    wiki_page: str = 'wiki.html'
    index_page: str = 'index.html'
    about_page: str = 'about.html'
    projects_page: str = 'projects.html'

    wiki_page_md: str = 'wiki.md'

    def __post_init__(self):
        if len(self.cmd_args) == 2:
            site_url = (
                self.ROOT_BLOG_URL_LOCAL
                if self.cmd_args[1] == self.cmd_arg_local_env
                else self.ROOT_BLOG_URL_PROD
            )
        else:
            site_url = self.ROOT_BLOG_URL_LOCAL

        self.blog_root_url = site_url

        logging.info(f'Root URL: {self.blog_root_url}')


config = Config(sys.argv)
