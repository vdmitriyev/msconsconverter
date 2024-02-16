import logging
import os
import sys
import time
import uuid
from datetime import datetime


class CustomLogger:
    """A class that overtakes logs handling routine"""

    def get_logger(self, logger_name: str = None, logging_level: int = None) -> None:
        """Gets a configured logger for the class

        Args:
            logging_level (int): level of the logging
        """

        LOGS_FOLDER = ".logs"

        if logger_name is None:
            logger_name = "msconsconverter"

        if not os.path.exists(LOGS_FOLDER):
            os.mkdir(LOGS_FOLDER)

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(os.path.join(LOGS_FOLDER, f"{logger_name}.log"), mode="a"),
                logging.StreamHandler(),
            ],
        )
        logger = logging.getLogger(logger_name)

        if logging_level is None:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging_level)
        return logger
