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
size1 = 0
size2 = 0
size3 = 0
size4 = 0
size5 = 0
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
        lenth =0 
        for str in getWords(snippet):
            if str in keywords:
                actual += str + ' '
                lenth = lenth + 1

        if lenth == 1:
            size1 += 1

        if lenth == 2:
            size2 += 1

        if lenth == 3:
            size3 += 1

        if lenth == 4:
            size4 += 1

        if lenth >= 5:
            size5 += 1


        if len(actual) > 1 and lenth > 1:
            print actual

    cnt = cnt + 1

#print 'size1:', size1
#print 'size2:', size2
#print 'size3:', size3
#print 'size4:', size4
#print 'size5:', size5

conn.close()
