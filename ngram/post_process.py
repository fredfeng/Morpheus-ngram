import requests
import sqlite3
from time import sleep
import re

def getWords(text):
    return re.compile('\w+').findall(text)

conn = sqlite3.connect('morpheus11.db')
c = conn.cursor()
divider = '#morpheus#'
keywords = ['arrange', 'cbind', 'rbind', 'filter', 'gather', 'group_by', 'inner_join', 'mutate', 'select', 'separate', 'spread', 'summarise', 'unite']

cnt = 1
for row in c.execute('SELECT code,myurl FROM post_tb'):
#    if cnt > 50:
#        break
    code = row[0]
    url = row[1]
    #print '==========================================', url
    #print code.encode('utf8')
    for snippet in code.split(divider):
        snippet = snippet.replace('summarize', 'summarise')
        snippet = snippet.replace('summarise_each', 'summarise')
        snippet = snippet.replace('regroup', 'group_by')
        snippet = snippet.replace('group_by_', 'group_by')
        snippet = snippet.replace('merge', 'inner_join')
        actual = ''
        for str in getWords(snippet):
            if str in keywords:
                actual += str + ' '

        if len(actual) > 1:
            print actual

    cnt = cnt + 1

conn.close()
