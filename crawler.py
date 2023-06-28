from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
from bs4 import BeautifulSoup

from utils import *

# def search_restaurant(restaurant_name):
#     query = driver.find_element(By.CLASS_NAME, 'gLFyf')
#     query.clear()
#     query.send_keys(restaurant_name)

#     driver.find_element(By.CLASS_NAME, 'Tg7LZd').click()
    
def see_comment():
    search_results = driver.find_elements(By.CLASS_NAME, 'vwVdIc')
    search_results[3].click()

    driver.implicitly_wait(20) 

    comment_btn = driver.find_elements(By.CLASS_NAME, 'KYeOtb')[-1]
    comment_btn.click()
    # comment_btn = driver.find_element('xpath', '//*[@id="akp_tsuid_21"]/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[5]/div[1]/g-sticky-content/div/div[1]/g-tabs/div/div/a[3]/div[1]')
    html = comment_btn.get_attribute('outerHTML')
    attrs = BeautifulSoup(html, 'html.parser').a.attrs
    print(attrs)



chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
page_content = driver.page_source
response = Selector(page_content)

web_source = 'https://www.google.com/search?tbs=lf:1,lf_ui:9&tbm=lcl&q=%E9%A6%AC%E7%A5%96%E9%BA%B5%E9%A4%A8&rflfq=1&num=10&rldimm=5238133383601099463&ved=2ahUKEwiq5b7FsuL_AhVggVYBHQ8dDD8Qu9QIegQIFRAK#rlfi=hd:;si:;mv:[[25.1223384,121.56062569999999],[25.0037056,121.45101059999999]]'
driver.get(web_source)

search_restaurant(driver, '肯德基')

driver.implicitly_wait(20) 

# search_results = driver.find_elements('xpath', '//*[contains(@id, "tsuid_")]/div[2]/div/div/a/div')
search_results = driver.find_elements(By.CLASS_NAME, 'vwVdIc')
search_results[3].click()

driver.implicitly_wait(20) 

comment_btn = driver.find_elements(By.CLASS_NAME, 'KYeOtb')[-1]
comment_btn.click()
# comment_btn = driver.find_element('xpath', '//*[@id="akp_tsuid_21"]/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[5]/div[1]/g-sticky-content/div/div[1]/g-tabs/div/div/a[3]/div[1]')
# html = comment_btn.get_attribute('outerHTML')
# attrs = BeautifulSoup(html, 'html.parser').a.attrs
# print(attrs)

driver.implicitly_wait(20) 
sorting_btns = driver.find_elements(By.CLASS_NAME, 'AxAp9e')
# driver.implicitly_wait(20) 
newest_btn = sorting_btns[1]
newest_btn.click()

reviews = driver.find_element('id', 'tsuid_OZiaZMmiKtqB2roPitWg2Aw_1reviewSort')
print(reviews)

# comment_btn = driver.find_elements(By.CLASS_NAME, 'KYeOtb')
# print(comment_btn)