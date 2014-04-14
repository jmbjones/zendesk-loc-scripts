import sqlite3

db = sqlite3.connect('kb.db')

query = '''
    CREATE TABLE topics (
        topic_id        INTEGER PRIMARY KEY     NOT NULL,
        topic_title     TEXT,
        topic_author    INTEGER,
        forum_id        INTEGER,
        topic_de        INTEGER,
        topic_fr        INTEGER,
        topic_ja        INTEGER
    )
'''
db.execute(query)

query = '''
    CREATE TABLE forums (
        forum_id        INTEGER PRIMARY KEY     NOT NULL,
        forum_name      TEXT,
        forum_de        INTEGER,
        forum_fr        INTEGER,
        forum_ja        INTEGER
    )
'''
db.execute(query)
db.close()
print('Tables created successfully')