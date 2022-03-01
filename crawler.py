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
selected_name = select_names[1] 

dropdown = Select(select_list_raw)
dropdown.select_by_visible_text(selected_name)
time.sleep(1)
#4. 대통령선거 클릭 
code_list_raw = driver.find_element_by_xpath("""//*[@id="electionCode"]""")
code_list = code_list_raw.find_elements_by_tag_name('option')
code_names = [option.text for option in code_list] 
selected_name = code_names[1]

dropdown = Select(code_list_raw)
dropdown.select_by_visible_text(selected_name)
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




