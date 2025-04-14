from vsu_task_core.common.ner import NamedEntity, NERType
from vsu_task_core.main.fuzzy import FuzzyRapidMatcher

from classification.constants import (
    LOCATION_NAMES_EN,
    LOCATION_NAMES_RU,
    PERSON_NAMES_EN,
    PERSON_NAMES_RU,
)
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

    def get_fuzzy_result(
        self, language: str, entities: ExtractedGroupEntities
    ) -> FuzzyResultDTO:
        references = self.get_references(language)
        matched_persons = self.match_entities(
            entities["persons"], references["persons"], entity_type="person"
        )
        matched_locations = self.match_entities(
            entities["locations"],
            references["locations"],
            entity_type="location",
        )
        return {
            "persons": self.dtos_fuzzy(matched_persons),
            "locations": self.dtos_fuzzy(matched_locations),
        }

    def match_entities(
        self, entities: NamedEntities, reference: Reference, entity_type: str
    ) -> MatchedEntities:
        named_entity = [
            NamedEntity(
                NERType.PERSON if entity_type == "person" else NERType.LOCATION,
                value,
            )
            for value in reference
        ]
        return self.matcher.match(entities, named_entity)

    @staticmethod
    def get_references(language: str) -> References:
        return {
            "persons": PERSON_NAMES_RU if language == "ru" else PERSON_NAMES_EN,
            "locations": (
                LOCATION_NAMES_RU if language == "ru" else LOCATION_NAMES_EN
            ),
        }

    @staticmethod
    def dto_fuzzy(matched_entity: MatchedEntity) -> DtoFuzzy:
        return {
            "matched": matched_entity.first_name,
            "suggestion": matched_entity.second_name,
            "score": matched_entity.score,
        }

    def dtos_fuzzy(self, matched_entities: MatchedEntities) -> DtosFuzzy:
        return [self.dto_fuzzy(res) for res in matched_entities]
