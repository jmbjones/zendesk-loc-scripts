import os

import requests
from bs4 import BeautifulSoup

subdomain = 'your_subdomain'                # setting
email = 'your_email'                        # setting
password = 'your_zd_password'               # setting
session = requests.Session()
session.auth = (email, password)
session.headers = {'Content-Type': 'application/json'}

locale = 'en-us'                            # setting

sections = ['36406', '200122006']                # setting
# ignore = ['23650177', '33992907', '44356063']  # setting
ignore = []                                      # setting

file_path = os.path.join('..', 'handoff', 'current')

for section in sections:
    articles = []
    url = 'https://{}.zendesk.com/api/v2/help_center/sections/{}/articles.json'.format(subdomain, section)
    response = session.get(url)
    if response.status_code != 200:
        print('Failed to get articles in section {}. Error {}.'.format(section, response.status_code))
        exit()
    print('\nSuccessfully retrieved the articles in section {}:'.format(section))
    data = response.json()
    [articles.append(article['id']) for article in data['articles']]

    for article in articles:
        if str(article) in ignore: continue
        url = 'https://{}.zendesk.com/api/v2/help_center/articles/{}/translations/{}.json'.format(subdomain, article, locale)
        response = session.get(url)
        data = response.json()
        tree = BeautifulSoup('<html></html>')
        body = BeautifulSoup(data['translation']['body'])
        title = tree.new_tag('h1')
        title.string = data['translation']['title']

        tree.html.append(title)
        tree.html.append(body)

        filename = '{}.html'.format(article)
        with open(os.path.join(file_path, filename), mode='w', encoding='utf-8') as f:
            f.write(tree.prettify())
        print('- Saved "{}" as {}'.format(data['translation']['title'], filename))
