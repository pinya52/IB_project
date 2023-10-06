from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from parsel import Selector
from pynput import keyboard
from pynput.keyboard import Key
from html.parser import HTMLParser
from bs4 import BeautifulSoup

from collections import defaultdict
import json
import os, sys
import random
import time
from tqdm import tqdm, trange


class WebDriver:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        service = Service(executable_path='./chromedriver.exe')

        self.driver = webdriver.Chrome(options=chrome_options, service=service)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                            'Chrome/85.0.4183.102 Safari/537.36'})
    
        self.action = webdriver.ActionChains(self.driver)
        page_content = self.driver.page_source
        self.parser = HTMLParser()
        response = Selector(page_content)

    def implicitly_wait(self, time:int):
        self.driver.implicitly_wait(time)
        
    def refresh(self):
        self.driver.refresh()

    def get_url(self, web_source:str):
        self.driver.get(web_source)
        self.driver.implicitly_wait(20)

    def kill(self):
        self.driver.close()
        self.driver.quit()

        
class GoogleMapDriver(WebDriver):
    def __init__(self):
        super().__init__()

    def implicitly_wait(self, time: int):
        return super().implicitly_wait(time)
        
    def refresh(self):
        return super().refresh()

    def get_url(self, web_source:str):
        return super().get_url(web_source)

    def kill(self):
        return super().kill()

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
    
def get_from_google():
    web_source = 'https://www.google.com/search?tbs=lf:1,lf_ui:9&tbm=lcl&q=%E9%A6%AC%E7%A5%96%E9%BA%B5%E9%A4%A8&rflfq=1&num=10&rldimm=5238133383601099463&ved=2ahUKEwiq5b7FsuL_AhVggVYBHQ8dDD8Qu9QIegQIFRAK#rlfi=hd:;si:;mv:[[25.1223384,121.56062569999999],[25.0037056,121.45101059999999]]'
    # web_source = 'https://www.google.com/search?q=momo&tbm=lcl&ei=GVeqZPOVAvbP2roPxv2ykAo&ved=0ahUKEwizhof8goGAAxX2p1YBHca-DKIQ4dUDCAk&uact=5&oq=momo&gs_lcp=Cg1nd3Mtd2l6LWxvY2FsEAMyBwgAEIoFEEMyCwgAEIAEELEDEIMBMgcIABCKBRBDMgsIABCABBCxAxCDATILCAAQgAQQsQMQgwEyCwgAEIAEELEDEIMBMggIABCABBCxAzIFCAAQgAQyCwgAEIoFELEDEIMBMgsIABCABBCxAxCDAVAAWMEeYK0laAFwAHgAgAEuiAHmAZIBATaYAQCgAQGwAQDAAQE&sclient=gws-wiz-local#rlfi=hd:;si:13015144036072985373,l,CgRtb21vSKf0s5T7qoCACFoIEAAiBG1vbW-SASNzaGFidV9zaGFidV9hbmRfc3VraXlha2lfcmVzdGF1cmFudKoBNxABKggiBG1vbW8oRTIfEAEiGyfn7m9C-Z2GUZQm_CyLbFZ-27aSjNvYMN3iujIIEAIiBG1vbW8;mv:[[25.087027000000003,121.61229180000001],[24.9658601,121.46718109999999]]'
    # web_source = 'https://www.google.com/search?q=%E7%84%A1%E8%80%81%E9%83%AD&tbm=lcl&ei=GVeqZPOVAvbP2roPxv2ykAo&ved=0ahUKEwizhof8goGAAxX2p1YBHca-DKIQ4dUDCAk&uact=5&oq=%E7%84%A1%E8%80%81%E9%83%AD&gs_lcp=Cg1nd3Mtd2l6LWxvY2FsEAMyDQgAEIAEELEDEIMBEAoyCwgAEIoFELEDEIMBMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKOggIABCABBCxAzoFCAAQgAQ6CwgAEIAEELEDEIMBOgUIABCiBFAAWNwRYO4SaANwAHgAgAEviAGGA5IBAjEwmAEAoAEBsAEAwAEB&sclient=gws-wiz-local#rlfi=hd:;si:5322316505095930375,l,CgnnhKHogIHpjYsiA4gBAUjh_cf2m6qAgAhaHRAAEAEQAhgAGAEYAiIL54ShIOiAgSDpjYsqAggCkgESaG90X3BvdF9yZXN0YXVyYW50qgFEEAEqDyIL54ShIOiAgSDpjYsoRTIeEAEiGrZ2aAr9G-ive49dRvAgLzkdAOCb_ygVo1boMg8QAiIL54ShIOiAgSDpjYs;mv:[[25.0551033,121.5231801],[25.042005699999997,121.50813249999999]]'
    driver = GoogleMapDriver()
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
    


class MOEADriver(WebDriver):
    def __init__(self):
        super().__init__()

    def implicitly_wait(self, time: int):
        return super().implicitly_wait(time)
        
    def refresh(self):
        return super().refresh()

    def get_url(self, web_source:str):
        return super().get_url(web_source)

    def kill(self):
        return super().kill()

    def search_restaurant(self, restaurant_name='', restaurant_addr=''):
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
                time.sleep(random.randint(1, 2))
                result.find_element(By.CLASS_NAME, 'hover').click()
                break

    def get_info(self):
        result_info = {"核准設立日期" : '', '資本額(元)' : '', '組織類型' : ''}

        infos = self.driver.find_element(By.CLASS_NAME, "table.table-striped").text
        infos = infos.replace("\n", " ").split(" ")

        for i, info in enumerate(infos): 
            if info in result_info.keys():
                result_info[info] = infos[i+1]

        return result_info


def get_from_MOEA():
    web_source = 'https://findbiz.nat.gov.tw/fts/query/QueryBar/queryInit.do?request_locale=zh_TW&fhl=zh_TW'
    driver = MOEADriver()
    driver.get_url(web_source)
    driver.search_restaurant(restaurant_name='狗不李餐館', restaurant_addr='台北市中山區中山北路二段137巷45號')
    info = driver.get_info()
    print(info)



class DataAIDriver(WebDriver):
    def __init__(self):
        super().__init__()
        self._top500_link = []

    def implicitly_wait(self, time: int):
        return super().implicitly_wait(time)
        
    def refresh(self):
        return super().refresh()

    def get_url(self, web_source:str):
        return super().get_url(web_source)

    def kill(self):
        return super().kill()

    @property
    def top500_link(self):
        return self._top500_link

    def login(self, email, password):
        [email_query, password_query] = self.driver.find_elements(By.CLASS_NAME, 'UcTextField__Input-sc-pe1svn-0.hQFFTp')
        email_query.clear()
        email_query.send_keys(email)
        time.sleep(random.randint(1, 2))

        password_query.clear()
        password_query.send_keys(password)
        time.sleep(random.randint(1, 2))

        self.driver.find_element(By.CLASS_NAME, 'Button__ButtonBlank-sc-hyde8s-2.Button__UCButton-sc-hyde8s-4.hXRtgJ.jASK').click()

        time.sleep(random.randint(1, 2))
        
        # wait = WebDriverWait(self.driver, 30)
        # element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'Button__ButtonBlank-sc-hyde8s-2.Button__UCButton-sc-hyde8s-4.hXRtgJ.jASK')))
        time.sleep(30)
        self.driver.find_element(By.CLASS_NAME, 'Button__ButtonBlank-sc-hyde8s-2.Button__UCButton-sc-hyde8s-4.hXRtgJ.jASK').click()
        self.driver.implicitly_wait(20)

    def scroll_window(self):
        self.driver.implicitly_wait(5)
        app = set()
        links = []

        # print('Scrolling...')
        progress = tqdm(total=100, desc="Scrolling", leave=False, position=1)
        # progress = 0
        with open('link.txt', 'a') as f:
            while len(app) < 100:
                
                app_links = self.driver.find_elements(By.CLASS_NAME, 'FlexView-sc-eu9ylc-0.NZFLj.entity-name.FlexView.entity-name')

                for app_link in app_links:
                    link = app_link.find_element(By.CLASS_NAME, 'Touchable__TouchableBase-sc-1anmdnm-0.fnkjgx.styles__ButtonText-sc-n1y5g3-1.jefKNv')
                    if link.text not in app:
                        # print(link.text)
                        links.append((link.text, link.get_attribute("href")))
                        app.add(link.text)
                        # link[app_link[i].text] = app_link[i].get_attribute("href").split('/')[6]

                        f.writelines(link.text)
                        f.writelines('\n')
                        f.writelines(link.get_attribute("href"))
                        f.writelines('\n\n')

                for i in range(10):
                    self.action.key_down(Keys.ARROW_DOWN).perform()

                time.sleep(1)

                progress.update(len(app)-progress.n)
            
        progress.close()
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        return links

    def topChart_APP(self):
        self.get_url('https://www.data.ai/intelligence/top-apps/downloads-revenue/downloads?country_code=!(WW)&device_code=ios-all&unified_category_id=!(800000)&date=!(%272019-01-01%27,%272022-12-31%27)&granularity=monthly&order_by=!((name:est_download__sum,order:desc))&top-apps.breakdown=app&table_change(top_apps_by_downloads_rank_table)=(status:!t,type:value_change,unit:PERIOD)')
        self.driver.implicitly_wait(5)

        for _ in trange(5, position=0):
            self.driver.implicitly_wait(5) 
            app_link = self.scroll_window()
            self._top500_link += app_link

            self.driver.implicitly_wait(5)
            next_page = self.driver.find_elements(By.CLASS_NAME, 'Touchable__TouchableBase-sc-1anmdnm-0.fnkjgx.styles__ButtonBase-sc-n1y5g3-0.euwwje.button-secondary.is-small.is-icon-only')[-1]
            next_page.click()
            self.driver.implicitly_wait(5)

        # print(len(self._top500_link))

        # print(self._top500_link[0])
        # print(self.top500_link[list(self.top500_link.keys())[1]])

    def get_description(self, app):
        (app_name, link) = app
        self.get_url(link)
        time.sleep(0.5)

        for i in range(15):
            self.action.key_down(Keys.ARROW_DOWN).perform()

        description = self.driver.find_element(By.CLASS_NAME, 'AppStoreNotes__Wrapper-sc-1235je2-0.iQkxXV').text
        print(description, '\n\n')
        time.sleep(0.5)

        return description

    def get_info(self, app):
        (app_name, link) = app
        self.get_url(link)
        time.sleep(0.5)

        for i in range(15):
            self.action.key_down(Keys.ARROW_DOWN).perform()

        description = self.driver.find_element(By.CLASS_NAME, 'AppStoreNotes__Wrapper-sc-1235je2-0.iQkxXV').text
        print(description, '\n\n')
        time.sleep(0.5)


        # def get_genre(web_element):
        #     genres = web_element.find_elements(By.CLASS_NAME, 'Button__ButtonBlank-sc-hyde8s-2.Button__ButtonTertiary-sc-hyde8s-3.AppClassifications__StyledButtonTertiary-sc-bj2n4u-1.hXRtgJ.gaIUpJ.jhjWri')
            
        #     return [genre.text.split(' ')[-1] for genre in genres]  
        

        # primary_classification = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/main/div/div[2]/div[2]/div[3]/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]')
        # sencondary_classification = self.driver.find_elements(By.CLASS_NAME, "FlexView-sc-eu9ylc-0.bnnTjk.FlexView")
        # primary_classification = get_genre(primary_classification)
        # sencondary_classification = get_genre(sencondary_classification)

        classifications = self.driver.find_elements(By.CLASS_NAME, "Button__ButtonBlank-sc-hyde8s-2.Button__ButtonTertiary-sc-hyde8s-3.AppClassifications__StyledButtonTertiary-sc-bj2n4u-1.hXRtgJ.gaIUpJ.jhjWri")
        classifications = [classification.text.split(' ')[-1] for classification in classifications]
        # print(classifications, '\n\n')

        time.sleep(0.5)

        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        abouts = self.driver.find_elements(By.CLASS_NAME, 'AppAbout__ItemWrapper-sc-m4u0il-1.gXvyRh')

        info = {"name" : app_name, "Description" : description, 
                        "Classifications": classifications, "Num of Classifications" : len(classifications),
                        "Initial Release Date" : "", "Worldwide Release Date" : "", 
                        "Size" : "", "Languages" : "''", "Num_of_Languages" : 0, "Has Game Center" : "''"}

        for about in abouts:
            try:
                about_type = about.find_element(By.TAG_NAME, "dt").text
                # print(about_type, '\n')
                if about_type in info:
                    info[about_type] = about.find_element(By.TAG_NAME, "dd").text
            except:
                break

        info['Num_of_Languages'] = len(info["Languages"].split(','))
        # print(info)

        return info

def get_from_DataAI(email, password):
    web_source = "https://www.data.ai/account/login"
    driver = DataAIDriver()
    driver.get_url(web_source)
    driver.implicitly_wait(20)

    driver.login(email, password)
    
    driver.topChart_APP()
    top500_link = driver.top500_link
    # print(top500_link)
    # print(len(top500_link))

    save_path = 'app_info_2.json'

    if os.path.isfile('app_info.json'):
        with open('app_info.json', newline='') as jsonfile:
            app_infos = json.load(jsonfile)
            print(len(app_infos))
    else:
        app_infos = []

    # app_infos = []

    for i, app in enumerate(tqdm(top500_link, desc='Get app info')):
        # info = driver.get_info(app)
        # app_infos.append(info)

        description = driver.get_description(app)
        app_infos[i]['Description'] = description
        with open(save_path, 'w', newline='') as jsonfile:
            json.dump(app_infos, jsonfile, indent=4)
        time.sleep(2.5)
        
    
if __name__ == '__main__':
    # get_from_google()
    # get_from_MOEA()
    get_from_DataAI('r11922158@ntu.edu.tw', 'ca06BN12/')