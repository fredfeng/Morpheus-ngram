from lxml import html
import requests
import sqlite3
from time import sleep

base_url = 'http://stackoverflow.com'

conn = sqlite3.connect('morpheus11.db')

c = conn.cursor()
# Create table

for row in c.execute('SELECT count(*) FROM post_tb'):
    code = row[0]
    print code

conn.close()
