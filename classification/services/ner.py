from vsu_task_core.common.lang import Lang
from vsu_task_core.main.ner import SpacyNerExtractorEn, SpacyNerExtractorRu

from classification.core.global_resources import GlobalResources
from classification.types.fuzzy import EntityGroup
from classification.types.ner import (ExtractedGroupEntities,
                                      ExtractedGroupEntitiesDTO, NamedEntities)


class NERService:
    def __init__(self):
        self.spacy_ru = GlobalResources.get_spacy_ru()
        self.spacy_en = GlobalResources.get_spacy_en()


    def extract(self, text: str, language: str) -> ExtractedGroupEntities:
        if language == Lang.RU.value:
            entities = self.spacy_ru.apply(text)
        elif language == Lang.EN.value:
            entities = self.spacy_en.apply(text)
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
