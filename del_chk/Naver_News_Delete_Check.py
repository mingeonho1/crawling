import requests
from bs4 import BeautifulSoup
import time
import datetime
import sys, os
sys.path.append(os.path.abspath(os.getcwd() + '../../../../'))
from config.config_del_chk import *

today = datetime.date.today() + datetime.timedelta(days=1)
today_3_ago = today - datetime.timedelta(days=3)

query = QUERY()

conn = DB()
cursor = conn.cursor()

cursor.execute(query, ("NAVER", "N", today_3_ago, today))
select_result = cursor.fetchall()
headers = [{
    'User-Agent': UserAgent()
}]


def update_delete_chk(idx):
    print("삭제된 글")
    conn = DB()
    cursor = conn.cursor()
    query2 = "UPDATE main_data " \
             "SET Delete_chk = 1 " \
             "WHERE Main_idx = %s "
    cursor.execute(query2, idx)
    conn.commit()
    print("Del_chk 업뎃 성공!")
    conn.close()


def crawling():
    for row in select_result:
        url = row[5]
        print(url)
        try:
            response = requests.get(url, headers=headers[0], timeout=5)
            time.sleep(0.2)
            soup = BeautifulSoup(response.content, 'html.parser')
            sports = soup.select_one("#article_title")
            content = soup.select_one("#content > div.end_ct > div > div.press_logo > a > img")
            h1 = soup.select_one("#fusion-app > div.article.\| > div:nth-child(2) > div > div > div.article-header__headline-container.\|.box--pad-left-md.box--pad-right-md > h1")
            contents = soup.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_top > a > img.media_end_head_top_logo_img.light_type")
            if not (contents or content or sports or h1):
                update_delete_chk(row[0])
            else:
                print("= undeleted")
        except Exception as e:
            print(e)


crawling()
conn.close()

#아직 삭제페이지를 못봐서 일단 어떻게 될 지 모름(일단 완성)