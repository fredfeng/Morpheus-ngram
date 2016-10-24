from lxml import html
import requests
from time import sleep
import sqlite3

conn = sqlite3.connect('morpheus.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE topic_tb 
             (url text, title text, vote text, answer text, src text)''')

type1 = 'tidyr'
#for p_num in range(1,246):
for p_num in range(183,184):
    try:
        page = 'http://stackoverflow.com/search?page=' + str(p_num) + '&tab=relevance&q=%5br%5dtidyr' 
        print 'Request------------------', page
        page = requests.get(page)
        tree = html.fromstring(page.content)
        topics = tree.xpath('//*[@class="question-summary search-result"]')
        print len(topics)
        for topic in topics:
            url = topic.xpath('div[2]/div[1]/span/a/@href')
            title = topic.xpath('div[2]/div[1]/span/a/@title')
            vote = topic.xpath('div[1]/div[2]/div[1]/div/span/strong/text()')
            answer = topic.xpath('div[1]/div[2]/div[2]/strong/text()')
            if len(url) == 0 or len(title) == 0 or len(vote) == 0:
                continue

            #print title, ' ', url, ' ', vote, ' ', answer
            # Insert a row of data
            ans = '-2'
            if len(answer) != 0:
                ans = answer[0]

            newT1 = title[0].replace("\"", "")
            sql = "INSERT INTO topic_tb VALUES (\"" + url[0] + "\",\""+ newT1 +"\",\""+ vote[0] +"\",\""+ ans + "\",\"" + type1 +"\")"
            print sql
            c.execute(sql)
            
        # Save (commit) the changes
        conn.commit()

        #sleep for a while
        sleep(4)
    except:
        print "Caught it!"


type2 = 'dplyr'
for p_num in range(1,1200):
    try:
        page = 'http://stackoverflow.com/search?page=' + str(p_num) + '&tab=relevance&q=%5br%5ddplyr'
        print 'Request------------------', page
        page = requests.get(page)
        tree = html.fromstring(page.content)
        topics = tree.xpath('//*[@class="question-summary search-result"]')
        print len(topics)
        for topic in topics:
            url = topic.xpath('div[2]/div[1]/span/a/@href')
            title = topic.xpath('div[2]/div[1]/span/a/@title')
            vote = topic.xpath('div[1]/div[2]/div[1]/div/span/strong/text()')
            answer = topic.xpath('div[1]/div[2]/div[2]/strong/text()')
            if len(url) == 0 or len(title) == 0 or len(vote) == 0:
                continue

            ans = '-2'
            if len(answer) != 0:
                ans = answer[0]

            #print title, ' ', url, ' ', vote, ' ', answer
            # Insert a row of data
            newT2 = title[0].replace("\"", "")
            sql = "INSERT INTO topic_tb VALUES (\"" + url[0] + "\",\""+ newT2 +"\",\""+ vote[0] +"\",\""+ ans + "\",\"" + type2 +"\")"
            print sql
            c.execute(sql)
            
        # Save (commit) the changes
        conn.commit()

        #sleep for a while
        sleep(4)
    except:
        print "Caught it!"




# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
