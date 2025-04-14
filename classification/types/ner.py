from typing import List
from pydantic import BaseModel, Field
from vsu_task_core.common.ner import NamedEntity

class NamedEntities(BaseModel):
    List[NamedEntity]

class ExtractedGroupEntities(BaseModel):
    persons: NamedEntities = Field(default_factory=list)
    locations: NamedEntities = Field(default_factory=list)

class ExtractedGroupEntitiesDTO(BaseModel):
    persons: List[str]
    locations: List[str]