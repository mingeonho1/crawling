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

first_url = "https://web.u-playtv.com/webapp/index.php"

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


login()
for i, v in enumerate(zip(f['name'], f['extitle'])):
    try:
        name, extitle = v
        driver.get(f"{first_url}?a=search&term={name}")
        time.sleep(3)
        response = driver.page_source
        soup = BeautifulSoup(response, 'html.parser')
        lis = soup.select("#solo-seriesthumbs-ul > li")
        if not lis:
            delete = "o"
        else:
            delete = "x"
        print(f"{i + 1} 없는 키워드 = {delete}")
        LOG = soup.select_one("#solo_login_submitbtn")
        if LOG:
            login()
            print("재로그인 완료")
        for li in lis:
            a = li.select_one('a')['href']
            title = li.select_one("div.movie_name_under").text
            if name in title:
                driver.execute_script(f"{a}")
                time.sleep(3)
                main_url = driver.current_url
                response = driver.page_source
                soup1 = BeautifulSoup(response, 'html.parser')
                divs = soup1.select("#solo-seriedetails-seasons-container > div")
                for div in divs:
                    aa = div.select_one('a')['href']
                    driver.execute_script(f"{aa}")
                    time.sleep(2)
                    response = driver.page_source
                    soup2 = BeautifulSoup(response, 'html.parser')
                    liss = soup2.select("#solo-serie-episodes-ul > li")
                    link = driver.page_source
                    for lis in liss:
                        if LOG:
                            login()
                            print("(재로그인)")
                        aaa = lis.select_one('a')['href']
                        driver.execute_script(f"{aaa}")
                        time.sleep(2)
                        host_url = driver.current_url
                        print(host_url)
                        driver.back()
                        time.sleep(1)
                        site = "uplayhd"

                        site_list.append(site)
                        cnt_title_list.append(extitle)
                        title_list.append(title)
                        main_url_list.append(main_url)
                        host_url_list.append(host_url)
                        state_list.append(1)
                        time.sleep(1)
                        print("데이터 삽입 성공")



                    driver.back()
                    print("뒤로이동")
                driver.back()
                print("뒤로이동")
                time.sleep(1)

            else:
                print("키워드랑 제목이랑 다름!!")
                continue


    except Exception as e:
        print(e)
        continue

last_data = pd.DataFrame(
    zip(site_list, cnt_title_list, title_list, main_url_list, host_url_list, state_list),
    columns=['사이트', '콘텐츠 제목', '검출 제목', '메인URL', '호스트URL (각 회차URL)', 'STATE'])
last_data.to_excel('./uplay/uplay2.xlsx')
print("엑셀 만들기 성공")