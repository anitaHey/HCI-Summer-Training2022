import calendar
import pymssql
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select

db_settings = {
    "host": "127.0.0.1",
    "user": "sa",
    "password": "zxc123",
    "database": "ncu_database",
    "charset": "utf8"
}

holiday_dir = {}

options = Options()
# options.add_argument("--headless")  # 執行時不顯示瀏覽器
options.add_argument("--disable-notifications")  # 禁止瀏覽器的彈跳通知
chrome = webdriver.Chrome(service=Service('./chromedriver'), options=options)

chrome.get("https://www.emega.com.tw/emegaTran/calendarRestList.do")

try:
    # 等元件跑完再接下來的動作，避免讀取不到內容
    WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@title='去年']")))
    chrome.find_element(By.XPATH,"//a[@title='去年']").click()
    Select(chrome.find_element(By.ID,"countrySelect")).select_by_value("local")
    WebDriverWait(chrome, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='calistset']//table")))
    holiday_list = chrome.find_elements(By.XPATH,"//div[@class='calistset']//table//tr")
    first = True;
    for holiday in holiday_list:
        if(first):
            first = False;
            continue
        td_list = holiday.find_elements(By.TAG_NAME, "td")
        date = td_list[0].text.split("(")[0]
        explain = td_list[2].find_element(By.TAG_NAME, "li").text
        date_time_obj = datetime.strptime(date, '%Y/%m/%d').strftime('%Y%m%d')
        holiday_dir[date_time_obj] = explain
except TimeoutException as e:
    print(e)    
chrome.close()
holiday_dir['20210208'] = '春節假期前夕'
holiday_dir['20210209'] = '春節假期前夕'

# print(holiday_dir)
work_count = 0
try:
    conn = pymssql.connect(**db_settings)
    command = "INSERT INTO [dbo].[calendar] (date, day_of_stock, other) VALUES (%s, %d, %s)"
    with conn.cursor() as cursor:
        for month in range(1,13):
            for date in range(1, calendar.monthrange(2021,month)[1]+1):
                date_str = f"2021{month:02d}{date:02d}"
                weekday = calendar.weekday(2021,month,date)  #取得星期，星期一為0
                
                if date_str in holiday_dir:  #若日期為特殊假日
                    cursor.execute(command, (date_str, -1, holiday_dir[date_str]))
                elif weekday == 5 or weekday == 6:  #若日期為周末
                    cursor.execute(command, (date_str, -1, ""))
                else:
                    work_count += 1
                    cursor.execute(command, (date_str, work_count, ""))
                
                conn.commit()
except Exception as e:
    print(e)

try:
    conn = pymssql.connect(**db_settings)
    command = "INSERT INTO [dbo].[year_calendar] (year, total_day) VALUES (%d, %d)"
    with conn.cursor() as cursor:
        cursor.execute(command, (2021, work_count))
        conn.commit()
except Exception as e:
    print(e)