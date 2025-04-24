import time
import logging
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)
link = "https://client.dev.rera.cy/"
EMAIL = f"{random.randint(1, 9999)}@g.com"
OTP = "111111"
def login(browser, email="1@g.com", otp="111111"):
    logger.info("Starting login process...")
    link = "https://client.dev.rera.cy/"
    browser.get(link)
    logger.info(f"Navigated to {link}")
    
    # Wait for and click login button
    logger.info("Waiting for login button...")
    button = WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/auth/login"]'))
    )
    browser.find_element(By.CSS_SELECTOR, 'a[href="/auth/login"]').click()
    logger.info("Clicked login button")
    
    # Enter email
    WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
    )
    logger.info(f"Entering email: {email}")
    email_input = browser.find_element(By.CSS_SELECTOR, "input[type='email']")
    email_input.send_keys(email)
    confirm_button = browser.find_element(By.CSS_SELECTOR, ".rk-button--primary")
    confirm_button.click()
    logger.info("Email submitted")
    
    # Enter OTP
    logger.info("Waiting for OTP input...")
    button = WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Code']"))
    )
    otp_input = browser.find_element(By.XPATH, "//input[@type='text']")
    otp_input.send_keys(otp)
    logger.info("OTP entered")
    
    # Wait for main screen
    logger.info("Waiting for main screen...")
    WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.XPATH, "//button[text()=' Create an Ad']"))
    )
    logger.info("Login completed successfully")