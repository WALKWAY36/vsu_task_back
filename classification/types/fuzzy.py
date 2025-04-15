from enum import Enum
from typing import List
from pydantic import BaseModel, Field, RootModel


class MatchedEntity(BaseModel):
    first_name: str
    second_name: str
    score: str


class MatchedEntities(RootModel[List[MatchedEntity]]):
    pass


class DtoFuzzy(BaseModel):
    matched: str
    suggestion: str
    score: float


class DtosFuzzy(RootModel[List[DtoFuzzy]]):
    pass


class Reference(RootModel[List[str]]):
    pass


class References(BaseModel):
    persons: Reference = Field(default_factory=Reference)
    locations: Reference = Field(default_factory=Reference)


class FuzzyResultDTO(BaseModel):
    persons: DtosFuzzy = Field(default_factory=DtosFuzzy)
    locations: DtosFuzzy = Field(default_factory=DtosFuzzy)


class EntityGroup(str, Enum):
    PERSONS = "persons"
    LOCATIONS = "locations"

    def __str__(self) -> str:
        return self.value


class DtoFuzzyField(str, Enum):
    MATCHED = "matched"
    SUGGESTION = "suggestion"
    SCORE = "score"

    def __str__(self):
        return self.value
