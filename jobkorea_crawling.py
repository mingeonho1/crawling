import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


# 검색어 수정가능
keyword = "파이썬"


# 서울전체 : I000 , 경기전체 : B000 , 서울경기전체 : I000%2CB000
loc = "I000"


def location():
    if loc == "I000%2CB000":
        return "서울경기전체"
    elif loc == "I000":
        return "서울"
    elif loc == "B000":
        return "경기"
    else:
        return "지역오류"


def Data():
    first_url = "https://www.jobkorea.co.kr"

    title_list = []
    exp_list = []
    href_list = []
    company_list = []
    com_loc_list = []
    date_list = []

    try:
        for i in range(1,1000):
            print(i,"Page")
            url = f"{first_url}/Search/?stext={keyword}&local={loc}&tabType=recruit&Page_No={i}"
            response = requests.get(url)
            print(response)
            time.sleep(2)
            soup = BeautifulSoup(response.content, 'html.parser')
            divs = soup.select("#content > div > div > div.cnt-list-wrap > div > div.recruit-info > "
                               "div.lists > div > div.list-default > ul > li")
            if not divs:
                print("None Page!!!!!!!!")
                break
            else:
                for div in divs:
                    title = div.select_one("div > div.post-list-info > a")["title"]
                    exp = div.select_one("div > div.post-list-info > p.option > span.exp").text
                    href = div.select_one("div > div.post-list-info > a")["href"]
                    href = f"{first_url}{href}"
                    company = div.select_one("div > div.post-list-corp > a")["title"]
                    com_loc = div.select_one("div > div.post-list-info > p.option > span.loc.long").text
                    date = div.select_one("div > div.post-list-info > p.option > span.date").text

                    title_list.append(title)
                    exp_list.append(exp)
                    href_list.append(href)
                    company_list.append(company)
                    com_loc_list.append(com_loc)
                    date_list.append(date)
                print("Success!!!!")
                print("")

        data = {
            "제목": title_list,
            "경력": exp_list,
            "회사": company_list,
            "위치": com_loc_list,
            "세부링크": href_list,
            "마감일": date_list,
            "채증일": datetime.today().strftime('%Y-%m-%d')
        }

        return data

    except Exception as e:
        print(e)


def save_excel():
    saramin_data = pd.DataFrame(Data())
    saramin_data.to_excel(f"./Jobkorea_{keyword}_{location()}_{datetime.today().strftime('%Y-%m-%d')}.xlsx", sheet_name=f'{keyword}_{location()}')
    print("")
    print(">>>>>Save Excel<<<<<")


save_excel()