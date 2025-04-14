import hashlib


def get_cache_key(text: str) -> str:
    """Генерация ключа кеша на основе текста"""
    text_hash = hashlib.md5(text.encode("utf-8")).hexdigest()
    return f"analyze_text:{text_hash}"
