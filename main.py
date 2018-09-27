import os
from datetime import datetime
from markdown2 import markdown
from jinja2 import Environment, PackageLoader
import shutil
import logging
import argparse


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def home():
    logger.info('Creating index')
    POSTS = {}
    for markdown_post in os.listdir('content'):
        file_path = os.path.join('content', markdown_post) #Where markdown posts are stored...

        with open(file_path, 'r') as file: #content/senior.md
            POSTS[markdown_post] = markdown(file.read(), extras=['metadata'])
            # print(POSTS)
        POSTS = {
            post: POSTS[post] for post in sorted(POSTS, key=lambda post: datetime.strptime(POSTS[post].metadata['date'], '%Y-%m-%d  %H:%M'), reverse=True)
        }  
    
        for post in POSTS:
            post_metadata = POSTS[post].metadata

            post_data = {
                'content': POSTS[post],
                'title': post_metadata['title'],
                'date': post_metadata['date'],
            }
    print(post_data)
    # print(list(post_data.keys())[0])

def index():
    logger.info('Creating index')
    POSTS = {}
    for markdown_post in os.listdir('content'):
        file_path = os.path.join('content', markdown_post) #Where markdown posts are stored...

        with open(file_path, 'r') as file: #content/senior.md
            POSTS[markdown_post] = markdown(file.read(), extras=['metadata'])
            # print(POSTS)
        POSTS = {
            post: POSTS[post] for post in sorted(POSTS, key=lambda post: datetime.strptime(POSTS[post].metadata['date'], '%Y-%m-%d  %H:%M'), reverse=True)
        }     # Stores posts in reverse order
        
        env = Environment(loader=PackageLoader('main', 'templates'))
        index_template = env.get_template('index.html')
        post_template = env.get_template('post-detail.html')

        index_posts_metadata = [POSTS[post].metadata for post in POSTS] #metadata of posts
        index_html_content = index_template.render(posts=index_posts_metadata)

        with open('output/index.html', 'w') as file:
            file.write(index_html_content)
        
        for post in POSTS:
            post_metadata = POSTS[post].metadata

            post_data = {
                'content': POSTS[post],
                'title': post_metadata['title'],
                'date': post_metadata['date'],
            }
    
            post_html_content = post_template.render(post=post_data)

            post_file_path = 'output/posts/{slug}.html'.format(slug=post_metadata['slug']) #{slug}/{slug}.html Where files are stored...

            os.makedirs(os.path.dirname(post_file_path), exist_ok=True) #makes the files
            with open(post_file_path, 'w') as file:
                file.write(post_html_content)

def about():
    logger.info('Creating about')
    aboutMD = 'about.md'
    with open(aboutMD, 'r') as file:
        parsed_md = markdown(file.read())

    env = Environment(loader=PackageLoader('main', 'templates'))
    about_template = env.get_template('about.html')

    data = {
        'content': parsed_md
    }

    about_html_content = about_template.render(posts = data)
    with open('output/about.html', 'w') as file:
        file.write(about_html_content)

def contact():
    logger.info('Creating contact')
    contactMD = 'contact.md'
    with open(contactMD, 'r') as file:
        parsed_md = markdown(file.read())

    env = Environment(loader=PackageLoader('main', 'templates'))
    about_template = env.get_template('contact.html')

    data = {
        'content': parsed_md
    }

    about_html_content = about_template.render(posts = data)
    with open('output/contact.html', 'w') as file:
        file.write(about_html_content)

def deleteOutput():
    '''Delete the output folder content'''
    logger.info('Deleting Output folder content')
    shutil.rmtree('output')
    os.mkdir('output')

def createFiles():
    '''Command to create all the files'''
    logger.info('Creating file structure')
    index()
    about()
    contact()

home()
# createFiles()
# deleteOutput()

'''
parser = argparse.ArgumentParser()
subParsers = parser.add_subparsers()

createParser = subParsers.add_parser('create')
createParser.set_defaults(func = createFiles())

createParser = subParsers.add_parser('clean')
createParser.set_defaults(func = deleteOutput())
'''