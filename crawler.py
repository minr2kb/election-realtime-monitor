import pandas as pd 
import numpy as np 
import platform 
import matplotlib.pyplot as plt 
from selenium import webdriver 
import time

driver = webdriver.Chrome('./chromedriver') 
driver.get('http://info.nec.go.kr')


# 1. 홈페이지 접근
driver.switch_to_default_content()
driver.switch_to_frame('main')

# 2. 역대선거 클릭
driver.find_element_by_class_name("eright").click()

# 3. 투개표 클릭
driver.find_element_by_xpath("""//*[@id="presubmu"]/li[3]/a""").click()

# 4. 개표현황 클릭
driver.find_element_by_xpath("""//*[@id="header"]/div[4]/ul/li[4]/a""").click()

# 5. 대통령선거 클릭
driver.find_element_by_xpath("""//*[@id="electionType1"]""").click()

# 6. 몇대 선거를 선택할지 및 선거 시도
