from typing import List
from pydantic import BaseModel, Field, RootModel
from vsu_task_core.common.ner import NamedEntity


class NamedEntities(RootModel[List[NamedEntity]]):
    pass


class ExtractedGroupEntities(BaseModel):
    persons: NamedEntities = Field(default_factory=list)
    locations: NamedEntities = Field(default_factory=list)


class ExtractedGroupEntitiesDTO(BaseModel):
    persons: List[str] = Field(default_factory=list)
    locations: List[str] = Field(default_factory=list)
