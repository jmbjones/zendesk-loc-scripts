import sqlite3
import json
import requests

subdomain = '{your_subdomain}'              # setting
email = '{your_email}'                      # setting
password = '{your_zd_password}'             # setting
session = requests.Session()
session.auth = (email, password)
session.headers = {'Content-Type': 'application/json'}

db = sqlite3.connect('kb.db')
rows = db.execute('''
          SELECT topic_id, topic_title, topic_author, forum_de, forum_fr
          FROM topics, forums
          WHERE topics.forum_id = forums.forum_id
          ''')
topics = [(row[0], row[1], row[2], (row[3], row[4])) for row in rows]     # setting
db.close()

rows = []
url = 'https://{}.zendesk.com/api/v2/topics.json'.format(subdomain)
for topic in topics:
    new_topics = []
    for forum in topic[3]:
        data = {'topic': {'title': topic[1], 'body': 'Content at translation.',
                    'submitter_id': topic[2], 'forum_id': forum}}
        payload = json.dumps(data)
        response = session.post(url, data=payload)
        data = response.json()
        new_topics.append(data['topic']['id'])
    new_topics.append(topic[0])
    rows.append(tuple(new_topics))

db = sqlite3.connect('kb.db')
query = 'UPDATE topics SET topic_de = ?, topic_fr = ? WHERE topic_id = ?'   # setting
db.executemany(query, rows)
db.commit()
print('Topics created and rows updated successfully.')
db.close()