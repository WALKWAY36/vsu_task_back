import logging
import time

from django.core.cache import cache
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse

from classification.utils.cache import get_cache_key
from classification.utils.validate import ValidationError, validate_request

from .apps import ClassificationConfig
from .services.fuzzy import FuzzyService
from .services.language import LanguageService
from .services.ner import NERService
from .serializers import (
    AnalyzeTextRequestSerializer,
    AnalyzeTextResponseSerializer,
    ErrorSerializer,
)

app_name = ClassificationConfig.name
logger = logging.getLogger(__name__)

language_service = LanguageService()
ner_service = NERService()
fuzzy_service = FuzzyService(threshold=85)

example_text = "Одним солнечным днём они решили сделать что-то необычноые. Вместо того, чтобы оставаться дома, Владислав и Екатерина решили устроить путешествие. Они выбрали современный город. Им оказался Москва."


@extend_schema(
    request=AnalyzeTextRequestSerializer,
    examples=[
        OpenApiExample(
            "Пример текста", value={"text": example_text}, request_only=True
        )
    ],
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=AnalyzeTextResponseSerializer,
            description="Успешный запрос",
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=ErrorSerializer, description="Некорректный запрос"
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: OpenApiResponse(
            response=ErrorSerializer, description="Ошибка валидации данных "
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
            response=ErrorSerializer, description="Ошибка сервера"
        ),
    },
    tags=["Text Analysis"],
    summary="Analyze input text for named entities",
)
@api_view(["POST"])
@renderer_classes([JSONRenderer])
def analyze_text(request: Request):
    method_name = "analyze_text"
    logger.info(f"[{app_name}] -> {method_name} start:")
    start_time = time.time()
    response_status = status.HTTP_200_OK
    response_data = {}
    response: Response
    try:
        text = validate_request(request)
        cache_key = get_cache_key(text)

        if cached := cache.get(cache_key):
            response_data.update(cached)
            logger.info(f"[{app_name}] Cache hit for key: {cache_key}")
            response = Response(response_data, status=response_status)
            return response

        language = language_service.detect(text)
        entities = ner_service.extract(text, language)
        response_data.update(
            {
                "language": language,
                "entities": ner_service.get_ner_result(entities),
                "fuzzy_matches": fuzzy_service.get_fuzzy_result(
                    language, entities
                ),
            }
        )
        cache.set(cache_key, response_data, timeout=3600)
        response = Response(response_data, status=response_status)

    except ValidationError as e:
        logger.warning(f"{method_name} - Validation error: {str(e)}")
        response_status = status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data["error"] = str(e)
        response = Response(response_data, status=response_status)

    except ValueError as e:
        logger.warning(f"{method_name} - Client error: {str(e)}")
        response_status = status.HTTP_400_BAD_REQUEST
        response_data["error"] = str(e)
        response = Response(response_data, status=response_status)

    except Exception:
        logger.exception(f"{method_name} - Server error")
        response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_data["error"] = "Internal server error"
        response = Response(response_data, status=response_status)

    finally:
        finish_time = time.time() - start_time
        logger.info(
            f"[{app_name}] {method_name} completed in {finish_time:.2f}s. "
            f"Status: {response_status}. Result: {response_data.get('language')}"
        )
    return response
