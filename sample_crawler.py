import json
import time
import csv
from selenium import webdriver
from collections import OrderedDict

search_link = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='
keyword = '전시회'

driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(3)

if __name__ == '__main__':
    driver.get(search_link + keyword)
    total_num = int(driver.find_element_by_css_selector('div.page_sec._page_navi > span').text.split('/')[1])
    next_key_element = driver.find_element_by_css_selector('a.next._btn._btn_next.on')

    for i in range(total_num - 1):
        file_data = OrderedDict()
        
        title_selector = 'div.item_box > dl > dd.tit > a'
        period_selector = 'div.item_box > dl > dd.period'
        place_selector = 'div.item_box > dl > dd:nth-child(6) > a'
        place_url_selector = 'a.map'
        reserv_url_selector = 'a.resevation'
        thumb_url_selector = 'div.img_box > a > img'
        
        for j in range(2):
            ul_nth = "ul:nth-child(" + j + ") "
            for k in range(3):
                li_nth = "li:nth-child(" + j + ") "
                
                prefix = ul_nth + li_nth
                
                title_element = driver.find_elements_by_css_selector(prefix + title_selector)
                period_element = driver.find_elements_by_css_selector(prefix + period_selector)
                place_element = driver.find_elements_by_css_selector(prefix + place_selector)
                place_url_element = driver.find_elements_by_css_selector(prefix + place_url_selector)
                reserv_url_element = driver.find_elements_by_css_selector(prefix + reserv_url_selector)
                thumb_url_element = driver.find_elements_by_css_selector(prefix + thumb_url_selector)
                
                if len(title_element) > 0:
                    title = title_element[0].text
                    period = period_element[0].text
                    place = place_element[0].text
                    place_url = place_url_element[0].get_attribute('href') if len(place_url_element) > 0 else "null"
                    reserv_url = reserv_url_element[0].get_attribute('href')  if len(reserv_url_element) > 0 else "null"
                    thumb_url = thumb_url_element[0].get_attribute('src')
                    
                    file_data["title"] = title_element[0].text
                    file_data[""]
                
                
                
        title_element_list = driver.find_elements_by_css_selector('div.item_box > dl > dd.tit > a')
        period_element_list = driver.find_elements_by_css_selector('div.item_box > dl > dd.period')
        place_element_list = driver.find_elements_by_css_selector('div.item_box > dl > dd:nth-child(6) > a')
        place_key_element_list = driver.find_elements_by_css_selector('a.map')
        place_key_element_list = driver.find_elements_by_css_selector('a.resevation')
        thumb_url_element_list = driver.find_elements_by_css_selector('div.img_box > a > img')

        for j in range(len(title_element_list)):
            print('---------------------')
            print(title_element_list[j].text)
            print(period_element_list[j].text)
            print(place_element_list[j].text)
            print(place_key_element_list[j].get_attribute('href'))
            print(thumb_url_element_list[j].get_attribute('src'))
            print('---------------------')

        next_key_element.click()
        time.sleep(1)
    