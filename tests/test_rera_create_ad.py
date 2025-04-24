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


def test_create_ad_rent(browser):
    login(browser)
    
#Этап создания
#Step 1
    create_ad_button = browser.find_element(By.CSS_SELECTOR, "button:has(svg.w-5)")
    create_ad_button.click()
    
    wait = WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Next']"))
    )
    #Deal type RENT
    deal_type_btn = browser.find_element(By.XPATH, "//label[input[@value='rent']]")
    deal_type_btn.click()
    #Property type
    property_type_btn = browser.find_element(By.XPATH, "//label[input[@value='flat']]")
    property_type_btn.click()
    
    wait = WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".min-w-32 > button"))
    )
    next_btn = browser.find_element(By.CSS_SELECTOR, ".min-w-32 > button")
    actions = ActionChains(browser)
    # Скролл и клик одной цепочкой действий
    actions.move_to_element(next_btn).click().perform()
    element = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
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
    actions.click_and_hold(map_element).move_by_offset(30, 20).release().perform()

    # Ждем завершения анимации более надежным способом
    #WebDriverWait(browser, 5).until(
    #    EC.presence_of_element_located((By.CSS_SELECTOR, ".leaflet-grab"))
    #)
    #time.sleep(5)
    next_btn = WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".min-w-32 > button"))
    )
    time.sleep(3)
    actions = ActionChains(browser)
    # Скролл и клик одной цепочкой действий
    actions.move_to_element(next_btn).click().perform()
#Step 3
    wait_screen3 = WebDriverWait(browser, 30).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, "span > span")))
    time.sleep(3)

    # Click on flat type dropdown
    flat_type_dropdown = browser.find_element(By.XPATH, "//span[text()='Flat type']/following-sibling::div//button")
    flat_type_dropdown = WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Flat type']/following-sibling::div//button"))
    )
    actions.move_to_element(flat_type_dropdown).click().perform()
    time.sleep(3)

    # Select Apartment option
    apartment_option = browser.find_element(By.XPATH, "//button//span[text()='Apartment']")
    actions.move_to_element(apartment_option).click().perform()