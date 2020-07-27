import json
import time
import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from collections import OrderedDict

search_link = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='
keyword = '전시회'

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)

if __name__ == '__main__':
    driver.get(search_link + keyword)
    district = ['서울', '경기', '부산', '다른지역']
    
    for tab in range(4):
        driver.get(search_link + district[tab] + " " + keyword)
        time.sleep(0.5)
        
        total_num = int(driver.find_element_by_css_selector('div.page_sec._page_navi > span').text.split('/')[1])
        next_key_element = driver.find_element_by_css_selector('a.next._btn._btn_next.on')

        for i in range(total_num - 1):
            url = "http://192.249.19.242:7380/maintain"
            headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
            
            title_selector = 'div.item_box > dl > dd.tit > a'
            period_selector = 'div.item_box > dl > dd.period'
            place_selector = 'div.item_box > dl > dd:nth-child(6) > a'
            place_url_selector = 'a.map'
            reserv_url_selector = 'a.resevation'
            thumb_url_selector = 'div.img_box > a > img'
            
            for j in range(3):
                ul_nth = "ul:nth-child(" + str(j + 1) + ") > "
                for k in range(2):
                    li_nth = "li:nth-child(" + str(k + 1) + ") "
                    
                    prefix = ul_nth + li_nth
                    
                    title_element = driver.find_elements_by_css_selector(prefix + title_selector)
                    if len(title_element) > 0:
                        # Get elements
                        period_element = driver.find_elements_by_css_selector(prefix + period_selector)
                        place_element = driver.find_elements_by_css_selector(prefix + place_selector)
                        thumb_url_element = driver.find_elements_by_css_selector(prefix + thumb_url_selector)
                        
                        place_url_element = driver.find_elements_by_css_selector(prefix + place_url_selector)
                        reserv_url_element = driver.find_elements_by_css_selector(prefix + reserv_url_selector)
                        
                        # Get data
                        title = title_element[0].text
                        period = period_element[0].text
                        place = place_element[0].text
                        thumb_url = thumb_url_element[0].get_attribute('src')
                        
                        place_url = place_url_element[0].get_attribute('href') if len(place_url_element) > 0 else "null"
                        reserv_url = reserv_url_element[0].get_attribute('href')  if len(reserv_url_element) > 0 else "null"
                        
                        # Extract year, month, day
                        period_split = period.split(" ~ ")
                        start_split = period_split[0].split(".")
                        finish_split = period_split[1].split(".")
                        if len(finish_split) == 1:
                            finish_split = [0, 0, 0, 0]
                        
                        start_y, start_m, start_d, temp = tuple(start_split)
                        finish_y, finish_m, finish_d, temp = tuple(finish_split)
                        
                        start_y, start_m, start_d = int(start_y), int(start_m), int(start_d)
                        finish_y, finish_m, finish_d = int(finish_y), int(finish_m), int(finish_d)
                        
                        # Modify thumb_url
                        thumb_url = thumb_url.split("144x200")
                        thumb_url = thumb_url[0] + "256x368" + thumb_url[1]
                        
                        # Make json
                        file_data = OrderedDict()
                        
                        file_data["title"] = title
                        file_data["place"] = place
                        file_data["thumb_url"] = thumb_url
                        
                        file_data["start_y"] = start_y
                        file_data["start_m"] = start_m
                        file_data["start_d"] = start_d
                        file_data["start_num"] = start_y * 10000 + start_m * 100 + start_d
                        
                        file_data["finish_y"] = finish_y
                        file_data["finish_m"] = finish_m
                        file_data["finish_d"] = finish_d
                        file_data["finish_num"] = finish_y * 10000 + finish_m * 100 + finish_d
                        
                        file_data["place_url"] = place_url
                        file_data["reserv_url"] = reserv_url
                        
                        file_data["district"] = district[tab]
                        
                        # Send request
                        requests.post(url, data=json.dumps(file_data), headers = headers)
                    else:
                        print("Error or finished")
                        
            next_key_element.click()
            time.sleep(0.5)