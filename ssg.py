import os
from datetime import datetime
from markdown2 import markdown
from jinja2 import Environment, PackageLoader

POSTS = {}
for markdown_post in os.listdir('content'):
    file_path = os.path.join('content', markdown_post)

    with open(file_path, 'r') as file: #content/senior.md
        POSTS[markdown_post] = markdown(file.read(), extras=['metadata'])
        # print(POSTS)
    POSTS = {
        post: POSTS[post] for post in sorted(POSTS, key=lambda post: datetime.strptime(POSTS[post].metadata['date'], '%Y-%m-%d  %H:%M'), reverse=True)
    }   
    print(POSTS[0:1])

    env = Environment(loader=PackageLoader('ssg', 'templates'))
    index_template = env.get_template('index.html')
    post_template = env.get_template('post-detail.html')

    index_posts_metadata = [POSTS[post].metadata for post in POSTS]

    index_html_content = index_template.render(posts=index_posts_metadata)

    with open('output/index.html', 'w') as file:
        file.write(index_html_content)

'''
with open('content/senior.md', 'r') as file:
    parsed_md = markdown(file.read(), extras=['metadata'])

    print('Metadata: ', parsed_md.metadata)
    print('Content: ', parsed_md)

    env = Environment(loader=PackageLoader('ssg', 'templates'))
    post_detail_template = env.get_template('post-detail.html')

    data = {
        'content': parsed_md,
        'title': parsed_md.metadata['title'],
        'date': parsed_md.metadata['date'],
        'author': parsed_md.metadata['author']
    }

    print(post_detail_template.render(post=data))
'''