from bs4 import BeautifulSoup
import requests
from gloFun import *


def get_board_list(url, soup):
    divs = soup.select('.wrapper_main > div.result_item.result_item_h')

    for div in divs:
        try:
            href = div.select_one('h2 > a')["href"]
            title = div.select_one('h2').text
            title_only_word = titleNull(title)
            host_url = div.select_one('div.result_info > div:nth-of-type(1) > div.info_item.info_item_even > span.content > span')["dt-params"]
            print(href, title)
            print("host_url : ", host_url.split("cp_id=")[1])
            host_url = host_url.split("cp_id=")[1]
            if not href or not title:
                print("url이나 제목이 없음 Error")
                continue
            get_key = getKeyword()
            key_check = checkTitle(title_only_word, get_key)
            if not key_check['m']:
                continue
            cnt_id = key_check['i']
            cnt_keyword = key_check['k']
            once = False
            print('aaaaaaaaaaaaa   \n', cnt_id, cnt_keyword)
            data = {
                'cnt_id': cnt_id,
                'cnt_osp': 'phim33',
                'cnt_title': title,
                'cnt_title_null': title_only_word,
                'host_url': host_url,
                'host_cnt': '1',
                'site_url': url,
                'cnt_cp_id': 'sbscp',
                'cnt_keyword': cnt_keyword,
                'cnt_nat': 'vetnam',
                'cnt_writer': '',
            }
            print(data)
            # db_result = insertALL(data)
            # print("DB 결과 : ", db_result)
        except Exception as e:
            print("url 및 제목 뽑을 때 Error 발생!!!!!!!!!!!!!!!!")
            print(e)


def start_crawling():
    keyword_list = list(getKeyword())
    for keyword in keyword_list:
        for i in range(1, 10):
            try:
                url = "https://v.qq.com/x/search/?searchSession=firstTabid=%E5%85%A8%E9%83%A8%7C0&q=" + keyword + \
                      "&preQid=07gYlBOlAOY9wPmWCfocsJdugU00qYSSJITQm1_AtMG63fhpDJzUTg&queryFrom=3&cur=" + str(i) + \
                      "%sisNeedQc=true&filterValue=firstTabid%3D0%26sortTabid%3D0%26tabid%3D2%26timeLongTabid%3D0%26publishTimeTabid%3D0&_=1648433574430"
                response = requests.get(url)

                if response.status_code != 200:
                    print("사이트 접속 못하고 Error 발생!!!!!!!!!!!")
                    return

                html = response.content
                soup = BeautifulSoup(html, 'html.parser')
                get_board_list("https://v.qq.com", soup)

            except Exception as e:
                print("없는 검색어")
                print(e)


start_crawling()