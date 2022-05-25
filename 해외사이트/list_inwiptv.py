from openpyxl import load_workbook
import pandas as pd
from bs4 import BeautifulSoup
import time
from update_chrome1 import *

load_wb = load_workbook(r"C:\Users\UNI-S\Desktop\list.xlsx")
load_ws = load_wb['Sheet1']
data = load_ws.values
columns = next(data)[0:]
f = pd.DataFrame(data, columns=columns)

first_url = "https://inwiptv.com/fw-login.php"

no_list = []
site_list = []
title_list = []
cnt_title_list = []
main_url_list = []
host_url_list = []
state_list = []


def login():
    try:
        driver.get(first_url)
        time.sleep(1)

        user_id = ""
        user_pw = ""
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

login()
for i, v in enumerate(zip(f['name'], f['extitle'])):
    try:
        name, extitle = v
        print(f"{i + 1} - {name}")
        driver.get(f"https://inwiptv.com/search.php?title={name}")
        time.sleep(1)
        response = driver.page_source
        soup = BeautifulSoup(response, 'html.parser')
        trs = soup.select("body > div:nth-child(2) > table > tbody > tr")
        for tr in trs:
            tds = tr.select("td")
            for td in tds:
                title = td.select_one("a > div > div").text
                if name in title:
                    print("키워드 맞음")
                    href = td.select_one("a")['href']
                    main_url = f"https://inwiptv.com/{href}"
                    print(main_url)
                    site = "inwiptv"
                    site_list.append(site)
                    cnt_title_list.append(extitle)
                    title_list.append(title)
                    main_url_list.append(main_url)
                    host_url_list.append(main_url)
                    state_list.append("TRUE")
                    time.sleep(1)
                    print("데이터 삽입 성공")
                else:
                    print("키워드랑 제목이랑 다름!!")
                    continue

    except Exception as e:
        print(e)
        print("없는 키워드")
        continue

last_data = pd.DataFrame(
    zip(site_list, cnt_title_list, title_list, main_url_list, host_url_list, state_list),
    columns=['사이트', '콘텐츠 제목', '검출 제목', '메인URL', '호스트URL (각 회차URL)', 'STATE'])
last_data.to_excel('../uplay/inwiptv2.xlsx')
print("엑셀 만들기 성공")