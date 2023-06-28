from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from parsel import Selector
from bs4 import BeautifulSoup
import time
import random


class WebDriver:

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.action = webdriver.ActionChains(self.driver)
        page_content = self.driver.page_source
        response = Selector(page_content)

    def implicitly_wait(self, time:int):
        self.driver.implicitly_wait(time)

    def get_url(self, web_source:str):
        self.driver.get(web_source)

    def search_restaurant(self, restaurant_name:str):
        query = self.driver.find_element(By.CLASS_NAME, 'gLFyf')
        query.clear()
        query.send_keys(restaurant_name)

        self.driver.find_element(By.CLASS_NAME, 'Tg7LZd').click()

        self.driver.implicitly_wait(20)

        search_results = self.driver.find_elements(By.CLASS_NAME, 'vwVdIc')
        search_results[1].click()

    def scroll_reviews(self) -> dict:
        self.driver.implicitly_wait(20) 
        total_reviews = int(self.driver.find_element(By.CLASS_NAME, 'RDApEe.YrbPuc').get_attribute("innerHTML")[1:-1])

        wait = WebDriverWait(driver, 20)

        rating_class_name = 'lTi8oc.z3HNkc'
        timestamp_class_name = 'dehysf.lTi8oc'
        review_class_name = 'Jtu6Td'
        user_class_name = 'TSUbDb'

        review_dict = {}
        review_found = 0

        while review_found < total_reviews:
            self.driver.implicitly_wait(20) 

            rating_elements = self.driver.find_elements(By.CLASS_NAME, rating_class_name)
            timestamps = self.driver.find_elements(By.CLASS_NAME, timestamp_class_name)
            reviews = self.driver.find_elements(By.CLASS_NAME, review_class_name)
            users = self.driver.find_elements(By.CLASS_NAME, user_class_name)
            # WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'TSUbDb')))
            # rating_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, rating_class_name)))
            # timestamps = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, timestamp_class_name)))
            # reviews = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, review_class_name)))

            for i, user in enumerate(users):
                # there's duplicate in raing, timestamps and comments when scrapying
                if not user in review_dict:
                    print(user.text)
                    rating = rating_elements[2*i].get_attribute('aria-label')[3]
                    print(rating)
                    timestamp = timestamps[2*i].get_attribute('innerHTML')
                    print((timestamp))
                    review_dict[user.text] = (rating, timestamp, reviews[2*i])
            
            exit()

            for i in range(100):
                self.action.key_down(Keys.ARROW_DOWN).perform()

            review_found = len(review_dict)
            print("review found : %d/%d"%(review_found, total_reviews))

            time.sleep(random.randint(2, 5))

        return review_dict
        

    def get_reviews(self):
        review_btn = self.driver.find_elements(By.CLASS_NAME, 'KYeOtb')[-1]
        review_btn.click()

        self.driver.implicitly_wait(20) 
        sorting_btns = self.driver.find_elements(By.CLASS_NAME, 'AxAp9e')
        self.driver.implicitly_wait(20) 
        newest_btn = sorting_btns[1]
        time.sleep(1)
        newest_btn.click()

        time.sleep(1)

        return self.scroll_reviews()

web_source = 'https://www.google.com/search?tbs=lf:1,lf_ui:9&tbm=lcl&q=%E9%A6%AC%E7%A5%96%E9%BA%B5%E9%A4%A8&rflfq=1&num=10&rldimm=5238133383601099463&ved=2ahUKEwiq5b7FsuL_AhVggVYBHQ8dDD8Qu9QIegQIFRAK#rlfi=hd:;si:;mv:[[25.1223384,121.56062569999999],[25.0037056,121.45101059999999]]'
driver = WebDriver()
driver.get_url(web_source)
driver.implicitly_wait(20)
driver.search_restaurant('肯德基')
driver.implicitly_wait(20)
driver.get_reviews()