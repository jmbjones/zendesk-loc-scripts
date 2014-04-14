import sqlite3
import json
import requests

subdomain = 'your_subdomain'              # setting
email = 'your_email'                      # setting
password = 'your_zd_password'             # setting
session = requests.Session()
session.auth = (email, password)
session.headers = {'Content-Type': 'application/json'}

# Fetch the available locales for your account
url = 'https://{}.zendesk.com/api/v2/locales.json'.format(subdomain)
response = session.get(url)
data = response.json()
locale_names = [locale['name'] for locale in data['locales'] if locale['name'] != 'English'] # setting

# Create the language-specific categories
new_categories = []
url = 'https://{}.zendesk.com/api/v2/categories.json'.format(subdomain)
for locale in locale_names:
    name = 'Documentation - {}'.format(locale)
    data = {'category': {'name': name}}
    payload = json.dumps(data)
    response = session.post(url, data=payload)
    data = response.json()
    new_categories.append(data['category']['id'])
print("Categories created successfully.")

# Create the forums
db = sqlite3.connect('kb.db')
rows = db.execute('SELECT forum_id, forum_name FROM forums')
forums = {row[0]: row[1] for row in rows}
db.close()

rows = []
url = 'https://{}.zendesk.com/api/v2/forums.json'.format(subdomain)
for forum in forums:
    new_forums = []
    for category in new_categories:
        data = {'forum': {'name': forums[forum],
                            'forum_type': 'articles',
                            'category_id': category,
                            'access': 'agents only'}}
        payload = json.dumps(data)
        response = session.post(url, data=payload)
        data = response.json()
        new_forums.append(data['forum']['id'])
    new_forums.append(forum)
    rows.append(tuple(new_forums))
print("Forums created successfully.")

# Update the database with the new forum ids
db = sqlite3.connect('kb.db')
query = 'UPDATE forums SET forum_de = ?, forum_fr = ? WHERE forum_id = ?'   # setting
db.executemany(query, rows)
db.commit()
print('Rows updated successfully.')
db.close()