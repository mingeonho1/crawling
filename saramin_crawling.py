import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


# 검색어 수정가능
keyword = "파이썬"


# 서울전체 : 101000 , 경기전체 : 102000 , 서울경기전체 : 101000%2C102000
loc = "101000"


def location():
    if loc == "101000%2C102000":
        return "서울경기전체"
    elif loc == "101000":
        return "서울"
    elif loc == "102000":
        return "경기"
    else:
        return "지역오류"


def Data():
    first_url = "https://www.saramin.co.kr"

    title_list = []
    href_list = []
    company_list = []
    date_list = []

    try:
        for i in range(1,30):
            print(i,"Page")
            url = f"{first_url}/zf_user/search/recruit?search_area=main&search_done=y&search_optional_item=n&searchType=recently&searchword={keyword}&loc_mcd={loc}&" \
                  f"recruitPage={i}&recruitSort=relation&recruitPageCount=100"
            response = requests.get(url)
            print(response)
            time.sleep(2)
            soup = BeautifulSoup(response.content, 'html.parser')
            divs = soup.select("#recruit_info_list > div.content > div")
            if not divs:
                print("None Page!!!!!!!!")
                break
            else:
                for div in divs:
                    title = div.select_one("div.area_job > h2 > a")["title"]
                    href = div.select_one("div.area_job > h2 > a")["href"]
                    href = f"{first_url}{href}"
                    company = div.select_one("div.area_corp > strong > a").text
                    company = company.replace(" ", "")
                    date = div.select_one("div.area_job > div.job_date > span").text

                    title_list.append(title)
                    href_list.append(href)
                    company_list.append(company)
                    date_list.append(date)
                print("Success!!!!")
                print("")

        data = {
            "제목": title_list,
            "회사": company_list,
            "세부링크": href_list,
            "마감일": date_list,
            "채증일": datetime.today().strftime('%Y-%m-%d')
        }

        return data

    except Exception as e:
        print(e)
        print("에러!")


def save_excel():
    saramin_data = pd.DataFrame(Data())
    saramin_data.to_excel(f"./Saramin_{keyword}_{location()}_{datetime.today().strftime('%Y-%m-%d')}.xlsx", sheet_name=f'{keyword}_{location()}')
    print("")
    print(">>>>>Save Excel<<<<<")


save_excel()