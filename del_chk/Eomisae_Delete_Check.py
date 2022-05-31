from bs4 import BeautifulSoup
import time
import datetime
from update_chrome import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, os
sys.path.append(os.path.abspath(os.getcwd() + '../../../../'))
from config.config_del_chk import *

today = datetime.date.today() + datetime.timedelta(days=1)
today_3_ago = today - datetime.timedelta(days=3)

query = QUERY()

conn = DB()
cursor = conn.cursor()

cursor.execute(query, ("EOMISAE", "1", today_3_ago, today))
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


def login():
    url = 'https://eomisae.co.kr/'
    print("첫번째 페이지")
    driver.get(url)

    driver.find_element_by_xpath('//*[@id="navbar"]/div[1]/div[3]/div[2]/a').click()
    user_id = "als77770@naver.com"
    user_passwd = "qwe123"

    time.sleep(1)
    driver.find_element_by_id('email').send_keys(user_id)
    time.sleep(1)
    driver.find_element_by_css_selector('#login-modal > div.eq.modal-content > div.eq.modal-body > form > fieldset > div:nth-child(2) > input').send_keys(user_passwd)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="login-modal"]/div[1]/div[2]/form/fieldset/button').click()
    time.sleep(1)
    print("로그인 완료")


def crawling():
    login()
    for row in select_result:
        url = row[5]
        print(url)
        try:
            driver.get(url)
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            time.sleep(1)
            alert.accept()
            update_delete_chk(row[0])
        except:
            print("no alert")
            try:
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                contents = soup.select_one("div.btm_area.clear")
                if not contents:
                    update_delete_chk(row[0])
                else:
                    print("= undeleted")
            except Exception as e:
                print(e)


crawling()
driver.quit()
conn.close()

