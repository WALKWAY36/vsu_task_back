import logging
import os

from vsu_task_core.main.fuzzy import FuzzyRapidMatcher
from vsu_task_core.main.lang import MainTextClassifierByLang
from vsu_task_core.main.ner import SpacyNerExtractorEn, SpacyNerExtractorRu

logger = logging.getLogger(__name__)


class GlobalResources:
    _main_classifier = None
    _spacy_ru = None
    _spacy_en = None
    _fuzzy_matcher = None

    @classmethod
    def get_main_classifier(cls):
        if cls._main_classifier is None:
            logger.info("Initializing MainTextClassifierByLang...")
            cls._main_classifier = MainTextClassifierByLang()
            cls._main_classifier.prepare()
            logger.info("MainTextClassifierByLang initialized.")
        return cls._main_classifier

    @classmethod
    def get_spacy_ru(cls):
        if cls._spacy_ru is None:
            logger.info("Initializing SpacyNerExtractorRu...")
            cls._spacy_ru = SpacyNerExtractorRu()
            logger.info("SpacyNerExtractorRu initialized.")
        return cls._spacy_ru

    @classmethod
    def get_spacy_en(cls):
        if cls._spacy_en is None:
            logger.info("Initializing SpacyNerExtractorEn...")
            cls._spacy_en = SpacyNerExtractorEn()
            logger.info("SpacyNerExtractorEn initialized.")
        return cls._spacy_en

    @classmethod
    def get_fuzzy_matcher(cls):
        if cls._fuzzy_matcher is None:
            try:
                threshold_str = os.getenv("THRESHOLD_FUZZY", "90")
                threshold = float(threshold_str)
            except ValueError:
                threshold = 80 
            logger.info(f"Initializing FuzzyRapidMatcher with threshold={threshold}...")
            cls._fuzzy_matcher = FuzzyRapidMatcher(threshold=threshold)
            logger.info("FuzzyRapidMatcher initialized.")
        return cls._fuzzy_matcher

    @classmethod
    def preload_all(cls):
        logger.info("Preloading all global resources...")
        cls.get_main_classifier()
        cls.get_spacy_ru()
        cls.get_spacy_en()
        cls.get_fuzzy_matcher()
        logger.info("All global resources are preloaded.")
