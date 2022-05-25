from selenium import webdriver
from openpyxl import load_workbook
import pandas as pd
import datetime
import time
import pyautogui

load_wb = load_workbook('')
load_ws = load_wb['Sheet1']
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
time.sleep(5)
last_tab = driver.window_handles[-1]
driver.switch_to.window(window_name=last_tab)



for i, v in enumerate(f['호스트URL']):
    try:
        # if i < 257:
        #     continue

        print(i+1)
        print(v)



        driver.get(v)
        time.sleep(3)
        pyautogui.moveTo(743, 489, duration=1)
        time.sleep(2)
        pyautogui.click()
        time.sleep(20)
        dt_datetime = datetime.datetime.now()
        format = '%Y-%m-%d %H %M %S'
        str_datetime = datetime.datetime.strftime(dt_datetime, format)
        path = r"C:\Users\UNI-S\Desktop\do"
        pyautogui.screenshot(f'{path}\\{i + 1} {str_datetime}.png', region=(0, 0, 1280, 720))
        print("성공")
        print("")
    except:
        print(f"에러=========== {i+1}")
        continue