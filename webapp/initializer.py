import logging


logger = logging.getLogger(__name__)


class Initializer:
    def execute(self):
        module_name = "webapp.settings"
        try:
            from vsu_task_core.main.lang import MainTextClassifierByLang

            MainTextClassifierByLang().prepare()
        except Exception as exc:
            logger.error(
                f"[{self.__class__.__name__}] -> execute error, exception: {exc}"
            )
        logger.info(
            f"[{self.__class__.__name__}] -> execute with {module_name=}"
        )
