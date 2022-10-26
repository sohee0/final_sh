import pandas as pd
import numpy as np
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')

# df = pd.read_csv('./data_tour/부산관광지440개.csv',encoding='utf-8') 
# df['naver_map_review'] = '' # 미리 리뷰 건수 담을 column을 만들어줌 
# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# wd=webdriver.Chrome('./chromedriver.exe',options=options)

# for i, keyword in enumerate(df['명칭'].tolist()): 
    
#     try:
#         naver_map=wd.get()
#     print("관광지 :", i, f"/ {df.shape[0]} 행", keyword) 
    
 
    


def getNavermap(result):
    
    df = pd.read_csv('./data_tour/관광지명칭.csv',encoding='utf-8') 
    df['naver_map_review'] = '' # 미리 리뷰 건수 담을 column을 만들어줌 

    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    wd = webdriver.Chrome('./chromedriver.exe', options=options)

    for i, keyword in enumerate(df['명칭'].tolist()): 
    
        print("이번에 찾을 키워드 :", i, f"/ {df.shape[0]} 행", keyword) 
    
        try: 
            wd.get(f'https://map.naver.com/v5/search/{keyword}=14377346.8495072,4186044.6333144,15,0,0,0,dh') # 검색 url 접속 = 검색하기 
            time.sleep(4) # 중요

            
            # wd.switch_to.frame('searchIframe')
            # wd.find_element(By.XPATH,'//*[@id="_pcmap_list_scroll_container"]/ul/li[1]').click()
            # time.sleep(3)
                
        
            wd.switch_to.frame('entryIframe')
            wd.find_element(By.XPATH,'//*[@id="app-root"]/div/div/div/div[2]/div[1]').click()
            time.sleep(3)
            html = wd.page_source
            soup = BeautifulSoup(html, 'html.parser')
            # span 태그에 class 속성 사용 추출하기
            review = soup.find_all('span', attrs={'class':'PXMot'})
            for item in review:
                print(item.get_text())

            result.append([review])
        except:
            wd.switch_to.frame('searchIframe')
            # wd.find_element(By.XPATH,'//*[@id="_pcmap_list_scroll_container"]/ul/li[1]').click()
            wd.find_element(By.XPATH,'//*[@id="_pcmap_list_scroll_container"]/ul/li[1]/div[2]/a[1]/div/div/span[1]').click()
            time.sleep(4)
            html = wd.page_source
            soup = BeautifulSoup(html, 'html.parser')  
            # span 태그에 class 속성 사용 추출하기
            review = soup.find_all('span', attrs={'class':'PXMot'})
            
            for item in review:
                print(item.get_text())

            result.append([review])
        # except IndexEror: 
        #     df['naver_map_review'][i]= ''
        #     print('none') 


    # query = df['명칭'].tolist()
    # wd.get(f'https://map.naver.com/v5/search/{query}=14377346.8495072,4186044.6333144,15,0,0,0,dh')
    # time.sleep(3)
    # wd.switch_to.frame('entryIframe')
    # wd.find_element(By.XPATH,'//*[@id="app-root"]/div/div/div/div[2]/div[1]').click()
    # time.sleep(3)
    # html = wd.page_source
    # soup = BeautifulSoup(html, 'html.parser')
    # # span 태그에 class 속성 사용 추출하기
    # review = soup.find_all('span', attrs={'class':'PXMot'})
    # for item in review:
    #     print(item.get_text())

    # result.append([review])


def main():
    result = []
    print('네이버맵크롤링 : ')
    getNavermap(result)
    print('크롤링끝')

if __name__=='__main__':
    main()