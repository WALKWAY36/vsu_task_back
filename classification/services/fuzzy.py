from typing import List, Dict, Any

from vsu_task_core.common.fuzzy import FuzzyResult
from vsu_task_core.common.ner import NamedEntity, NERType
from vsu_task_core.main.fuzzy import FuzzyRapidMatcher

from classification.types.fuzzy import DtoFuzzy


class FuzzyService:
    def __init__(self, threshold: float = 90):
        self.matcher = FuzzyRapidMatcher(threshold=threshold)

    def match_entities(self, entities: list[NamedEntity], reference: List[str], entity_type: str) -> List[FuzzyResult]:
        named_entity = [
            NamedEntity(
                NERType.PERSON if entity_type == "person" else NERType.LOCATION,
                value
            )
            for value in reference
        ]
        return  self.matcher.match(entities, named_entity)

    @staticmethod
    def dto_fuzzy(entity: FuzzyResult) -> DtoFuzzy:
        return DtoFuzzy(
            matched=entity.first_name,
            suggestion=entity.second_name,
            score=entity.score,
        )

    def get_fuzzy_result(self, fuzzy_result: List[FuzzyResult]):
        return [self.dto_fuzzy(res).model_dump() for res in fuzzy_result]

