from lxml import html
import requests
import sqlite3
from time import sleep

base_url = 'http://stackoverflow.com'

conn = sqlite3.connect('morpheus11.db')
conn2 = sqlite3.connect('morpheus11.db')

keywords = ['cbind', 'rbind', 'filter', 'gather', 'group_by', 'inner_join', 'mutate', 'select', 'separate', 'spread', 'summarise', 'unite']

c = conn.cursor()
c2 = conn2.cursor()
# Create table
c.execute('''CREATE TABLE post_tb 
             (myurl text, offset text, vote text, code text)''')

cnt = 1
urls = []
for row in c.execute('SELECT url FROM topic_tb'):
    myurl = base_url + row[0]
    urls.append(myurl)

conn.close()

for myurl in urls:
    try:
        print 'Request------------------', 'index:', cnt, myurl
        cnt = cnt + 1
        page = requests.get(myurl)
        tree = html.fromstring(page.content)
        accept_ans = tree.xpath('//*[@class="answer accepted-answer"]')
        other_ans = tree.xpath('//*[@class="answer"]')

        if len(accept_ans) > 0:
            accept_code_list = accept_ans[0].xpath('table/tr[1]/td[2]/div/pre/code/text()')

            acp_vote = '-2'
            acp_vote_list = accept_ans[0].xpath('table/tr[1]/td[1]/div/span[1]/text()')
            if len(acp_vote_list) > 0:
                acp_vote = acp_vote_list[0]

            acpt_code = "#morpheus#".join(accept_code_list)
            flag = False
            for key in keywords:
                if key in acpt_code:
                    flag = True
                    break

            if len(accept_code_list) > 0 and flag:
                #print 'acpt:', acpt_code, 'vote:', acp_vote
                acpt_code = acpt_code.replace("\"", "")
                sql = "INSERT INTO post_tb VALUES (\"" + row[0] + "\",\""+ str(1) +"\",\""+ acp_vote +"\",\""+ acpt_code + "\")"
                #print sql
                c2.execute(sql)

        num = 2
        for other in other_ans:
            other_code = other.xpath('table/tr[1]/td[2]/div/pre/code/text()')
            if len(other_code) == 0:
                continue

            other_vote_list = other.xpath('table/tr[1]/td[1]/div/span[1]/text()')
            other_vote = '-2'
            if len(other_vote_list) > 0:
                other_vote = other_vote_list[0]

            #print '------------------------------------'
            others = "#morpheus#".join(other_code)
            flag = False
            for key in keywords:
                if key in others:
                    flag = True
                    break

            if not flag:
                continue
            #print 'other:', others, 'vote:', other_vote

            others = others.replace("\"", "")
            sql = "INSERT INTO post_tb VALUES (\"" + row[0] + "\",\""+ str(num) +"\",\""+ other_vote +"\",\""+ others + "\")"
            #print sql
            c2.execute(sql)
            num = num +1

        conn2.commit()
        sleep(5)

    except Exception as inst:
        print "Exception!", inst

conn2.close()

#page = 'http://stackoverflow.com/questions/29679381/tidyr-wide-to-long'
#page = 'http://stackoverflow.com/questions/29775461/tidyr-repeated-measures-multiple-variables-wide-format'

