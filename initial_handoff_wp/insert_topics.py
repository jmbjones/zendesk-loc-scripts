import sqlite3
import requests

subdomain = '{your_subdomain}'              # setting
email = '{your_email}'                      # setting
password = '{your_zd_password}'             # setting
session = requests.Session()
session.auth = (email, password)
session.headers = {'Content-Type': 'application/json'}

db = sqlite3.connect('kb.db')
rows = db.execute('SELECT forum_id, forum_name FROM forums')
forums = {row[0]: row[1] for row in rows}
db.close()

ignore = ['23650177', '24919921', '33992907', '44356063']    # setting

rows = []
for forum in forums:
    url = 'https://{}.zendesk.com/api/v2/forums/{}/topics.json'.format(subdomain, forum)
    response = session.get(url)
    data = response.json()
    for topic in data['topics']:
        if str(topic['id']) in ignore: continue
        row = topic['id'], topic['title'], topic['submitter_id'], forum
        rows.append(row)

db = sqlite3.connect('kb.db')
query = 'INSERT INTO topics (topic_id, topic_title, topic_author, forum_id) VALUES (?, ?, ?, ?)'
db.executemany(query, rows)
db.commit()
print("Rows inserted successfully")
db.close()