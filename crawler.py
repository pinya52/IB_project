from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from parsel import Selector
from html.parser import HTMLParser
from bs4 import BeautifulSoup
import time
import random
from collections import defaultdict
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class WebDriver():
    def __init__(self):
        # 配置代理
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("detach", True)
        # chrome_options.add_argument("--proxy-server=http://35.240.219.50:8080")
        # chrome_options.add_argument("start-maximized")

        self.driver = webdriver.Chrome(
            # service=Service(ChromeDriverManager().install()),
            options=chrome_options,
        )
        self.action = webdriver.ActionChains(self.driver)
        page_content = self.driver.page_source
        self.parser = HTMLParser()
        response = Selector(page_content)

    def implicitly_wait(self, time:int):
        self.driver.implicitly_wait(time)

    def quit(self):
        self.driver.quit()
        
    def refresh(self):
        self.driver.refresh()

    def get_url(self, web_source:str):
        self.driver.get(web_source)
        self.driver.implicitly_wait(20)

    def search_restaurant(self, restaurant_name:str, restaurant_address:str):
        query = self.driver.find_element(By.CLASS_NAME, 'gLFyf')
        query.clear()
        query.send_keys('%s %s'%(restaurant_name, restaurant_address))

        self.driver.find_element(By.CLASS_NAME, 'Tg7LZd').click()

        self.driver.implicitly_wait(5)

        # try:
        #     self.driver.find_elements(By.CLASS_NAME, 'card-section')
        #     return (None, None)
        # except:
        #     pass
        
        try:
            # print(restaurant_address, restaurant_name)
            self.driver.find_element(By.CLASS_NAME, 'gqLncc.card-section.KDCVqf')
            self.driver.find_elements(By.CLASS_NAME, 'gL9Hy')[1].click()
            self.driver.implicitly_wait(5)
        except:
            pass

        try:
            search_results = self.driver.find_elements(By.CLASS_NAME, 'vwVdIc')
            
            # if len(search_results) == 1:
            #     search_results[0].click()
            
            # for result in search_results:
            #     result_name = result.find_element(By.CLASS_NAME, 'OSrXXb').get_attribute('innerHTML')
            #     result_address = result.find_element(By.CLASS_NAME, 'rllt__details').find_elements(By.TAG_NAME, 'div')[2].get_attribute('innerHTML')
            #     print(restaurant_name, restaurant_address)
            #     print(result_name, result_address)
            #     print()

            #     if restaurant_name == result_name or restaurant_address == result_address:
            #         result.click()
            #         break

            result_name = search_results[0].find_element(By.CLASS_NAME, 'OSrXXb').get_attribute('innerHTML')
            result_address = search_results[0].find_element(By.CLASS_NAME, 'rllt__details').find_elements(By.TAG_NAME, 'div')[2].get_attribute('innerHTML')

            search_results[0].click()

            return (result_name, result_address)
        except:
            return (None, None)

    def scroll_reviews(self) -> dict:
        self.driver.implicitly_wait(5) 
        total_reviews = int(self.driver.find_element(By.CLASS_NAME, 'RDApEe.YrbPuc').get_attribute("innerHTML")[1:-1])
        
        # self.driver.implicitly_wait(20) 

        rating_class_name = 'lTi8oc.z3HNkc'
        timestamp_class_name = 'dehysf.lTi8oc'
        review_class_name = 'Jtu6Td'
        user_class_name = 'TSUbDb'

        review_dict = defaultdict(tuple)
        rating_dict = defaultdict(list)
        review_found = 0
        

        # print('Scrolling...')
        progress = tqdm(total=total_reviews, desc="Scrolling", leave=False, position=1)
        # progress = 0
        while review_found < total_reviews:
            self.driver.implicitly_wait(5) 

            users = self.driver.find_elements(By.CLASS_NAME, user_class_name)

            for i in range(500):
                self.action.key_down(Keys.ARROW_DOWN).perform()

            review_found = len(users)
            if review_found == progress.n:
                break
            # progress = review_found
            progress.update(review_found-progress.n)

            time.sleep(random.randint(1, 2))
            
        progress.close()


        rating_elements = self.driver.find_elements(By.CLASS_NAME, rating_class_name)
        timestamps = self.driver.find_elements(By.CLASS_NAME, timestamp_class_name)
        reviews = self.driver.find_elements(By.CLASS_NAME, review_class_name)
        users = self.driver.find_elements(By.CLASS_NAME, user_class_name)

        # WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'TSUbDb')))
        # rating_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, rating_class_name)))
        # timestamps = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, timestamp_class_name)))
        # reviews = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, review_class_name)))

        # print('Get reviews...\n')
        for i, user in enumerate(tqdm(users, desc="Get review", leave=False, position=1)):
            # there's duplicate in raing, timestamps and comments when scrapying
            if not user in review_dict:
                # print(user.text)
                rating = rating_elements[2*i].get_attribute('aria-label')[3]
                # print(rating)
                timestamp = timestamps[2*i].get_attribute('innerHTML')
                # print((timestamp))
                review_dict[user.text] = (int(rating), timestamp, reviews[2*i])
                rating_dict[timestamp].append(int(rating))

        return review_dict, rating_dict
        

    def get_reviews(self):
        review_btn = self.driver.find_elements(By.CLASS_NAME, 'KYeOtb.rWAMad')

        if len(review_btn) == 0:
            return None, None
        
        review_btn = review_btn[-1]
        review_btn.click()
        
        try:
            self.driver.implicitly_wait(20) 
            sorting_btns = self.driver.find_elements(By.CLASS_NAME, 'AxAp9e')
            self.driver.implicitly_wait(30) 
            newest_btn = sorting_btns[1]
            time.sleep(1)
            newest_btn.click()
        except:
            review_btn = self.driver.find_elements(By.CLASS_NAME, 'KYeOtb.rWAMad')[-1]
            review_btn.click()

            self.driver.implicitly_wait(20) 
            sorting_btns = self.driver.find_elements(By.CLASS_NAME, 'AxAp9e')
            self.driver.implicitly_wait(30) 
            newest_btn = sorting_btns[1]
            time.sleep(1)
            newest_btn.click()
        time.sleep(1)

        return self.scroll_reviews()
    
    def inline_exits(self):
        outers = self.driver.find_elements(By.CLASS_NAME, 'JV5xkf')
        
        for outer in outers:
            for inner in outer.find_elements(By.CLASS_NAME, 'xFAlBc'):
                if 'inline' in inner.get_attribute('innerHTML'):
                    return True
        return False
    

    def search_restaurant_MOEA(self, restaurant_name='', restaurant_addr=''):
        query = self.driver.find_element(By.CLASS_NAME, 'form-control')
        query.clear()
        query.send_keys(restaurant_name)

        # click address
        if len(restaurant_addr):
            self.driver.find_element(By.ID, 'infoAddr').click()
            query.clear()
            query.send_keys(restaurant_addr)

        # uncheck company and check business
        self.driver.find_element(By.XPATH, '//*[@id="queryListForm"]/div[1]/div[1]/div/div[4]/div[2]/div/div/div/input[5]').click()
        self.driver.find_element(By.XPATH, '//*[@id="queryListForm"]/div[1]/div[1]/div/div[4]/div[2]/div/div/div/input[1]').click()

        # self.driver.find_element(By.CLASS_NAME, 'glyphicon.glyphicon-search').click()

        self.driver.implicitly_wait(20)

        # search
        self.driver.find_element(By.CLASS_NAME, 'btn.btn-primary').click()

        self.driver.implicitly_wait(20)
        results = self.driver.find_elements(By.CLASS_NAME, 'panel.panel-default')
        
        for result in results:
            infos = result.text.split('\n')

            if restaurant_name == infos[0]:
                result_info = {}
                result_info['店名'] = restaurant_name

                infos = infos[1].replace(' ', '').split(',')
                for info in infos:
                    temp = info.split('：')
                    result_info[temp[0]] = temp[1]

                print(result_info)
                break

                
def get_from_google():
    web_source = 'https://www.google.com/search?tbs=lf:1,lf_ui:9&tbm=lcl&q=%E9%A6%AC%E7%A5%96%E9%BA%B5%E9%A4%A8&rflfq=1&num=10&rldimm=5238133383601099463&ved=2ahUKEwiq5b7FsuL_AhVggVYBHQ8dDD8Qu9QIegQIFRAK#rlfi=hd:;si:;mv:[[25.1223384,121.56062569999999],[25.0037056,121.45101059999999]]'
    # web_source = 'https://www.google.com/search?q=momo&tbm=lcl&ei=GVeqZPOVAvbP2roPxv2ykAo&ved=0ahUKEwizhof8goGAAxX2p1YBHca-DKIQ4dUDCAk&uact=5&oq=momo&gs_lcp=Cg1nd3Mtd2l6LWxvY2FsEAMyBwgAEIoFEEMyCwgAEIAEELEDEIMBMgcIABCKBRBDMgsIABCABBCxAxCDATILCAAQgAQQsQMQgwEyCwgAEIAEELEDEIMBMggIABCABBCxAzIFCAAQgAQyCwgAEIoFELEDEIMBMgsIABCABBCxAxCDAVAAWMEeYK0laAFwAHgAgAEuiAHmAZIBATaYAQCgAQGwAQDAAQE&sclient=gws-wiz-local#rlfi=hd:;si:13015144036072985373,l,CgRtb21vSKf0s5T7qoCACFoIEAAiBG1vbW-SASNzaGFidV9zaGFidV9hbmRfc3VraXlha2lfcmVzdGF1cmFudKoBNxABKggiBG1vbW8oRTIfEAEiGyfn7m9C-Z2GUZQm_CyLbFZ-27aSjNvYMN3iujIIEAIiBG1vbW8;mv:[[25.087027000000003,121.61229180000001],[24.9658601,121.46718109999999]]'
    # web_source = 'https://www.google.com/search?q=%E7%84%A1%E8%80%81%E9%83%AD&tbm=lcl&ei=GVeqZPOVAvbP2roPxv2ykAo&ved=0ahUKEwizhof8goGAAxX2p1YBHca-DKIQ4dUDCAk&uact=5&oq=%E7%84%A1%E8%80%81%E9%83%AD&gs_lcp=Cg1nd3Mtd2l6LWxvY2FsEAMyDQgAEIAEELEDEIMBEAoyCwgAEIoFELEDEIMBMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKOggIABCABBCxAzoFCAAQgAQ6CwgAEIAEELEDEIMBOgUIABCiBFAAWNwRYO4SaANwAHgAgAEviAGGA5IBAjEwmAEAoAEBsAEAwAEB&sclient=gws-wiz-local#rlfi=hd:;si:5322316505095930375,l,CgnnhKHogIHpjYsiA4gBAUjh_cf2m6qAgAhaHRAAEAEQAhgAGAEYAiIL54ShIOiAgSDpjYsqAggCkgESaG90X3BvdF9yZXN0YXVyYW50qgFEEAEqDyIL54ShIOiAgSDpjYsoRTIeEAEiGrZ2aAr9G-ive49dRvAgLzkdAOCb_ygVo1boMg8QAiIL54ShIOiAgSDpjYs;mv:[[25.0551033,121.5231801],[25.042005699999997,121.50813249999999]]'
    driver = WebDriver()
    driver.get_url(web_source)
    # print(driver.inline_exits())
    driver.implicitly_wait(20)
    # driver.search_restaurant('108抹茶茶廊Sogo復興店', '台北市大同區華陰街91號5F')
    driver.search_restaurant('101 Diningroom', '台北市南港區新民街101號101小飯廳 ')
    
    driver.implicitly_wait(20)
    reviews, ratings = driver.get_reviews()

    for time in ratings.keys():
        ratings[time] = sum(ratings[time]) / len(ratings[time])

    print(dict(ratings))

def get_from_MOEA():
    web_source = 'https://findbiz.nat.gov.tw/fts/query/QueryBar/queryInit.do?request_locale=zh_TW&fhl=zh_TW'
    driver = WebDriver()
    driver.get_url(web_source)
    driver.search_restaurant_MOEA(restaurant_name='狗不李餐館', restaurant_addr='台北市中山區中山北路二段137巷45號')
    
if __name__ == '__main__':
    get_from_google()
    # get_from_MOEA()