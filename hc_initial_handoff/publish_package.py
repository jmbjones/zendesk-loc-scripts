import os
import glob
import json

import requests
from bs4 import BeautifulSoup, Comment


def main():
    subdomain = 'your_subdomain'            # setting
    email = 'your_email'                    # setting
    password = 'your_zd_password'           # setting
    session = requests.Session()
    session.auth = (email, password)
    session.headers = {'Content-Type': 'application/json'}

    locales = ('de', 'fr')                 # setting

    for locale in locales:
        print('Processing {} articles ...\n'.format(locale))
        files = glob.glob(os.path.join('..', 'handoff', 'localized', locale, '*.html'))
        path_len = 22 + len(locale)
        for file in files:
            print('Reading {}/{} ...'.format(locale, file[path_len:]))
            payload = create_payload(locale, file)
            url = 'https://{}.zendesk.com/api/v2/help_center/articles/{}/translations.json'.format(subdomain, file[path_len:-5])
            post_translation(payload, url, session)
            print('https://{}.zendesk.com/hc/{}/articles/{}.html\n'.format(subdomain, locale, file[path_len:-5]))
        print('\n-----\n')

#-------------------------------------------------------------------------------
# FUNCTIONS


def create_payload(locale, file):
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
    data = {'translation': {'locale': locale, 'title': title, 'body': str(tree)}}
    return json.dumps(data)


def post_translation(payload, url, session):
    response = session.post(url, data=payload)
    if response.status_code != 201:
        print('Status:', response.status_code, 'Problem with the post request. Exiting.')
        exit()
    print('Translation created successfully.')

#-------------------------------------------------------------------------------
# RUN SCRIPT

main()
