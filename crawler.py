import pandas as pd 
import numpy as np 
import platform 
import matplotlib.pyplot as plt 
from selenium import webdriver 
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

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

#4. 대통령선거 클릭 
code_list_raw = driver.find_elements(By.XPATH,'//*[@id="electionCode"]/option')
print(len(code_list_raw))
for i in range(len(code_list_raw)):
    print(code_list_raw[i].text)
