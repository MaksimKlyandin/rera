import pytest
import requests
import logging
import json

# Настроим логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://api.dev.rera.cy/api/v1/listings"
CLIENT_URL = "https://client.dev.rera.cy"
HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Origin": CLIENT_URL,
    "Referer": f"{CLIENT_URL}/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "accept": "application/json",
    "authorization": "Bearer 14|aZRZwvjPQ97WsV8P40ornZBId2s4eFOgQ93bgGnv59321fe3",
    "content-type": "application/json",
    "x-county": "CY",
    "x-language": "en",
}

def fetch_listings(page):
    """Функция для получения списка недвижимости на указанной странице."""
    payload = {
        "order": "created_at,asc",
        "deal_type": "rent",
        "offer_type": "residential",
        "page": page,
        "limit": 18
    }
    response = requests.post(BASE_URL, headers=HEADERS, json=payload)
    return response

def safe_decode(content):
    """Пытаемся декодировать байты с использованием нескольких кодировок."""
    try:
        # Пробуем UTF-8
        return content.decode('utf-8')
    except UnicodeDecodeError:
        try:
            # Если UTF-8 не сработал, пробуем ISO-8859-1
            return content.decode('ISO-8859-1')
        except UnicodeDecodeError:
            # Если и это не помогает, пытаемся заменить ошибочные символы
            return content.decode('utf-8', errors='replace')

@pytest.mark.parametrize("page", range(1, 10))
def test_listings_pages(page):
    """Тестирование получения страниц списка недвижимости."""
    # Получаем ответ от API
    response = fetch_listings(page)
    assert response.status_code == 200, f"Ошибка {response.status_code} на странице {page}"
    
    # Получаем байтовое содержимое ответа
    response_content = response.content
    response_text = safe_decode(response_content)

    # Логируем первые 500 символов ответа для диагностики
    logger.info(f"Ответ от сервера на странице {page}: {response_text[:500]}...")  # Печатаем первые 500 символов
    
    try:
        # Если это JSON, то обрабатываем как JSON
        response_data = json.loads(response_text)
        
        # Проверка, что 'data' существует и это список
        if 'data' in response_data and isinstance(response_data['data'], list):
            ids = [listing['id'] for listing in response_data['data']]  # Извлекаем 'id' из JSON-ответа
        else:
            logger.error(f"Ошибка: 'data' нет или это не список. Ответ: {response_data}")
            ids = []
    except json.JSONDecodeError:
        # Если это не JSON, продолжаем с BeautifulSoup для HTML
        logger.error(f"Ошибка декодирования JSON для страницы {page}: {response_text}")
        ids = []

    # Логируем список ID для текущей страницы
    logger.info(f"Список ID на странице {page}: {ids}")
    
    for property_id in ids:
        property_url = f"{CLIENT_URL}/property-search/{property_id}"
        logger.info(f"Переход по ссылке: {property_url}")
        property_response = requests.get(property_url, headers=HEADERS)
        
        # Применяем кодировку для второго запроса
        property_response.encoding = 'utf-8'  # Явно указываем кодировку для второго запроса

        status = "PASS" if property_response.status_code == 200 else "FAIL"
        
        # Логируем результат
        logger.info(f"Страница {page}, ID {property_id}: {status}")
        
        assert property_response.status_code == 200, f"Ошибка {property_response.status_code} на {property_url}"
