#pytest -s -n 4 test_rera_503.py
import requests
import pytest
import logging

# Настройка логгера для вывода только в консоль
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# URL и заголовки для выполнения запроса
url = "https://api.dev.rera.cy/api/v1/listings"
headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Origin": "https://client.dev.rera.cy",
    "Referer": "https://client.dev.rera.cy/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "accept": "application/json",
    "authorization": "Bearer 14|aZRZwvjPQ97WsV8P40ornZBId2s4eFOgQ93bgGnv59321fe3",  # Используйте актуальный токен
    "content-type": "application/json",
    "sec-ch-ua": "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "x-county": "CY",
    "x-language": "en"
}

# Данные для запроса
data = {
    "order": "created_at,asc",
    "deal_type": "rent",
    "offer_type": "residential",
    "viewport": None,
    "radius": None,
    "coordinates": None,
    "city_id": None,
    "price_from": None,
    "price_to": None,
    "with_3d": None,
    "with_video": None,
    "full_area_from": None,
    "full_area_to": None,
    "plot_area_from": None,
    "plot_area_to": None,
    "is_available": None,
    "become_available_at": None,
    "construction_year_from": None,
    "estimated_completion_at": None,
    "inchat": None,
    "above_first_floor": None,
    "not_top_floor": None,
    "window_views": [],
    "construction_stage": [],
    "heating_types": [],
    "loggias": [],
    "balconies": [],
    "elevator_count": [],
    "with_freight_elevator": None,
    "building_class": [],
    "energy_class": [],
    "with_conditioner": None,
    "with_internet": None,
    "with_phone": None,
    "is_accessible": None,
    "security_systems": [],
    "rental_type": [],
    "distance_to_bus_stops": [],
    "no_deposit": None,
    "owner_only": None,
    "residential_type": [],
    "furnished": None,
    "bedroom_type": [],
    "house_type": [],
    "flat_type": [],
    "storage_types": [],
    "parking_types": [],
    "combined_bathrooms": [],
    "separate_bathrooms": [],
    "with_bath": None,
    "shower_cubicle": None,
    "pets": [],
    "repair_type": [],
    "kitchen_furnished": None,
    "furnished_rooms": None,
    "with_tv": None,
    "with_fridge": None,
    "with_washing_machine": None,
    "with_tumble_dryer": None,
    "with_dishwasher": None,
    "with_interactive_tv": None,
    "smoking_allowed": None,
    "jacuzzi": None,
    "smart_home_features": None,
    "selling_and_looking_to_buy": None,
    "residential_common_areas": [],
    "commercial_type": [],
    "foot_traffic": [],
    "design_features": [],
    "layout_type": None,
    "common_areas": [],
    "legal_status": [],
    "advertising_installation_allowed": [],
    "equipped": None,
    "additional_details": [],
    "available_parking_spaces": [],
    "page": 1,
    "limit": 18
}

# Функция для получения общего числа доступных объектов (total_listings)
def get_total_listings():
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        #logging.info(f"Ответ API: {response_data}")  # Логируем ответ API
        total_listings = response_data.get('data', {}).get('total_listings', 0)
        return total_listings
    else:
        logging.error(f"Ошибка запроса: {response.status_code} | {response.text}")
        raise Exception(f"Ошибка запроса: {response.status_code}")

# Функция для получения ID на определенной странице
def get_listing_ids_for_page(page):
    data['page'] = page  # Устанавливаем номер страницы
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        listings = response_data.get('data', {}).get('listings', [])
        listing_ids = [listing['id'] for listing in listings if 'id' in listing]
        return listing_ids
    else:
        logging.error(f"Ошибка запроса на странице {page}: {response.status_code} | {response.text}")
        raise Exception(f"Ошибка запроса на странице {page}: {response.status_code}")

# Функция для выполнения запроса по ссылке
def check_listing_url_status(id):
    url = f"https://client.dev.rera.cy/property-search/{id}"
    response = requests.get(url)
    return response.status_code

# Тест для проверки всех страниц
def test_listing_ids_and_status_codes_for_all_pages():
    total_listings = get_total_listings()
    
    # Логирование total_listings
    logging.info(f"Общее количество объектов (total_listings): {total_listings}")

    # Проверка, что общее количество страниц больше 0
    assert total_listings > 0, "Нет доступных страниц"

    # Рассчитываем количество страниц
    total_pages = total_listings // 18 + (1 if total_listings % 18 != 0 else 0)

    # Логирование общего числа страниц
    logging.info(f"Общее количество страниц: {total_pages}")

    # Перебор всех страниц и проверка каждой
    for page in range(1, total_pages + 1):
        listing_ids = get_listing_ids_for_page(page)

        # Проверка, что список ID не пустой
        assert len(listing_ids) > 0, f"Список ID пустой на странице {page}"

        # Логирование списка ID
        logging.info(f"Полученные ID на странице {page}: {listing_ids}")

        # Проверка, что все элементы являются числами (если id - это число)
        assert all(isinstance(id, int) for id in listing_ids), f"Не все ID являются числами на странице {page}"

        # Проверка кода ответа для каждой ссылки
        for listing_id in listing_ids:
            status_code = check_listing_url_status(listing_id)
            logging.info(f"Ссылка https://client.dev.rera.cy/property-search/{listing_id} на странице {page} вернула код: {status_code}")
