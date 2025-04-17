import logging

from classification.core.global_resources import GlobalResources

logger = logging.getLogger(__name__)


class Initializer:
    def execute(self):
        module_name = "webapp.settings"
        try:
            GlobalResources.preload_all()
        except Exception as exc:
            logger.error(f"[{self.__class__.__name__}] -> execute error, exception: {exc}")
        logger.info(f"[{self.__class__.__name__}] -> execute with {module_name=}")
