from selenium import webdriver
from openpyxl import load_workbook
import pandas as pd
import datetime
import time
import pyautogui

load_wb = load_workbook('')
load_ws = load_wb['uplayhd']
data = load_ws.values
columns = next(data)[0:]
f = pd.DataFrame(data, columns=columns)

driver = webdriver.Chrome('C:\\user\\chromedriver.exe')
driver.set_window_position(0, 0)
driver.maximize_window()

first_url = "https://web.u-playtv.com/webapp/index.php?"
def login():
    try:

        driver.get(first_url)
        time.sleep(1)

        user_id = ""
        user_pw = ""
        time.sleep(1)
        driver.find_element_by_id('solo_login_email').send_keys(user_id)
        time.sleep(1)
        driver.find_element_by_id('solo_login_password').send_keys(user_pw)
        time.sleep(1)
        sample = driver.find_element_by_css_selector('#solo_login_submitbtn')
        sample.click()
        time.sleep(3)
        print("로그인 완료")

    except Exception as e:
        print(e)
        print("로그인 오류!!!!!!!!!!!!!!!!!!!!!!")

def crawling():
    for i, v in enumerate(f['호스트URL']):
        try:
            if i < 115:
                continue

            print(i+1)
            print(v)

            driver.get(v)
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, 1000)")
            driver.find_element_by_css_selector("#player > div > div.container > div.player-poster.clickable").click()
            time.sleep(10)
            path = r"C:\Users\UNI-S\Desktop\uplayhd"
            dt_datetime = datetime.datetime.now()
            format = '%Y-%m-%d %H %M %S'
            str_datetime = datetime.datetime.strftime(dt_datetime, format)
            pyautogui.screenshot(f'{path}\\{i+1} {str_datetime}.png', region=(0, 0, 1280, 720))
            print("성공")
            print("")

        except Exception as e:
            print(e)
            log_id = driver.find_element_by_css_selector("#solo_login_email")
            if log_id:
                login()
            continue


login()
crawling()
driver.close()