from enum import Enum


class AnalyzeFieldRequest(str, Enum):
    TEXT = "text"

    def __str__(self) -> str:
        return self.value


class AnalyzeFieldResponse(str, Enum):
    LANGUAGE = "language"
    ENTITY = "entities"
    FUZZY = "fuzzy_matched"
    ERROR = "error"

    def __str__(self) -> str:
        return self.value
