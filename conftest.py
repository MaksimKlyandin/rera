import pytest
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Настроим логирование на уровне INFO
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_driver(browser_name):
    """Функция выбора WebDriver в зависимости от переданного параметра."""
    if browser_name == "chrome":
        logger.info("\nЗапускаем Chrome...")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
    elif browser_name == "firefox":
        logger.info("\nЗапускаем Firefox...")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)
    else:
        raise ValueError(f"Браузер '{browser_name}' не поддерживается. Используйте 'chrome' или 'firefox'.")
    
    driver.maximize_window()
    return driver

@pytest.fixture(scope="function")
def browser(request):
    """Фикстура для запуска браузера с выбором Chrome или Firefox."""
    browser_name = request.config.getoption("--browser_name")
    driver = get_driver(browser_name)
    
    yield driver  # Передаем WebDriver в тест
    
    logger.info("\nЗакрываем браузер...")
    driver.quit()

def pytest_addoption(parser):
    """Добавляем параметр --browser_name для выбора браузера при запуске тестов."""
    parser.addoption("--browser_name", action="store", default="chrome",
                     help="Выберите браузер: chrome или firefox")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    
    if report.failed:  # Если тест упал
        with open(item.fspath, 'r', encoding='utf-8') as f:  # Указана кодировка 'utf-8'
            lines = f.readlines()
            failed_line = lines[report.location[1] - 1].strip()
            logger.error(f"\n🔴 Тест упал на строке: {report.location[1]} → {failed_line}")
