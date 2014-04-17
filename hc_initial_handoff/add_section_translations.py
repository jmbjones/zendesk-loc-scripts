import csv
import json
import requests

subdomain = 'your_subdomain'                # setting
email = 'your_email'                        # setting
password = 'your_zd_password'               # setting
session = requests.Session()
session.auth = (email, password)
session.headers = {'Content-Type': 'application/json'}

locales = ['de', 'fr']                     # setting

with open('translated_titles.csv', encoding='utf-8', newline='') as f:
    title_reader = csv.reader(f, delimiter=',')

    sections = {}
    for row in title_reader:
        titles = {}
        count = 1
        for locale in locales:
            titles[locale] = row[count]
            count += 1
        sections[row[0]] = titles

for section in sections:
    url = 'https://{}.zendesk.com/api/v2/help_center/sections/{}/translations.json'.format(subdomain, section)
    for locale in locales:
        data = {'translation': {'locale': locale, 'title': sections[section][locale]}}
        payload = json.dumps(data)
        response = session.post(url, data=payload)
        print("Translation for locale '{}' created for section {}.".format(locale, section))