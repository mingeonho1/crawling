import requests
from bs4 import BeautifulSoup
import time
import datetime
import sys, os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
sys.path.append(os.path.abspath(os.getcwd() + '../../../../'))
from config.config_del_chk import *

today = datetime.date.today() + datetime.timedelta(days=1)
today_3_ago = today - datetime.timedelta(days=3)

query = QUERY()

conn = DB()
cursor = conn.cursor()

cursor.execute(query, ("THEQOO", "1", today_3_ago, today))
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
            # driver.get(url)
            # try:
            #     WebDriverWait(driver, 15).until(
            #         EC.presence_of_element_located((By.ID, "siteTitle"))
            #     )
            # finally:
            #     print("디도스 페이지 넘어감!")
            response = requests.get(url, headers=headers[0], timeout=5)
            time.sleep(1)
            soup = BeautifulSoup(response.content, 'html.parser')
            contents = soup.select_one("div.btm_area.clear")
            didos = soup.select_one("#cf-content > h1 > span")
            if not contents:
                if not didos:
                    update_delete_chk(row[0])
                else:
                    print('didos페이지 넘어감..')
            else:
                print("= undeleted")
        except Exception as e:
            print(e)


crawling()
conn.close()

#DB에 모든 데이터에 삭제페이지가 없어서 대충 예상으로 select 작성함