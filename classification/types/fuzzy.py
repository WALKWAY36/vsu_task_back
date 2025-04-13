from typing import List
from pydantic import BaseModel

class MatchedEntity(BaseModel):
    first_name: str
    second_name: str
    score: str

class MatchedEntities(BaseModel):
    List[MatchedEntity]

class DtoFuzzy(BaseModel):
    matched: str
    suggestion: str
    score: float

class DtosFuzzy(BaseModel):
    List[DtoFuzzy]

class Reference(BaseModel):
    List[str]

class References(BaseModel):
    persons: Reference
    locations: Reference

class FuzzyResultDTO(BaseModel):
    persons: DtosFuzzy
    locations: DtosFuzzy