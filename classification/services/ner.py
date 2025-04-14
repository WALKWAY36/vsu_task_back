from vsu_task_core.main.ner import SpacyNerExtractorEn, SpacyNerExtractorRu

from classification.types.ner import (
    ExtractedGroupEntities,
    ExtractedGroupEntitiesDTO,
    NamedEntities,
)


class NERService:
    @staticmethod
    def extract(text: str, language: str) -> ExtractedGroupEntities:
        if language == "ru":
            entities = SpacyNerExtractorRu().apply(text)
        elif language == "en":
            entities = SpacyNerExtractorEn().apply(text)
        else:
            return {"persons": [], "locations": []}

        return {
            "persons": entities.get("persons", []),
            "locations": entities.get("locations", []),
        }

    @staticmethod
    def get_ner_result(
        group_entities: ExtractedGroupEntities,
    ) -> ExtractedGroupEntitiesDTO:
        return {
            "persons": [entity.value for entity in group_entities["persons"]],
            "locations": [
                entity.value for entity in group_entities["locations"]
            ],
        }
