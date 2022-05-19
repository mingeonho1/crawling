import time
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import pandas as pd


def Data():
    url = "https://www.bithumb.com/trade/order/BTC_KRW"

    title_list = []
    price_list = []
    asset_list = []

    driver = webdriver.Chrome('C:\\user\\chromedriver.exe')
    driver.get(url)
    time.sleep(3)
    response = driver.page_source
    soup = BeautifulSoup(response, 'html.parser')
    lis = soup.select("#coinListTab > div > div > div.scrollbot-inner-parent > ol > li")
    len(lis)

    for li in lis:
        try:

            title = li.select_one("div.tx_l.tx_link > span.coinSymbol.sort_coin")["data-sorting"]
            price = li.select_one("div.tx_r.tx_real > div.sort_price_box > span.sort_price").text
            asset = li.select_one("div.tx_r.tx_amount > span.sort_amount").text

            title_list.append(title)
            price_list.append(price)
            asset_list.append(asset)
        except Exception as e:
            print("End")

    data = {
        "제목": title_list,
        "현재가": price_list,
        "거래대금": asset_list,
    }

    return data


def save_excel():
    bithumb_data = pd.DataFrame(Data())
    bithumb_data.to_excel(f"./Bithumb_{datetime.today().strftime('%Y-%m-%d')}.xlsx", sheet_name=f"{datetime.today().strftime('%Y-%m-%d')}")
    print("")
    print(">>>>>Save Excel<<<<<")


save_excel()