from selenium import webdriver
from selenium.webdriver.chrome.service import Service
def initialize_driver(PATH):
    ser = Service(PATH)
    driver = webdriver.Chrome(service=ser)
    return driver
