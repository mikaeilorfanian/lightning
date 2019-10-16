# Lightning: site generator framework
Lightning is a modern framework for generating static sites. It's a brand new project taking advantage of the latest features of Python. Batteries included, and it's easy to extend it and read its source code. Here's what you get out of the box:   
- Write in Markdown
- Add your own html, css, and JS files
- Or, customize the built-in mobile friendly template
- Organize pages or articles using "categories"
- Promote the latest and most popular pages
- Generate a wiki page automatically

# How to use it
Install the dependencies in `requirements.txt` in a Python virtual environment.   
Start reading the `Config` class. Then go to `main.py` and see how the `Articles`class works. Then understand what happens in the `__main__` block of `main.py`.   
To generate site for local env, Set `Config.ROOT_BLOG_URL_LOCAL` to the path where this project is downloaded, then run:      
`python main.py`
To generate for prod env, set `Config.ROOT_BLOG_URL_PROD` to your prod env's root URL and run:   
`python main.py prod`

