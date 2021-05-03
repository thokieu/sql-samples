import sqlite3
import json

conn = sqlite3.connect('RosterData.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Course')
cur.execute('DROP TABLE IF EXISTS Member')
cur.execute('DROP TABLE IF EXISTS User')

cur.execute('CREATE TABLE Course (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, title TEXT UNIQUE)')
cur.execute('CREATE TABLE Member (user_id INTEGER, course_id INTEGER, role INTEGER, PRIMARY KEY (user_id, course_id))')
cur.execute('CREATE TABLE User (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT UNIQUE)')

fname = input('Enter file name: ')
if len(fname) < 1 :
    fname = 'roster_data.json'

rawdata = open(fname).read() # Intermediary file handle; use open('file name').read() command to do so.
jdata = json.loads(rawdata) # You have to insert the data as one continuous string into a variable; here we name it jdata.

for entry in jdata :
    name = entry[0]
    title = entry[1]
    role = entry[2]

    cur.execute('INSERT OR IGNORE INTO User (name) VALUES (?)', (name, ))
    cur.execute('SELECT id FROM User WHERE name = ?', (name, ))
    user_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO Course (title) VALUES (?)', (title, ))
    cur.execute('SELECT id FROM Course WHERE title = ?', (title, ))
    course_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Member (user_id, course_id, role) VALUES (?, ?, ?)''',
        (user_id, course_id, role ))

conn.commit()
