import pytest
import requests

BASE_URL = "https://client.dev.rera.cy/property-search/"

@pytest.mark.parametrize("property_id", range(700, 730))  # Проверяем страницы с ID от 1 до 10
def test_property_page_status(property_id):
    url = f"{BASE_URL}{property_id}"
    response = requests.get(url)

    if response.status_code == 404:
        # Страница не найдена, но это не ошибка
        print(f"Page {url} returned 404 (not found).")
        return

    elif response.status_code == 500:
        # Страница с ошибкой на сервере, тест помечаем как failed
        pytest.fail(f"Page {url} returned 500 (server error).")

    elif response.status_code == 200:
        # Страница валидна
        print(f"Page {url} is valid (status 200).")
    else:
        # Любой другой неожиданный код статуса
        pytest.fail(f"Unexpected status code {response.status_code} for {url}")
