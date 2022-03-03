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
page = '투표현황'

def crawl_nec():
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome('./chromedriver', options=options) 
    #1.개표현황 주소로 이동 
    print("Opening the browser with headless mode...")
    if(page == '투표현황'):
     driver.get('http://info.nec.go.kr/main/showDocument.xhtml?electionId=0000000000&topMenuId=VC&secondMenuId=VCVP01')
    else:
     driver.get('http://info.nec.go.kr/main/showDocument.xhtml?electionId=0000000000&topMenuId=VC&secondMenuId=VCAP01')

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

    #5. 시도군 리스트 가져오기

    city_list_raw = driver.find_element_by_xpath("""//*[@id="cityCode"]""") 
    city_list=city_list_raw.find_elements_by_tag_name("option") 
    city_names = [option.text for option in city_list] 
    city_names = city_names[1:]  # city_names[2:] ==> city_names[1:] 서울특별시 추가

    print(city_names)

    #5-1, 투표일자 리스트 가져오기 
    if(page != '투표현황'):
        date_list_raw = driver.find_element_by_xpath("""//*[@id="dateCode"]""");
        date_list = date_list_raw.find_elements_by_tag_name("option")
        date_names = [option.text for option in date_list]
        date_names = date_names[1:]

    #6. 각 시도별로 데이터 긁어오기 
    def get_vote(n):
        name = n
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        tmp = soup.find_all('td','alignR')
        # gu = soup.find('tbody>tr')
        # gu.select_one(":nth-child(1)")
        gu = []
        for td in soup.select('table#table01>tbody>tr>td:nth-child(1)'):
            #print('class' in (td.attrs.keys()))
            if('class' in (td.attrs.keys())):
              continue
            else:
              gu.append(td)
        gu_names = [tmp_val.get_text().strip() for tmp_val in gu[1:]]
        tmp_list = []

        # 한 줄에 총 18개의 column이 있음. 그 다음줄의 18개는 퍼센트이므로 건너뜀.
        if page =='투표현황':
            for i in range(0,len(tmp),31):
                tmp_values = [(tmp_val.get_text().replace(',','')) for tmp_val in tmp[i:i+15]]
                tmp_list.append(tmp_values)
        else:
            for i in range(0,len(tmp),27):
                tmp_values = [(tmp_val.get_text().replace(',','')) for tmp_val in tmp[i:i+13]]
                tmp_list.append(tmp_values)
            #print(len(tmp_values))
        #print(tmp_list)
        #처음의 시도 총합과 필요없는 데이터 trim
        tmp_list=tmp_list[1:] #[1:-1]->[1:]

        gu_dict={}

        for i in range(len(tmp_list)):
            name=gu_names[i] #2i+1 -> i
            items=tmp_list[i]
            gu_dict[name] = items
            
        print(gu_dict)
        #Pandas 데이터프레임으로 변환
        result = pd.DataFrame.from_dict(gu_dict).T

        #19대 기준으로 18개의 column 지정
        # result.columns=['선거인수','투표수','이재명','윤석열','심상정','안철수','오준호','허경영','이백윤','옥은호','김동연','김경재','조원진','김재연','이경희','김민찬', '합계', '무효', '기권']
        #result.columns=['선거인수','투표수','문재인','홍준표','안철수','유승민','심상정','조원진','오영국','장성민','이재오','김선동','이경희','윤홍식','김민찬', '합계', '무효', '기권']
        if page == '투표현황':
            result.columns=['선거인수','7시','8시','9시','10시','11시','12시','13시','14시','15시','16시','17시','18시','19시','20시']
        else:
            result.columns=['선거인수','7시','8시','9시','10시','11시','12시','13시','14시','15시','16시','17시','18시']
        #각 구들의 광역시 / 도 에대한 정보 column을 추가
        result['광역시도'] = n
        result.reset_index(inplace=True)
        result.rename(index=str, columns={"index":"시군"}, inplace =True)

        return result

    # 각 도시에 대한 루프
    if page == '투표현황':
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
        
        driver.quit()

        return result.to_html()
    else:
        for i in date_names:
            print(i)
            for city in city_names:
                print("Crawling " + city + "...")
                element = driver.find_element_by_id('cityCode')
                element.send_keys(city) # 도시를 선택
                element = driver.find_element_by_id('dateCode')
                element.send_keys(i)
                driver.find_element_by_xpath("""//*[@id="searchBtn"]""").click() # 검색버튼
                tmp = get_vote(city)
                if city == city_names[0]:
                    result = tmp
                else:
                    result = result.append(tmp)
            
            driver.quit()

            return result.to_html()
    
