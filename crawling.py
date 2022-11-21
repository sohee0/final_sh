import random
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import requests
from webdriver_manager.chrome import ChromeDriverManager
# 오류확인
import traceback 
from selenium.webdriver.common.by import By
# # 최신 크롬 드라이버 사용하도록 세팅: 현재 OS에 설치된 크롬 브라우저 버전에 맞게 cache에 드라이버 설치
# from selenium.webdriver.chrome.service import Service
# service = Service(ChromeDriverManager().install())

# 셀레니움오류 해결 
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

wd = webdriver.Chrome('./chromedriver.exe')
word= word = '부산여행 카페'.replace(' ', '+')
url = "https://www.youtube.com/results?search_query=" + word
wd.get(url)
time.sleep(3)

def scroll():
    try:        
        # 페이지 내 스크롤 높이 받아오기
        last_page_height = wd.execute_script("return document.documentElement.scrollHeight")
        while True:
            # 임의의 페이지 로딩 시간 설정
        
            pause_time=  random.uniform(2,4)

            # 페이지 최하단까지 스크롤
            wd.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            # 페이지 로딩 대기
            time.sleep(pause_time)
            # 무한 스크롤 동작을 위해 살짝 위로 스크롤(i.e., 페이지를 위로 올렸다가 내리는 제스쳐)
            wd.execute_script("window.scrollTo(0, document.documentElement.scrollHeight-50)")
            time.sleep(pause_time)
            # 페이지 내 스크롤 높이 새롭게 받아오기
            new_page_height = wd.execute_script("return document.documentElement.scrollHeight")
            # 스크롤을 완료한 경우(더이상 페이지 높이 변화가 없는 경우)
            if new_page_height == last_page_height:
                print("스크롤 완료")
                break
                
            # 스크롤 완료하지 않은 경우, 최하단까지 스크롤
            else:
                last_page_height = new_page_height
            
    except Exception as e:
        print("에러 발생: ", e)

    # 페이지 소스 추출
    html_source = wd.page_source
    soup_source = BeautifulSoup(html_source, 'html.parser')

    content_total = soup_source.find_all(class_ = 'yt-simple-endpoint style-scope ytd-video-renderer')
    content_total_title = list(map(lambda data: data.get_text().replace("\n", ""), content_total))

    youtube_dict = {'title'       : content_total_title}

    df = pd.DataFrame(youtube_dict)
    
    df.to_csv('부산여행카페_유튜브.csv', encoding='', index=False)


scroll()

