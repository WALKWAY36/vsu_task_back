from typing import List

from vsu_task_core.common.ner import NamedEntity
from vsu_task_core.main.ner import SpacyNerExtractorRu, SpacyNerExtractorEn

from classification.types.ner import ExtractedEntitiesDTO, NamedEntityDTO


class NERService:
    def extract(text: str, language: str) -> dict[str, list[NamedEntity]]:
        if language == "ru":
            entities = SpacyNerExtractorRu().apply(text)
        elif language == "en":
            entities = SpacyNerExtractorEn().apply(text)
        else:
            return {"persons": [], "locations": []}

        return {
            "persons": entities.get("persons", []),
            "locations": entities.get("locations", [])
        }

    def get_ner_result(entities: List[NamedEntity]) -> List[str]:
       return [entity.value for entity in entities]