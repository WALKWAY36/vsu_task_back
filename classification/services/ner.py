from vsu_task_core.main.ner import SpacyNerExtractorEn, SpacyNerExtractorRu
from vsu_task_core.common.lang import Lang

from classification.types.fuzzy import EntityGroup
from classification.types.ner import ExtractedGroupEntities, ExtractedGroupEntitiesDTO, NamedEntities


class NERService:
    @staticmethod
    def extract(text: str, language: str) -> ExtractedGroupEntities:
        if language == Lang.RU.value:
            entities = SpacyNerExtractorRu().apply(text)
        elif language == Lang.EN.value:
            entities = SpacyNerExtractorEn().apply(text)
        else:
            return {EntityGroup.PERSONS: [], EntityGroup.LOCATIONS: []}

        return {
            EntityGroup.PERSONS: entities.get(EntityGroup.PERSONS, []),
            EntityGroup.LOCATIONS: entities.get(EntityGroup.LOCATIONS, []),
        }

    @staticmethod
    def get_ner_result(group_entities: ExtractedGroupEntities) -> ExtractedGroupEntitiesDTO:
        return {
            EntityGroup.PERSONS: [entity.value for entity in group_entities[EntityGroup.PERSONS]],
            EntityGroup.LOCATIONS: [entity.value for entity in group_entities[EntityGroup.LOCATIONS]],
        }
