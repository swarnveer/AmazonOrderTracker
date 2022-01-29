from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import CHROME_PATH, ORDER_URL
from initialize_chrome import initialize_driver
from login import initiate_login
from get_orders import get_order_list

driver = initialize_driver(CHROME_PATH)
driver.maximize_window()

initiate_login(driver, ORDER_URL)
get_order_list(driver)
