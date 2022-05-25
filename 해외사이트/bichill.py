from bs4 import BeautifulSoup
from selenium import webdriver
from gloFun import *
import re

keyword_list = list(getKeyword())
driver = webdriver.Chrome('C:\\user\\chromedriver.exe')

def crawling():
    first_url = "https://bichill.net"
    url = f"{first_url}/search?q={keyword}"
    driver.get(url)
    driver.execute_script("window.scrollTo(0, 500)")
    time.sleep(3)
    response = driver.page_source
    soup = BeautifulSoup(response, 'html.parser')
    divs = soup.select('#all-items')
    try:
        for div in divs:
            href = div.select_one("div > a")["href"]
            href = f"{first_url}{href}"
            title = div.select_one("div > a")["title"]
            t1 = titleNull(div.select_one("h6.title.elipsis").text)
            t2 = titleNull(div.select_one("p.elipsis").text)
            if t1 == Nullkeyword or t2 == Nullkeyword:
                print(title,href)
                driver.get(href)
                driver.execute_script("window.scrollTo(0, 500)")
                time.sleep(3)
                response = driver.page_source
                soup = BeautifulSoup(response, 'html.parser')
                divs2 = soup.select("#playlists > div.block.mt-3.mb-3 > div > div.epi-list-all > div > div.epi-block-right > div")
                for div2 in divs2:
                        video_num = div2.select_one("a").text
                        maxnum = re.sub(r'[^0-9]', '', video_num)
                        for i in range(1, int(maxnum)+1):
                            try:
                                video_href = div2.select_one(f"a:nth-child({i})")["href"]
                                video_title = div2.select_one(f"a:nth-child({i})")["title"]
                                video_href = f"{first_url}{video_href}"
                                title_only_word = titleNull(video_title)
                                get_key = getKeyword()
                                key_check = checkTitle(title_only_word, get_key)
                                if not key_check['m']:
                                    continue
                                cnt_id = key_check['i']
                                cnt_keyword = key_check['k']

                                data = {
                                    'cnt_id': cnt_id,
                                    'cnt_osp': 'bichill',
                                    'cnt_title': video_title,
                                    'cnt_title_null': title_only_word,
                                    'host_url': video_href,
                                    'host_cnt': '1',
                                    'site_url': href,
                                    'cnt_cp_id': 'sbscp',
                                    'cnt_keyword': cnt_keyword,
                                    'cnt_nat': 'vetnam',
                                    'cnt_writer': '',
                                }
                                print(data)
                                db_result = insertALL(data)
                                print("DB 결과 : ", db_result)

                            except:
                                curs
                                print("DB다시연결!!")
                                continue


    except Exception as e:
        print("없는 검색어")
        print(e)



for keyword in keyword_list:
    try:
        Nullkeyword = titleNull(keyword)
        crawling()

    except Exception as e:
        print(e)

driver.close()
