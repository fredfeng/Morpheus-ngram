import requests
import sqlite3
from time import sleep
import re

def getWords(text):
    return re.compile('\w+').findall(text)

conn = sqlite3.connect('morpheus_final.db')
c = conn.cursor()
divider = '#morpheus#'
keywords = ['arrange','cbind', 'rbind', 'mutate', 'filter', 'gather', 'group_by', 'inner_join', 'select', 'separate', 'spread', 'summarise', 'unite']

cnt = 1
#for row in c.execute("SELECT code,myurl FROM post_tb where code LIKE '%mutate%' and code LIKE '%ratio%' and code LIKE '%Ratio%'"):
#for row in c.execute("SELECT code,myurl FROM post_tb where code LIKE '%summarise%' and code LIKE '%filter%' and (code LIKE '%sum%' or code LIKE '%min%' or code LIKE '%mean%')"):
for row in c.execute("SELECT code,myurl FROM post_tb where code LIKE '%gather%' and code LIKE '%filter%'"):
#    if cnt > 50:
#        break
    code = row[0]
    url = row[1]
    print '==========================================', url
    print code.encode('utf8')
    cnt = cnt + 1

conn.close()
