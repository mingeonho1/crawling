from selenium import webdriver
from openpyxl import load_workbook
import pandas as pd
import datetime
import time
import pyautogui

load_wb = load_workbook('C:\\Users\\UNI-S\\Desktop\\SBS 태국 채증_220413.xlsx')
load_ws = load_wb['we-play']
data = load_ws.values
columns = next(data)[0:]
f = pd.DataFrame(data, columns=columns)

driver = webdriver.Chrome('C:\\user\\chromedriver.exe')
driver.set_window_position(1280, 0)
driver.maximize_window()

for i, v in enumerate(f['호스트URL']):
    print(i)
    print(v)

    dt_datetime = datetime.datetime.now()
    format = '%Y-%m-%d %H %M %S'
    str_datetime = datetime.datetime.strftime(dt_datetime, format)
    driver.get(v)
    time.sleep(2)
    sample = driver.find_element_by_css_selector('#widget_ads2 > div > a:nth-child(1)')
    driver.execute_script("arguments[0].click();", sample)
    driver.find_element_by_css_selector("#player").click()
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="player"]/div[2]/div[13]/div[5]').click()
    time.sleep(5)
    path = r"C:\Users\UNI-S\Desktop\we-play"
    print("Current Mouse Position:",pyautogui.position())
    pyautogui.screenshot(f'{path}\\{i+1} {str_datetime}.png', region=(1280, 0, 2560, 720))
    print("성공")
    print("")
