import os
import glob
import json
import sqlite3

import requests
from bs4 import BeautifulSoup, Comment


def main():
    subdomain = 'your_subdomain'          # setting
    email = 'your_email'                  # setting
    password = 'your_zd_password'         # setting
    session = requests.Session()
    session.auth = (email, password)
    session.headers = {'Content-Type': 'application/json'}

    locales = ('de', 'fr')                  # setting
    for locale in locales:
        print('Processing {} articles ...\n'.format(locale))
        topic_map = get_map(locale)
        files = glob.glob(os.path.join('..', 'handoff', 'localized', locale, '*.html'))
        for file in files:
            print('Reading {} ...'.format(file[24:]))
            payload = create_payload(file)
            url = 'https://{}.zendesk.com/api/v2/topics/{}.json'.format(subdomain, topic_map[int(file[24:-5])])
            put_article(payload, url, session)
            print('https://{}.zendesk.com/entries/{}.html\n'.format(subdomain, topic_map[int(file[24:-5])]))
        print('\n-----\n')

#-------------------------------------------------------------------------------
# FUNCTIONS


def get_map(locale):
    db = sqlite3.connect('kb.db')
    rows = db.execute('SELECT topic_id, topic_{} FROM topics'.format(locale))
    topic_map = {row[0]: row[1] for row in rows}
    db.close()
    return topic_map


def create_payload(file):
    with open(file, mode='r', encoding='utf-8') as f:
        html_source = f.read()

    tree = BeautifulSoup(html_source)
    title = tree.h1.string.strip()
    tree.h1.decompose()

    # Strip out html comments
    comments = tree.find_all(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    # Package the payload in a dict and JSON-encode it
    data = {'topic': {'title': title, 'body': str(tree)}}
    return json.dumps(data)


def put_article(payload, url, session):
    response = session.put(url, data=payload)
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the put request. Exiting.')
        exit()
    print('Topic updated successfully.')


#-------------------------------------------------------------------------------
# RUN SCRIPT

main()