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

driver = webdriver.Chrome('./chromedriver') 

 #1.개표현황 주소로 이동 
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
time.sleep(1)

#4. 대통령선거 클릭 
code_list_raw = driver.find_element_by_xpath("""//*[@id="electionCode"]""")
code_list = code_list_raw.find_elements_by_tag_name('option')
code_names = [option.text for option in code_list] 
selected_name = code_names[1:]

dropdown = Select(code_list_raw)
dropdown.select_by_visible_text(selected_name[0])
time.sleep(1)

#5. 시도군 선택

city_list_raw = driver.find_element_by_xpath("""//*[@id="cityCode"]""") 
city_list=city_list_raw.find_elements_by_tag_name("option") 
city_names = [option.text for option in city_list] 
city_names = city_names[2:] 

print(city_names)

dropdown = Select(city_list_raw)
dropdown.select_by_visible_text(city_names[0])

#검색 버튼 클릭 
driver.find_element_by_xpath("""//*[@id="searchBtn"]""").click()

#정보 긁어오기 

def get_vote(n):
    name = n
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    tmp = soup.find_all('td','alignR')
    gu = soup.find_all('td','alignL')
    gu_names = [tmp_val.get_text() for tmp_val in gu[1:]]

    # print(gu_names)

    tmp_list = []
    for i in range(19,len(tmp),18):
        tmp_values = [(tmp_val.get_text().replace(',','')) for tmp_val in tmp]
        # print(tmp_values)
        tmp_list.append(tmp_values)
        
    tmp_list=tmp_list[0]
  
        
    gu_dict={}
    for i in range(len(gu_names)):
        name=gu_names[i]
        items=tmp_list[i]
        gu_dict[name] = items
    
    print(gu_dict)
    result = pd.DataFrame.from_dict(gu_dict).T
    print(result.head())
    result.columns=['총 투표수','이재명','윤석열','심상정','안철수','오준호','허경영','이백윤','옥은호','김동연','김경재','조원진','김재연','이경희','김민찬']

    result['광역시도'] = n
    result.reset_index(inplace=True)
    result.rename(index=str, columns={"index":"시군"}, inplace =True)

    return result

for city in city_names:
    print(city)
    time.sleep(1)
    element = driver.find_element_by_id('cityCode')
    element.send_keys(city)
    driver.find_element_by_xpath("""//*[@id="searchBtn"]""").click()
    tmp= get_vote(city)

    if city == city_names[0]:
        result = tmp
    else:
        result=result.append(tmp)

print(result)
result.to_csv('./data/election_result.csv', encoding='utf-8', sep=',')
