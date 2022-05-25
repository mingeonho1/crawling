
from bs4 import BeautifulSoup
from selenium import webdriver
from gloFun import *

keyword_list = list(getKeyword())
driver = webdriver.Chrome('C:\\user\\chromedriver.exe')

def crawling():
    first_url = "https://subnhanh.net"
    url = f"{first_url}/search?query={keyword}"
    driver.get(url)
    driver.execute_script("window.scrollTo(0, 500)")
    time.sleep(3)
    response = driver.page_source
    soup = BeautifulSoup(response, 'html.parser')
    divs = soup.select('#all-items')
    try:
        for div in divs:
            for i in range(2, 20):
                href = div.select_one(f"#all-items > div:nth-child({i}) > div > a.item-block-title.w-inline-block")["href"]
                href = f"{first_url}{href}"
                title = div.select_one(f"#all-items > div:nth-child({i}) > div > a.item-block-title.w-inline-block > div").text
                title_only_word = titleNull(title)
                if title_only_word == Nullkeyword:
                    print(title, href)
                    driver.get(href)
                    response = driver.page_source
                    soup = BeautifulSoup(response, 'html.parser')
                    a = soup.select_one("body > div.dynamic-page-header > div > div > div > div.header-info-block > div > a.button_xemphim.w-button")["href"]
                    a_href = f"{first_url}{a}"
                    driver.get(a_href)
                    driver.execute_script("window.scrollTo(0, 20000)")
                    time.sleep(3)
                    response = driver.page_source
                    soup = BeautifulSoup(response, 'html.parser')
                    divs2 = soup.select('div.collection-list.w-dyn-items > div')
                    for div2 in divs2:
                        try:
                            video_href = div2.select_one("a")["href"]
                            video_title = div2.select_one("a")["title"]
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
                                'cnt_osp': 'subnhanh',
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