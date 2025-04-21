import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(browser, email="1@g.com", otp="111111"):
    link = "https://client.dev.rera.cy/"
    browser.get(link)
    
    # Wait for and click login button
    button = WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/auth/login"]'))
    )
    browser.find_element(By.CSS_SELECTOR, 'a[href="/auth/login"]').click()
    
    # Enter email
    email_input = browser.find_element(By.CSS_SELECTOR, "input")
    email_input.send_keys(email)
    confirm_button = browser.find_element(By.CSS_SELECTOR, ".rk-button--primary")
    confirm_button.click()
    
    # Enter OTP
    button = WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Code']"))
    )
    otp_input = browser.find_element(By.XPATH, "//input[@type='text']")
    otp_input.send_keys(otp)
    
    # Wait for main screen
    WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()=' Create an Ad']"))
    )