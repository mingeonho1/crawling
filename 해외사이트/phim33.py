import time

from bs4 import BeautifulSoup
from selenium import webdriver
from gloFun import *

url_list = ["https://phim33.co/phim-anh-la-hiep-si-bong-dem-cua-em-16537.html","https://phim33.co/phim-co-giao-va-keo-bong-gon-16472.html","https://phim33.co/phim-tai-xe-taxi-16073.html","https://phim33.co/phim-anh-co-thich-brahms-15537.html","https://phim33.co/phim-xu-so-alice-15527.html"]



driver = webdriver.Chrome('C:\\user\\chromedriver.exe')

for li in url_list:
    driver.get(li)
    driver.execute_script("window.scrollTo(0, 300)")
    time.sleep(3)
    response = driver.page_source
    soup = BeautifulSoup(response, 'html.parser')
    # title = soup.select_one("h1.name").text
    # title2 = soup.select_one("h2.real-name").text
    lists = soup.select("ul.list-episode > li")
    for so in soup:
        try:
            for lst in lists:
                href = lst.select_one("a")["href"]
                title = so.select_one("h1.name").text
                title_only_word = titleNull(title)
                # host_url = lst.select_one("a")["href"]
                print(href, title)
                print(title_only_word)
                time.sleep(1)
                if not href or not title:
                    print("url이나 제목이 없음 Error")
                    continue
                get_key = getKeyword()
                key_check = checkTitle(title_only_word, get_key)
                print(key_check)
                if not key_check['m']:
                    continue
                cnt_id = key_check['i']
                cnt_keyword = key_check['k']
                once = False
                data = {

                    'cnt_id': cnt_id,
                    'cnt_osp': 'phim33',
                    'cnt_title': title,
                    'cnt_title_null': title_only_word,
                    'host_url': href,
                    'host_cnt': '1',
                    'site_url': li,
                    'cnt_cp_id': 'sbscp',
                    'cnt_keyword': cnt_keyword,
                    'cnt_nat': 'vetnam',
                    'cnt_writer': '',
                }
                print(data)
                db_result = insertALL(data)
                print("DB 결과 : ", db_result)
        except Exception as e:
            print("url 및 제목 뽑을 때 Error 발생!!!!!!!!!!!!!!!!")
            print(e)



driver.close()

