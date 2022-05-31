from selenium import webdriver
import chromedriver_autoinstaller

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]  #크롬드라이버 버전 확인
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_experimental_option("excludeSwitches",  ["enable-automation"])
try:
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', chrome_options=options)
    print("크롬드라이버 최신 버전!!")
except:
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', chrome_options=options)
    print("크롬드라이버 업데이트 완료!!")
driver.implicitly_wait(10)

