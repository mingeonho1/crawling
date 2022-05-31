## DEL_CHK bs4이용 ##
def update_delete_chk(idx):             # 삭제된 글이면 Delete_chk = 1 로 만들어주는 함수
    print("삭제된 글")
    query2 = "UPDATE main_data " \
             "SET Delete_chk = 1 " \
             "WHERE Main_idx = %s "
    cursor.execute(query2, idx)
    conn.commit()
    print("Del_chk 업뎃 성공!")

def DBCONN():                           # DB 연결
    host = ""
    port =
    database = ""               # DB 정보
    user = ''
    password = ''

    conn = pymysql.connect(
        host=host,
        user=user,
        passwd=password,
        db=database,
        port=port,
        use_unicode=True,
        charset='utf8'
    )

    query = "SELECT *" \
            "FROM main_data " \
            "WHERE Osp_type_B = %s and Osp_type_C = %s " \
            "AND Main_pick = 9 AND Delete_chk = 0 " \
            "AND Main_write_date BETWEEN %s AND %s "

    cursor = conn.cursor()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    cursor.execute(query, ("???", "1", today_3_ago, today))      # ??? 자리에는 해당하는 Osp_type_B를 넣고 / 기간은 today부터 3일전
    select_result = cursor.fetchall()
    headers = [{
        'User-Agent': user_agent
    }]

def Crawling():
    for row in select_result:
        url = row[5]
        print(url)
        try:
            response = requests.get(url, headers=headers[0], timeout=5)
            time.sleep(2)
            soup = BeautifulSoup(response.content, 'html.parser')
            contents = soup.select_one("???")                               # 삭제페이지와 일반페이지를 비교해서 삭제페이지가 가지고 있지 않은 셀렉터를 추출
            if not contents:                                                         
                update_delete_chk(row[0])                                   # 만약 그 셀렉터를 가지고 있지 않다면 update_delete_chk 함수 실행    
            else:
                print("= undeleted")                                        # 그게 아니라면 삭제되지 않은 페이지라고 판단
        except Exception as e:
            conn = pymysql.connect(                                         # 예외처리 DB가 끊기는 경우가 많기 때문에 디비연결후 계속되게 해놓음
                host=host,
                user=user,
                passwd=password,
                db=database,
                port=port,
                use_unicode=True,
                charset='utf8'
            )
            cursor = conn.cursor()
            continue


## DEL_CHK selenium이용 ##
from update_chrome import *     # chromedriver_exe 를 자동으로 업데이트 시켜주는 로직을 임포트
driver = update_chrome()   # 업데이트된 크롬드라이버

#로그인이 필요한 경우
def login():
    url = 'https://eomisae.co.kr/'  # 예시 사이트
    print("첫번째 페이지")
    driver.get(url)

    driver.find_element_by_xpath('//*[@id="navbar"]/div[1]/div[3]/div[2]/a').click()
    user_id = "a"      # 예시 아이디
    user_passwd = "qwe123"              # 예시 비번

    time.sleep(1)
    driver.find_element_by_id('email').send_keys(user_id)       # 아이디 입력
    time.sleep(1)
    driver.find_element_by_css_selector('#login-modal > div.eq.modal-content > div.eq.modal-body > form > fieldset > div:nth-child(2) > input').send_keys(user_passwd)      # 비번 입력
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="login-modal"]/div[1]/div[2]/form/fieldset/button').click()   #로그인버튼 클릭
    time.sleep(1)
    print("로그인 완료")

#알럿창이 삭제된 글이라는걸 알려줄 때
def alert_Crawling():
    for row in select_result:
        url = row[5]
        print(url)
        driver.get(url)
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            time.sleep(1)
            alert.accept()                      # 알럿창 확인후
            update_delete_chk(row[0])           # DEL_CHK 업데이트
        except:
            time.sleep(1)
            print("= no alert")




## 엑셀에서 URL가져와서 자동 스크린샷
def load_excel():
    load_wb = load_workbook('C:\\Users\\UNI-S\\Desktop\\SBS 태국 추가채증.xlsx')      # 예시 엑셀명
    load_ws = load_wb['uplayhd']                                                    # 예시 목록명
    data = load_ws.values
    columns = next(data)[0:]
    f = pd.DataFrame(data, columns=columns)

def screenshot_Crawling():
    driver = auto_update_chrome()
    driver.set_window_position(0, 0)
    driver.maximize_window()
    for i, v in enumerate(f['호스트URL']):
        try:
            # if i < 115:           # 116번째부터 찍기
            #     continue

            print(i+1)
            print(v)

            driver.get(v)
            time.sleep(5)
            driver.execute_script("window.scrollTo(0, 1000)")       #스크롤 내리기
            driver.find_element_by_css_selector("#player > div > div.container > div.player-poster.clickable").click()  # 비디오 클릭
            time.sleep(10)
            path = r"C:\Users\UNI-S\Desktop\uplayhd"    # 사진을 저장할 파일경로
            dt_datetime = datetime.datetime.now()
            format = '%Y-%m-%d %H %M %S'
            str_datetime = datetime.datetime.strftime(dt_datetime, format)
            pyautogui.screenshot(f'{path}\\{i+1} {str_datetime}.png', region=(0, 0, 1280, 720))
            print("성공")
            print("")

        except Exception as e:
            print(e)
            continue


