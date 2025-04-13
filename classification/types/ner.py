from pydantic import BaseModel
from typing import List


class NamedEntityDTO(BaseModel):
    value: str

class ExtractedEntitiesDTO(BaseModel):
    persons: List[NamedEntityDTO]
    locations: List[NamedEntityDTO]

class EntityResultDTO(BaseModel):
    persons: List[str]
    locations: List[str]