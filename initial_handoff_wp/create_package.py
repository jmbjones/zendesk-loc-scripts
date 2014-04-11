import os

import requests
from bs4 import BeautifulSoup

subdomain = '{your_subdomain}'              # setting
email = '{your_email}'                      # setting
password = '{your_zd_password}'             # setting
session = requests.Session()
session.auth = (email, password)
session.headers = {'Content-Type': 'application/json'}

forums = ['21535856', '21825876', '33838271']              # setting
ignore = ['23650177', '24919921', '33992907', '44356063']  # setting

file_path = os.path.join('..', 'handoff', 'current')

for forum in forums:
    url = 'https://{}.zendesk.com/api/v2/forums/{}/topics.json'.format(subdomain, forum)
    response = session.get(url)
    if response.status_code != 200:
        print('Failed to get topics in forum {}. Error {}.'.format(forum, response.status_code))
        exit()
    print('Successfully retrieved the topics in forum {}:'.format(forum))
    data = response.json()
    for topic in data['topics']:
        if str(topic['id']) in ignore: continue
        tree = BeautifulSoup('<html></html>')
        body = BeautifulSoup(topic['body'])
        title = tree.new_tag('h1')
        title.string = topic['title']

        tree.html.append(title)
        tree.html.append(body)

        filename = '{}.html'.format(topic['id'])
        with open(os.path.join(file_path, filename), mode='w', encoding='utf-8') as f:
            f.write(tree.prettify())
        print('- Saved "{}" as {}'.format(topic['title'], filename))