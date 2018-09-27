import os
from datetime import datetime
from markdown2 import markdown
from jinja2 import Environment, PackageLoader



aboutMD = 'about.md'

with open(aboutMD, 'r') as file:
    parsed_md = markdown(file.read())

    env = Environment(loader=PackageLoader('about', 'templates'))
    about_template = env.get_template('about.html')

    data = {
        'content': parsed_md
    }

    about_html_content = about_template.render(posts = data)
    with open('output/about.html', 'w') as file:
        file.write(about_html_content)