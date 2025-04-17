import time

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestAnalyzeTextAPI:
    client: APIClient
    url: str
    valid_text: str
    invalid_text: str

    def setup_method(self):
        self.client = APIClient()
        self.url = reverse('analyze_text')
        self.valid_text = "Одним солнечным днём они решили сделать что-то необычноые. Вместо того, чтобы оставаться дома, Владислав и Екатерина решили устроить путешествие. Они выбрали современный город. Им оказался Москва."
        self.invalid_text = ""

    def test_successful_text_analysis(self):
        """Тест успешного анализа текста"""
        data = {"text": self.valid_text}
        response = self.client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'language' in response.data
        assert 'entities' in response.data
        assert 'fuzzy_matched' in response.data
        assert 'error' not in response.data

    def test_caching_behavior(self):
        """Тест кэширования запросов"""
        data = {"text": self.valid_text}

        # Первый запрос - должен идти в сервис
        response1 = self.client.post(self.url, data, format='json')

        # Второй запрос с тем же текстом - должен браться из кэша
        response2 = self.client.post(self.url, data, format='json')

        assert response1.data == response2.data

    def test_empty_text_validation(self):
        """Тест валидации пустого текста"""
        data = {"text": self.invalid_text}
        response = self.client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert 'error' in response.data

    def test_invalid_payload(self):
        """Тест невалидного запроса (без текста)"""
        data = {}  # нет поля 'text'
        response = self.client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert 'error' in response.data

    @pytest.mark.parametrize(
        "text",
        [
            "Vladiaslav and Ekaterina go to Moscow",
            "Voronezh it's beautiful city",
            "Svetlana Live in Kirov",
            "Владислав приоберает новую машину в Воронеже",
            "Паша живёт в Лондоне",
        ],
    )
    def test_various_text_inputs(self, text):
        """Параметризованный тест с разными текстами"""
        data = {"text": text}
        response = self.client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert 'language' in response.data

    def test_response_time_under_3_seconds(self):
        """Тест на то, что ответ приходит быстрее 3 секунд"""
        data = {"text": self.valid_text}
        start_time = time.time()

        response = self.client.post(self.url, data, format='json')

        duration = time.time() - start_time
        assert duration < 3, f"Ответ сервера занял слишком много времени: {duration:.2f} сек"
        assert response.status_code == status.HTTP_200_OK
