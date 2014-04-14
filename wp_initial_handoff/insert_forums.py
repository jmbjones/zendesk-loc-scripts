import sqlite3
import requests

subdomain = 'your_subdomain'              # setting
email = 'your_email'                      # setting
password = 'your_zd_password'             # setting
session = requests.Session()
session.auth = (email, password)
session.headers = {'Content-Type': 'application/json'}

forums = ['21525876', '23000267']           # setting

rows = []
for forum in forums:
    url = 'https://{}.zendesk.com/api/v2/forums/{}.json'.format(subdomain, forum)
    response = session.get(url)
    data = response.json()
    row = forum, data['forum']['name']
    rows.append(row)

db = sqlite3.connect('kb.db')
query = 'INSERT INTO forums (forum_id, forum_name) VALUES (?, ?)'
db.executemany(query, rows)
db.commit()
print("Rows inserted successfully")
db.close()