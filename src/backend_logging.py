import logging


def setup_logging():
    from src.config.settings import settings

    log_config = settings.logs
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(level=log_config.level, format=log_format)

    logger = logging.getLogger("backend")

    if log_config.file_enabled:
        if log_config.filename == "":
            logger.warning("Logging filename not found but enabled file logging!!!")
        else:
            file_handler = logging.FileHandler(log_config.filename, encoding="utf-8")
            file_handler.setFormatter(logging.Formatter(log_format))
            logging.getLogger().addHandler(file_handler)


logger = logging.getLogger("backend")

setup_logging()
