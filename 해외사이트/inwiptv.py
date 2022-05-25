from openpyxl import load_workbook
import pandas as pd
import datetime
import time
import pyautogui
from update_chrome import *

auto_update_chrome()

load_wb = load_workbook('')
load_ws = load_wb['inwiptv']
data = load_ws.values
columns = next(data)[0:]
f = pd.DataFrame(data, columns=columns)


option = webdriver.ChromeOptions()
option.add_extension(
    'adblock.zip'
)
option.add_argument('--start-maximized');
driver = webdriver.Chrome(executable_path='C:\\user\\chromedriver.exe', chrome_options=option)
driver.set_window_position(0, 0)
driver.maximize_window()
time.sleep(10)
last_tab = driver.window_handles[-1]
driver.switch_to.window(window_name=last_tab)

first_url = "https://inwiptv.com/fw-login.php"


def login():
    try:
        driver.get(first_url)
        time.sleep(1)

        user_id = "9tiger"
        user_pw = "666666"
        time.sleep(1)
        driver.find_element_by_id('username').send_keys(user_id)
        time.sleep(2)
        driver.find_element_by_id('password').send_keys(user_pw)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="login"]').click()
        time.sleep(10)
        print("로그인 완료")

    except Exception as e:
        print(e)
        print("로그인 오류!!!!!!!!!!!!!!!!!!!!!!")


def crawling():
    for i, v in enumerate(f['메인URL']):
        try:
            if i < 33:
                continue
            print(i+1)
            print(v)

            driver.get(v)
            time.sleep(5)
            video = driver.find_element_by_css_selector("#myElement > div.jw-media.jw-reset > video")
            if video:
                video.click()
            driver.execute_script("window.scrollTo(0, 200)")
            time.sleep(5)
            path = r"C:\Users\UNI-S\Desktop\inwiptv"
            dt_datetime = datetime.datetime.now()
            format = '%Y-%m-%d %H %M %S'
            str_datetime = datetime.datetime.strftime(dt_datetime, format)
            pyautogui.screenshot(f'{path}\\{i+1} {str_datetime}.png', region=(0, 0, 1280, 720))
            print("성공")
            print("")

        except Exception as e:
            print(e)
            continue
login()
crawling()
driver.close()