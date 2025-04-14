import json

from rest_framework.request import Request


class ValidationError(ValueError):
    """Ошибка валидации, которая вызывает 422 Unprocessable Entity"""


def validate_request(request: Request) -> str:
    """Валидация входящего запроса и извлечение текста"""
    if not request.body:
        raise ValueError("Request body is empty")

    try:
        body = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON format") from exc

    text_value = body.get("text", "")
    if not isinstance(text_value, str):
        raise ValidationError("Text must be a string")

    text = text_value.strip()

    if not text:
        raise ValidationError("Text parameter is empty")
    if len(text) > 10000:
        raise ValidationError("Text is too long (max 10,000 characters)")

    return text
