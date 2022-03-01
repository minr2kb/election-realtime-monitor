import pandas as pd 
import numpy as np 
import platform 
import matplotlib.pyplot as plt 
from selenium import webdriver 
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup

# headless 옵션으로 브라우져의 백그라운드 실행
options = webdriver.ChromeOptions()
options.add_argument("headless")

driver = webdriver.Chrome('./chromedriver', options=options) 

 #1.개표현황 주소로 이동 
print("Opening the browser with headless mode...")
driver.get('http://info.nec.go.kr/main/showDocument.xhtml?electionId=0000000000&topMenuId=VC&secondMenuId=VCCP09')

#2. 대통령 선거 클릭
driver.find_element_by_xpath("""//*[@id="electionType1"]""").click()


#3. 제일 최신 대선 정보 출력 (최신이 가장 앞에 온다는 가정 하에)
select_list_raw = driver.find_element_by_xpath("""//*[@id="electionName"]""") 
select_list=select_list_raw.find_elements_by_tag_name("option") 
select_names = [option.text for option in select_list] 
selected_name = select_names[1:] 

dropdown = Select(select_list_raw)
dropdown.select_by_visible_text(selected_name[0])
time.sleep(0.5)

#4. 대통령선거 클릭 
code_list_raw = driver.find_element_by_xpath("""//*[@id="electionCode"]""")
code_list = code_list_raw.find_elements_by_tag_name('option')
code_names = [option.text for option in code_list] 
selected_name = code_names[1:]

dropdown = Select(code_list_raw)
dropdown.select_by_visible_text(selected_name[0])
time.sleep(0.5)

#5. 시도군 리스트 가져오기

city_list_raw = driver.find_element_by_xpath("""//*[@id="cityCode"]""") 
city_list=city_list_raw.find_elements_by_tag_name("option") 
city_names = [option.text for option in city_list] 
city_names = city_names[2:] 

print(city_names)

#6. 각 시도별로 데이터 긁어오기 

def get_vote(n):
    name = n
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    tmp = soup.find_all('td','alignR')
    gu = soup.find_all('td','alignL')
    gu_names = [tmp_val.get_text() for tmp_val in gu[1:]]

    tmp_list = []

    # 한 줄에 총 18개의 column이 있음. 그 다음줄의 18개는 퍼센트이므로 건너뜀.
    for i in range(0,len(tmp),36):
        tmp_values = [(tmp_val.get_text().replace(',','')) for tmp_val in tmp[i:i+18]]
        tmp_list.append(tmp_values)

    #처음의 시도 총합과 필요없는 데이터 trim
    tmp_list=tmp_list[1:-1]

    gu_dict={}
    for i in range(len(tmp_list)):
        # 공백을 건너 뛰며 각 구에대한 데이터들을 dictionary로 변환
        name=gu_names[2*i+1]
        items=tmp_list[i]
        gu_dict[name] = items
    
    #Pandas 데이터프레임으로 변환
    result = pd.DataFrame.from_dict(gu_dict).T

    #19대 기준으로 18개의 column 지정
    # result.columns=['선거인수','투표수','이재명','윤석열','심상정','안철수','오준호','허경영','이백윤','옥은호','김동연','김경재','조원진','김재연','이경희','김민찬', '합계', '무효', '기권']
    result.columns=['선거인수','투표수','문재인','홍준표','안철수','유승민','심상정','조원진','오영국','장성민','이재오','김선동','이경희','윤홍식','김민찬', '합계', '무효', '기권']

    #각 구들의 광역시 / 도 에대한 정보 column을 추가
    result['광역시도'] = n
    result.reset_index(inplace=True)
    result.rename(index=str, columns={"index":"시군"}, inplace =True)

    return result

# 각 도시에 대한 루프
for city in city_names:
    print("Crawling " + city + "...")
    element = driver.find_element_by_id('cityCode')
    element.send_keys(city) # 도시를 선택
    driver.find_element_by_xpath("""//*[@id="searchBtn"]""").click() # 검색버튼
    # time.sleep(0.5) # 로드해올 시간
    tmp= get_vote(city)

    if city == city_names[0]:
        result = tmp
    else:
        result = result.append(tmp)

print(result)
driver.quit()
# result.to_csv('./data/election_result.csv', encoding='utf-8', sep=',')
