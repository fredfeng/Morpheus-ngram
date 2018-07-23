from lxml import html
from lxml import etree
import requests
from time import sleep
import sqlite3

conn = sqlite3.connect('hacker_rank.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE hr_sol_tb 
             (problem text, author text, language text, score text, url text, solution text)''')

payload = {
    'login': 'yufeng.austin@gmail.com',
    'password': 'utaustin1'
}

loginPage = 'https://www.hackerrank.com/auth/login'
website = 'https://www.hackerrank.com'
problem = 'diagonal-difference'

cook = 'session_referring_domain=www.google.com; session_landing_url=https%3A%2F%2Fwww.hackerrank.com%2Fprefetch_data%3Fcontest_slug%3Dmaster%26get_feature_feedback_list%3Dtrue; default_cdn_url=hrcdn.net; cdn_url=hrcdn.net; cdn_set=true; __utmc=74197771; enableIntellisenseUserPref=true; hacker_editor_theme=light; session_referrer=https%3A%2F%2Fwww.google.com%2Furl%3Fq%3Dhttps%3A%2F%2Fwww.hackerrank.com%2Fchallenges%2Fdiagonal-difference%2Fproblem%26sa%3DD%26source%3Dhangouts%26ust%3D1532384710444000%26usg%3DAFQjCNHtNJElErmTo6e3H4EgRQh_C-NlNA; __utma=74197771.1151075130.1530743365.1532298320.1532298361.5; __utmz=74197771.1532298361.5.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=https://www.hackerrank.com/challenges/diagonal-difference/problem; hackerrank_mixpanel_token=48f14e30-b95d-41b5-947c-94b2e66eea53; _hrank_session=a23eb6516400b4aa9c508dba164fca59563847356ea2ac4a8eacc0dc5a86227cc7bd51884854fe62fdfc6535869f6bf0a890bfa6ef5cf994995ada4a48ecd27b; mp_bcb75af88bccc92724ac5fd79271e1ff_mixpanel=%7B%22distinct_id%22%3A%20%2248f14e30-b95d-41b5-947c-94b2e66eea53%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%2C%22mp_keyword%22%3A%20%22https%3A%2F%2Fwww.hackerrank.com%2Fchallenges%2Fdiagonal-difference%2Fproblem%22%7D; mp_86cf4681911d3ff600208fdc823c5ff5_mixpanel=%7B%22distinct_id%22%3A%20%22164676a1f6451c-079b6cd9fcf592-163b6953-1fa400-164676a1f65ff1%22%2C%22%24search_engine%22%3A%20%22google%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.google.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.google.com%22%2C%22mp_keyword%22%3A%20%22https%3A%2F%2Fwww.hackerrank.com%2Fchallenges%2Fdiagonal-difference%2Fproblem%22%7D; react_var=false__cnt5; react_var2=false__cnt5; metrics_user_identifier=448096-702dd0de8ad6de97672a0a083ec6381dd3d8583d'

with requests.Session() as s:
    p = s.post(loginPage, data=payload)
    # print the html returned or something more intelligent to see if it's a successful login page.
    head = {'cookie': cook, 'X-CSRF-Token': p.json()['csrf_token']}
    unlock_url = website + '/rest/contests/master/challenges/' + problem + '-difference/unlock_solution'
    s.get(unlock_url, headers=head)

    for p_num in range(330,24000):
        try:
            page_url = website + '/challenges/' + problem + '/leaderboard?page=' + str(p_num)
            #page = 'https://www.hackerrank.com/challenges/diagonal-difference/leaderboard?page=' + str(p_num) 
            print 'Request------------------', page_url
            page = s.get(page_url, headers=head)
            #print page.content
            tree = html.fromstring(page.content)

            topics = tree.xpath('//*[@class="table-row flex"]')
            print len(topics)
            for topic in topics:
                hacker_list = topic.xpath('div[1]/div[1]/a/text()')
                if not hacker_list:
                    continue
                hacker = hacker_list[0]
                lang_list = topic.xpath('div[4]/div[1]/text()')
                if not lang_list:
                    continue
                language = lang_list[0]
                score_list = topic.xpath('div[5]/div[1]/text()')
                if not score_list:
                    continue
                score = score_list[0]
                url_list =topic.xpath('div[6]/span/a/@href')
                if not url_list:
                    continue
                url = website + url_list[0]

                print 'hacker: ' + hacker
                print 'language: ' + language
                print 'score: ' + score
                print 'url: ' + url
                if language == 'C' and score == '10.00':
                    resp_code = s.get(url, headers=head)
                    code = resp_code.content
                    sol = resp_code.text
                    sol = sol.replace('"', '\""')
                    # Insert a row of data
                    sql = "INSERT INTO hr_sol_tb VALUES (\"" + problem + "\",\""+ hacker +"\",\""+ language +"\",\""+ score + "\",\"" + url + "\",\"" + sol +"\")"
                    #print sql
                    c.execute(sql)
                
            # Save (commit) the changes
            if p_num % 20 == 0:
                conn.commit()

            #sleep for a while
            sleep(1)
        except:
            print "Caught it! Stop at page " + str(p_num)
            conn.commit()
            raise

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
