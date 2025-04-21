import time
import math
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.auth_helper import login

link = "https://client.dev.rera.cy/"
EMAIL = "1@g.com"
OTP = "111111"

def test_auth(browser):
    login(browser)
    # Add any additional test steps here

