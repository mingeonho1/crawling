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

cursor.execute(query, ("TIKTOK", "1", today_3_ago, today))
select_result = cursor.fetchall()
headers = [{
    'User-Agent': UserAgent()
}]


def update_delete_chk(idx):
    print("삭제된 글")
    query2 = "UPDATE main_data " \
             "SET Delete_chk = 1 " \
             "WHERE Main_idx = %s "
    cursor.execute(query2, idx)
    conn.commit()
    print("Del_chk 업뎃 성공!")


def crawling():
    for row in select_result:
        url = row[5]
        print(url)
        try:
            response = requests.get(url, headers=headers[0], timeout=5)
            time.sleep(1)
            soup = BeautifulSoup(response.content, 'html.parser')
            contents = soup.select_one('#app > div.tiktok-19fglm-DivBodyContainer.eg65pf90 > \
            div.tiktok-yp78ys-DivMainContainer.eueotzt0 > div.tiktok-u2vwc1-DivErrorWrapper.eueotzt1 > div')
            if contents:
                update_delete_chk(row[0])
            else:
                print("= undeleted")
        except Exception as e:
            print(e)


crawling()
conn.close()