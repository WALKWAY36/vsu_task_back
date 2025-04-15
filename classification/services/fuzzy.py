from vsu_task_core.common.ner import NamedEntity, NERType
from vsu_task_core.common.lang import Lang
from vsu_task_core.main.fuzzy import FuzzyRapidMatcher

from classification.constants import LOCATION_NAMES_EN, LOCATION_NAMES_RU, PERSON_NAMES_EN, PERSON_NAMES_RU
from classification.types.fuzzy import (
    DtoFuzzy,
    DtoFuzzyField,
    DtosFuzzy,
    EntityGroup,
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

    def get_fuzzy_result(self, language: str, entities: ExtractedGroupEntities) -> FuzzyResultDTO:
        references = self.get_references(language)
        matched_persons = self.match_entities(
            entities[EntityGroup.PERSONS], references[EntityGroup.PERSONS], entity_type=NERType.PERSON.value
        )
        matched_locations = self.match_entities(
            entities[EntityGroup.LOCATIONS], references[EntityGroup.LOCATIONS], entity_type=NERType.LOCATION.value
        )
        return {
            EntityGroup.PERSONS: self.dtos_fuzzy(matched_persons),
            EntityGroup.LOCATIONS: self.dtos_fuzzy(matched_locations),
        }

    def match_entities(self, entities: NamedEntities, reference: Reference, entity_type: str) -> MatchedEntities:
        named_entity = [
            NamedEntity((NERType.PERSON if entity_type == NERType.PERSON.value else NERType.LOCATION), value)
            for value in reference
        ]
        return self.matcher.match(entities, named_entity)

    @staticmethod
    def get_references(language: str) -> References:
        return {
            EntityGroup.PERSONS: (PERSON_NAMES_RU if language == Lang.RU.value else PERSON_NAMES_EN),
            EntityGroup.LOCATIONS: (LOCATION_NAMES_RU if language == Lang.RU.value else LOCATION_NAMES_EN),
        }

    @staticmethod
    def dto_fuzzy(matched_entity: MatchedEntity) -> DtoFuzzy:
        return {
            DtoFuzzyField.MATCHED: matched_entity.first_name,
            DtoFuzzyField.SUGGESTION: matched_entity.second_name,
            DtoFuzzyField.SCORE: matched_entity.score,
        }

    def dtos_fuzzy(self, matched_entities: MatchedEntities) -> DtosFuzzy:
        return [self.dto_fuzzy(res) for res in matched_entities]
