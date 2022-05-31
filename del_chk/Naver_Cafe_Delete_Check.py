import time
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from update_chrome import *
import sys, os
sys.path.append(os.path.abspath(os.getcwd() + '../../../../'))
from config.config_del_chk import *

today = datetime.date.today() + datetime.timedelta(days=1)
today_3_ago = today - datetime.timedelta(days=3)

query = QUERY()

conn = DB()
cursor = conn.cursor()

cursor.execute(query, ("NAVER", "C", today_3_ago, today))
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
            driver.get(url)
            WebDriverWait(driver, 1).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            time.sleep(1)
            alert.accept()
            update_delete_chk(row[0])
        except:
            print("= no alert")


crawling()
driver.quit()
conn.close()