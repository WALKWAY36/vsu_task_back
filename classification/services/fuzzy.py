from typing import List, Dict, Any

from vsu_task_core.common.fuzzy import FuzzyResult
from vsu_task_core.common.ner import NamedEntity, NERType
from vsu_task_core.main.fuzzy import FuzzyRapidMatcher

from classification.types.fuzzy import (
    DtoFuzzy,
    DtosFuzzy,
    FuzzyResultDTO,
    MatchedEntities,
    MatchedEntity,
    Reference,
    References,
)
from classification.types.ner import ExtractedGroupEntities, NamedEntities


class FuzzyService:
    def __init__(self, threshold: float = 90):
        self.matcher = FuzzyRapidMatcher(threshold=threshold)

    def match_entities(
        self, entities: NamedEntities, reference: Reference, entity_type: str
    ) -> MatchedEntities:
        named_entity = [
            NamedEntity(
                NERType.PERSON if entity_type == "person" else NERType.LOCATION,
                value
            )
            for value in reference
        ]
        return  self.matcher.match(entities, named_entity)

    @staticmethod
    def dto_fuzzy(matched_entity: MatchedEntity) -> DtoFuzzy:
        return {
            "matched": matched_entity.first_name,
            "suggestion": matched_entity.second_name,
            "score": matched_entity.score,
        }

    def dtos_fuzzy(self, matched_entities: MatchedEntities) -> DtosFuzzy:
        return [self.dto_fuzzy(res) for res in matched_entities]
