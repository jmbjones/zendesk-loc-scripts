import sqlite3
import json
import requests

subdomain = 'your_subdomain'          # setting
email = 'your_email'                  # setting
password = 'your_zd_password'         # setting
session = requests.Session()
session.auth = (email, password)
session.headers = {'Content-Type': 'application/json'}

locales = ['de', 'fr']                  # setting

# Fetch the locale ids for your account
url = 'https://{}.zendesk.com/api/v2/locales.json'.format(subdomain)
response = session.get(url)
data = response.json()
locale_ids = [locale['id'] for locale in data['locales'] if locale['name'] != 'English']

# Verify that your locale list has the same number of locales
if len(locales) != len(locale_ids):
    print("Locales don't match. Exiting.")
    exit()

count = 0
for locale in locales:
    db = sqlite3.connect('kb.db')
    rows = db.execute('SELECT forum_{} FROM forums'.format(locale))
    forums = [row[0] for row in rows]
    db.close()
    data = {'forum': {'access': 'everybody', 'locale_id': locale_ids[count]}}   # setting
    payload = json.dumps(data)
    for forum in forums:
        url = 'https://{}.zendesk.com/api/v2/forums/{}.json'.format(subdomain, forum)
        response = session.put(url, data=payload)
        if response.status_code != 200:
            Print('Status:', response.status_code, 'Problem with the put request. Exiting.')
            exit()
        print('Forum {} successfully updated.'.format(forum))
    count += 1