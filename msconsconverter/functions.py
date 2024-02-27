import os

from msconsconverter.logger import CustomLogger
from msconsconverter.msconsconverter import MSCONSConverter


def convert_single(filename: str, target_dir: str, logger: CustomLogger) -> None:
    """Converts a single file"""

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    obj = MSCONSConverter(target_dir=target_dir, logger=logger)

    logger.info(f"start processing file: {filename}")

    obj.convert_to_csv(
        file_name=filename,
        csv_header_values=[
            "LOC_MSCONS",
            "LOC_PLZ",
            "LOC_EEGKEY",
            "DATE_PERIOD_START",
            "YEAR_PS",
            "MONTH_PS",
            "DAY_PS",
            "HOUR_PS",
            "MINUTE_PS",
            "UTC_PS",
            "DATE_PERIOD_END",
            "YEAR_PE",
            "MONTH_PE",
            "DAY_PE",
            "HOUR_PE",
            "MINUTE_PE",
            "UTC_PE",
            "VALUE",
        ],
    )

    logger.info(f"finish processing file: {filename}\n")


def convert_batch(directory: str, target_dir: str, logger: CustomLogger):
    """Converts all files within the directory"""

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    obj = MSCONSConverter(target_dir=target_dir, logger=logger)

    for file_name in os.listdir(directory):
        full_path = os.path.join(directory, file_name)

        if os.path.isfile(full_path):
            logger.info(f"start processing file: {full_path}")
            obj.convert_to_csv(
                file_name=full_path,
                csv_header_values=[
                    "LOC_MSCONS",
                    "LOC_PLZ",
                    "LOC_EEGKEY",
                    "DATE_PERIOD_START",
                    "YEAR_PS",
                    "MONTH_PS",
                    "DAY_PS",
                    "HOUR_PS",
                    "MINUTE_PS",
                    "UTC_PS",
                    "DATE_PERIOD_END",
                    "YEAR_PE",
                    "MONTH_PE",
                    "DAY_PE",
                    "HOUR_PE",
                    "MINUTE_PE",
                    "UTC_PE",
                    "VALUE",
                ],
            )
            logger.info(f"finish processing file: {full_path}\n")
