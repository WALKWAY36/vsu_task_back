from vsu_task_core.common.lang import Lang
from vsu_task_core.main.lang import MainTextClassifierByLang


class LanguageService:
    def __init__(self):
        self.classifier = MainTextClassifierByLang()
        self.classifier.prepare()

    def detect(self, text: str) -> str:
        if not text.strip():
            return Lang.UNDEFINED.value

        result = self.classifier.apply(text)
        return result.value
