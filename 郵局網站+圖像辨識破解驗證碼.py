# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 10:22:24 2024

@author: ASUS
"""
#這程式碼可以查詢郵遞區號
# 引入需要的庫
import requests as rq  # 用於發送 HTTP 請求
from bs4 import BeautifulSoup as bs  # 用於解析 HTML 頁面
import pytesseract  # 用於處理驗證碼辨識
from PIL import Image  # 用於處理圖片（Tesseract需要圖片作為輸入）
from selenium import webdriver  # 用於瀏覽器自動化
from selenium.webdriver.common.by import By  # 用於定位元素
from selenium.webdriver.support.ui import Select  # 用於選擇下拉框中的項目
from selenium.common.exceptions import UnexpectedAlertPresentException  # 用於處理瀏覽器彈窗異常
from selenium.common.exceptions import NoSuchElementException  # 用於處理找不到元素異常
from selenium.webdriver.support.ui import WebDriverWait  # 用於顯式等待
from selenium.webdriver.support import expected_conditions as EC  # 用於設置等待條件
import time  # 用於設置延遲

# 讓用戶輸入城市、區域和街道信息
city = input('input city')  # 輸入城市名
# 替換“台”為“臺”，處理繁體字問題
city = city.replace('台', '臺')  # 這是為了處理台灣地名中可能存在的“台”字與“臺”字的差異
area = input('input area')  # 輸入區域名
street = input('input street')  # 輸入街道名稱

# 驗證碼辨識過程可能會出錯，這段程式碼會無限重複直到成功辨識
while True:
    chrome_options = webdriver.ChromeOptions()  # 設定 Chrome 瀏覽器選項
    chrome_options.add_argument("--headless")  # 設定無頭模式（不顯示瀏覽器介面）
    driver = webdriver.Chrome(options=chrome_options)  # 初始化瀏覽器

    # 訪問郵政網站的查詢頁面
    driver.get('https://www.post.gov.tw/post/internet/SearchZone/index.jsp?ID=130107')

    # 讀取頁面源碼
    r = driver.page_source

    # 選擇城市下拉框
    select = Select(driver.find_element(By.ID, 'city_zip6'))
    select.select_by_visible_text(city)  # 選擇指定的城市
    time.sleep(1)  # 暫停 1 秒鐘，等待頁面更新

    # 選擇區域下拉框
    select = Select(driver.find_element(By.ID, 'cityarea_zip6'))
    select.select_by_visible_text(area)  # 選擇指定的區域
    time.sleep(1)  # 暫停 1 秒鐘

    # 選擇街道下拉框
    select = Select(driver.find_element(By.ID, 'street_zip6'))
    select.select_by_visible_text(street)  # 選擇指定的街道
    time.sleep(1)  # 暫停 1 秒鐘

    # 找到驗證碼輸入框，並且模擬點擊填寫驗證碼
    chebar = driver.find_element(By.ID, 'checkImange_zip6')
    chebar.send_keys()  # 用於觸發驗證碼加載（這裡似乎缺少對驗證碼的處理）

    time.sleep(1)  # 暫停 1 秒鐘，等待驗證碼圖片加載

    # 使用 requests 模擬請求來獲取驗證碼圖片
    sess = rq.Session()  # 創建一個請求會話
    soup = bs(r, 'html.parser')  # 使用 BeautifulSoup 解析頁面源碼
    img = soup.find('img', attrs={'id': 'imgCaptcha3_zip6'})  # 找到驗證碼圖片的 URL
    img = img.get('src')  # 提取圖片的 URL
    r2 = sess.get('https://www.post.gov.tw/post/internet' + img[2:])  # 請求該圖片
    with open('Postimg.jpg', 'wb') as file:  # 下載圖片並保存
        file.write(r2.content)

    # 使用 Tesseract OCR 來識別驗證碼
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 設定 Tesseract 的安裝路徑
    img = Image.open('Postimg.jpg')  # 打開下載的圖片
    img = img.convert('L')  # 轉為灰階圖像，以提高辨識效果
    ans = str.strip(pytesseract.image_to_string(img, config='--psm 6'))  # 辨識圖片中的文本
    print(f'圖像辨識結果為{ans}')  # 顯示識別結果

    # 將辨識結果填入驗證碼輸入框並提交表單
    chebar.send_keys(ans)
    btn = driver.find_element(By.CSS_SELECTOR, '[class="Submit_1"]')  # 找到提交按鈕
    btn.click()  # 點擊提交按鈕

    # 等待郵遞區號顯示，直到元素出現
    try:
        locater = (By.CSS_SELECTOR, '[data-th="郵遞區號"]')  # 定位郵遞區號元素
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(locater))  # 等待最多 10 秒直到元素加載完成
        r = driver.page_source  # 重新獲取頁面源碼
        break  # 成功獲取頁面後退出循環
    except UnexpectedAlertPresentException:
        # 如果出現了警告（例如錯誤的驗證碼），捕捉異常並打印“查詢中”
        print('查詢中')
        driver.quit()  # 關閉瀏覽器
        continue  # 重新開始循環

# 使用 BeautifulSoup 解析結果頁面
soup = bs(r, 'html.parser')

# 找到所有郵遞區號和投遞範圍
zipcode = soup.find_all(attrs={'data-th': "郵遞區號"})
codeRange = soup.find_all(attrs={'data-th': "投遞範圍"})

# 輸出郵遞區號和投遞範圍的對應關係
for z, c in zip(zipcode, codeRange):
    print(z.text, c.text)  # 打印郵遞區號和投遞範圍

driver.quit()  # 最後關閉瀏覽器