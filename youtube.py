import re
import time
import sys,os
from bs4 import BeautifulSoup
sys.path.append(os.path.abspath(os.getcwd() + '../../../../'))
from config.update_chrome import *
from config.config_crawler import *


def Date(date):
    date = date.split('.')
    yyyy = date[0]
    mm = date[1].replace(" ", "")
    dd = date[2].replace(" ", "")
    if int(mm) < 10:
        mm = '0' + mm
    if int(dd) < 10:
        dd = '0' + dd
    date = yyyy + "-" + mm + "-" + dd + " 00:00:00"
    return date


select_result = keyword_list()
# 0 = key_idx , 1 = Cp_id , 2 = Key_main , 3 = Key_word
for row in select_result:
    try:
        keyword = row[3]
        url = f"https://www.youtube.com/results?search_query={keyword}&sp=CAISBAgDEAE%253D"
        driver.get(url)
        time.sleep(1)
        response = driver.page_source
        soup = BeautifulSoup(response, 'html.parser')
        contents = soup.select("div#contents > ytd-video-renderer")
        for content in contents:
            href = content.select_one("a#video-title")["href"]
            href = f"https://www.youtube.com/{href}"
            driver.get(href)
            time.sleep(2)
            response = driver.page_source
            soup = BeautifulSoup(response, 'html.parser')
            user = soup.select_one("#text > a").text
            title = soup.select_one("#container > h1 > yt-formatted-string").text
            if not title:
                print("유튜브 쇼츠 넘어감!!!")
                print("==================")
                continue
            text = soup.select_one("#description > yt-formatted-string").text
            if len(text) > 999:
                Main_pick = Emotional_analysis(title)
            elif not text:
                Main_pick = Emotional_analysis(title)
            else:
                Main_pick = Emotional_analysis(text)
            write_date = soup.select_one("#info-strings > yt-formatted-string").text
            if "실시간 스트리밍" in write_date:
                print("실시간 스트리밍 넘어감!!!")
                print("==================")
                continue
            write_date = Date(write_date)

            data = {
                'Cp_id': row[1],
                'Osp_type_A': 'S',
                'Osp_type_B': 'YOUTUBE',
                'Osp_type_C': '1',
                'Main_url': href,
                'Main_title': title,
                'Main_text': text,
                'Main_writer': user,
                'Key_main': row[2],
                'Key_word': row[3],
                'Main_pick': Main_pick,
                'Main_write_date': write_date,
            }

            print("",
                  "Main_title : " + data['Main_title'],
                  "Main_url : " + data['Main_url'],
                  "Osp_type_A : " + data['Osp_type_A'],
                  "Osp_type_B : " + data['Osp_type_B'],
                  "Osp_type_C : " + data['Osp_type_C'],
                  "Key_main : " + data['Key_main'],
                  "Key_word : " + data['Key_word'],
                  "Main_writer : " + data['Main_writer'],
                  "Main_write_date : " + data['Main_write_date'],
                  sep='\n')

            # 키워드와 키메인이 제목이나 본문에 있는지 확인
            if not row[3].replace("영화", "") in text + title + user and not row[2].replace("(변형 키워드)", "") in text + title + user:
                print()
                print("키워드 키메인 체크!!\n"
                      "넘어감!!")
                print("==================")
                continue

            # 중복 체크
            ded = Deduplication(row[1], href, row[3])
            if ded == '중복':
                continue

            db_result = insertData(data)
            print("")
            print(f"DB INSERT 결과 : {db_result}")
            print("==================")

    except Exception as e:
        print(e)

driver.quit()
DB().close()