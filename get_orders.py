from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

import pandas as pd
from process_generated_file import *

orders_df = pd.DataFrame(columns=["Order Date","Order Value","Order Name", "Order Type", "Order Link"])

def get_order_details(driver):
    global orders_df
    driver.implicitly_wait(5)
    ordersContainer = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.ID, 'ordersContainer')))
    individual_orders = ordersContainer.find_elements(By.CLASS_NAME, 'order')
    for order in individual_orders:
        order_date = order.find_element(By.XPATH, 'div[1]/div/div/div/div[1]/div/div[1]/div[2]/span').text
        order_value = order.find_element(By.XPATH, 'div[1]/div/div/div/div[1]/div/div[2]/div[2]/span/span').text
        order_number = order.find_element(By.XPATH, 'div[1]/div/div/div/div[2]/div[1]/span[2]/bdi').text
        try:
            order_type = order.find_element(By.XPATH, 'div[2]/div/div[1]/div[1]/div[1]/span')
            order_type = order_type.text
            try:
                order_name = order.find_element(By.XPATH, 'div[2]/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]/a').text
            except NoSuchElementException:
                order_name = 'Multiple items in order'
            if(order_type.lower() in ['money added', 'successful']):
                order_link = 'NA'
            else:
                try:
                    order_link = order.find_element(By.XPATH, 'div[2]/div/div[2]/div/div[1]/div/div/div/div[2]/div[1]/a').get_attribute('href')
                except NoSuchElementException:
                    order_link = 'NA'
        except NoSuchElementException:
            order_type = "Delivered"
            try:
                order_name = order.find_element(By.XPATH, 'div[2]/div/div/div/div[1]/div/div/div/div[2]/div[1]/a').text
            except NoSuchElementException:
                order_name = 'Multiple items in order'
            try:
                order_link = order.find_element(By.XPATH, 'div[2]/div/div/div/div[1]/div/div/div/div[2]/div[1]/a').get_attribute('href')
            except NoSuchElementException:
                order_link = 'NA'

        #print(order_name,order_date,order_value,order_number,order_type,order_link)
        orders_df = orders_df.append(
                                    {
                                    "Order Date": order_date.strip(), "Order Value": float(order_value.strip().replace(',','')),
                                    "Order Name": order_name.strip(), "Order Type": order_type.strip(), "Order Link": order_link.strip()
                                    },ignore_index=True)
def get_order_list(driver):
    try:
        element = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.ID, 'yourOrders')))
    except Exception:
        driver.quit()
    order_years_list_id = driver.find_element(By.ID,'orderFilter')
    order_years = order_years_list_id.find_elements(By.TAG_NAME, 'option')
    years=[year.text for year in order_years if(len(year.text)==4)]

    for year in years:
        order_years_list_id = driver.find_element(By.ID,'orderFilter')
        select = Select(order_years_list_id)
        select.select_by_visible_text(year)
        get_order_details(driver)
        while True:
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, 'html/body/div[1]/div[2]/div[1]/div[5]/div[12]/div/ul/li[12]/a'))).click()
                get_order_details(driver)
            except Exception:
                break
    process_excel(orders_df)
