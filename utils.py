from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from parsel import Selector
from bs4 import BeautifulSoup

def search_restaurant(driver, restaurant_name):
    query = driver.find_element(By.CLASS_NAME, 'gLFyf')
    query.clear()
    query.send_keys(restaurant_name)

    driver.find_element(By.CLASS_NAME, 'Tg7LZd').click()