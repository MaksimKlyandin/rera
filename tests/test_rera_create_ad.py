import time
import math
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from utils.auth_helper import login



link = "https://client.dev.rera.cy/"
EMAIL = "1@g.com"
OTP = "111111"

@pytest.mark.parametrize("property_type", 
["flat"])
def test_create_ad_rent(browser, property_type):
    login(browser)
    
#Этап создания
#Step 1
    create_ad_button = browser.find_element(By.CSS_SELECTOR, "button .w-5")
    create_ad_button.click()
    
    wait = WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']"))
    )
    #Deal type RENT
    deal_type_btn = browser.find_element(By.XPATH, "//label[input[@value='rent']]")
    deal_type_btn.click()
    #Property type
    property_type_btn = browser.find_element(By.XPATH, f"//label[input[@value='{property_type}']]")
    property_type_btn.click()
    
    wait = WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']"))
    )
    next_btn = browser.find_element(By.XPATH, "//button[text()='Next']")
    next_btn.click()
    element = WebDriverWait(browser, 10).until(EC.presence_of_element_located(
    (By.XPATH, "//span[text()='Step 2/7 - Location']")))
    #time.sleep(5)
    
#Step2
    map_btn = browser.find_element(By.CSS_SELECTOR, ".gap-2 > button")
    map_btn.click()
    browser.implicitly_wait(5)
    # Находим элемент карты (может зависеть от сервиса)
    map_element = browser.find_element(By.XPATH, "//canvas")
    browser.implicitly_wait(5)
    # Создаем цепочку действий для перетаскивания карты
    actions = ActionChains(browser)

    # Захватываем карту, двигаем её на 300 пикселей вправо и 200 пикселей вниз
    actions.click_and_hold(map_element).move_by_offset(300, 200).release().perform()

    # Ждем, чтобы увидеть результат
    time.sleep(3)