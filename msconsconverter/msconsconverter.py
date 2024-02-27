import os
from datetime import datetime

from msconsconverter.constants import CSV_DELIMITER, CSV_FILE_PREFIX, VERIFY
from msconsconverter.exceptions import EntryHeaderCSVConflict
from msconsconverter.helpers import gen_file_name
from msconsconverter.logger import CustomLogger


class MSCONSConverter:

    def __init__(self, target_dir=None, logger=None):
        self.logger = logger
        self.logger.debug('class "MSCONSConverter" was created')

        if not os.path.exists(target_dir):
            raise Exception(f"No output folder was found: {target_dir}")

        self.target_dir = target_dir

    def to_csv(self, data: dict, csv_header_values: list):
        """Converting from Python dict to predefined CSV format.

        Args:
            data (dict): data to be saved
            csv_header_values (list): header of CSV file

        Raises:
            RuntimeError: _description_
        """

        new_file_name = "{0}-{1}".format(CSV_FILE_PREFIX, gen_file_name(extension=".csv"))
        new_file_name_path = os.path.join(self.target_dir, new_file_name)

        csv = open(new_file_name_path, "w")
        csv.write(CSV_DELIMITER.join(csv_header_values) + "\n")

        for loc_mscons in data["loc_mscons"]:
            loc_mscons_plz = loc_mscons[8:13]
            loc_mscons_eegkey = loc_mscons[-20:]
            # parsing results evaluation
            loc_to_expect = loc_mscons[:8] + loc_mscons_plz + loc_mscons_eegkey
            if loc_mscons != loc_to_expect:
                self.logger.warning(
                    f"unexpected customized LOC format, excepted: {loc_mscons} ; found: {loc_to_expect}"
                )

            tmp_line = ""
            for item in data["qty"][loc_mscons]:

                tmp_line = '"{0}"{1}'.format(loc_mscons, CSV_DELIMITER)
                tmp_line += '"{0}"{1}'.format(loc_mscons_plz, CSV_DELIMITER)
                tmp_line += '"{0}"{1}'.format(loc_mscons_eegkey, CSV_DELIMITER)
                tmp_line += "{0}{1}".format(self.__parse_date_to_csv(item[1]), CSV_DELIMITER)
                tmp_line += "{0}{1}".format(self.__parse_date_to_csv(item[2]), CSV_DELIMITER)
                tmp_line += '"{0}"'.format(item[0])
                tmp_line += "\n"

                if VERIFY:
                    self.__verify_single_entry(tmp_line, csv_header_values)

                csv.write(tmp_line)

        csv.close()

        self.logger.debug(f'parsing results saved into file": {new_file_name_path}')

    def parse_mscons(self, file_name: str):
        """Parses MSCONS format"""

        mscons_dict = {}
        mscons_data = self.__read_file_content(file_name)

        self.logger.debug("identified special characters of MSCONS")

        COMPONENT_SEPARATOR = ":"
        ELEMENT_SEPARATOR = "+"
        DECIMAL_MARK = "."
        RELEASE_SYMBOL = "?"
        SEGMENTAION_SYMBOL = "'"

        if mscons_data.startswith("UNA"):
            offset = 2
            COMPONENT_SEPARATOR = mscons_data[offset + 1]
            ELEMENT_SEPARATOR = mscons_data[offset + 2]
            DECIMAL_MARK = mscons_data[offset + 3]
            RELEASE_SYMBOL = mscons_data[offset + 4]
            SEGMENTAION_SYMBOL = mscons_data[offset + 6]
        else:
            self.logger.debug("no special characters were found, default will be used")

        self.MSCONS_DECIMAL_MARK = DECIMAL_MARK

        self.logger.debug(
            f"""\nspecial symbols that will be used
            COMPONENT_SEPARATOR {COMPONENT_SEPARATOR}
            ELEMENT_SEPARATOR {ELEMENT_SEPARATOR}
            DECIMAL_MARK {self.MSCONS_DECIMAL_MARK}
            RELEASE_SYMBOL {RELEASE_SYMBOL}
            SEGMENTAION_SYMBOL {SEGMENTAION_SYMBOL}"""
        )

        mscons_tokens = mscons_data.split(SEGMENTAION_SYMBOL)
        cur_qty = 0.0
        start_saving = False
        save_cur_qty_value = False

        current_loc = None

        for index, token in enumerate(mscons_tokens):
            if token.startswith("LOC"):
                subtoken = token.split(ELEMENT_SEPARATOR)
                self.logger.debug(subtoken)
                if subtoken[1] == "172":
                    if "loc_mscons" not in mscons_dict:
                        mscons_dict["loc_mscons"] = list()
                    mscons_dict["loc_mscons"].append(subtoken[2])
                    current_loc = subtoken[2]

                self.logger.debug(f"Found LOC token {subtoken} at line: {index}")

            if token.startswith("PIA"):
                self.logger.warning("PIA was found, but ignored")

            if token.startswith("QTY"):
                start_saving = True
                subcomponents = token.split(COMPONENT_SEPARATOR)
                if subcomponents[0] == "QTY+220":
                    cur_qty = subcomponents[1]
                else:
                    self.logger.warning("strange numeric code fro QTY was found, value will be save as 0.0")
                    cur_qty = 0.0

            if token.startswith("DTM"):
                subcomponents = token.split(COMPONENT_SEPARATOR)
                subcomponents[1] = subcomponents[1].replace(RELEASE_SYMBOL, "")

                if subcomponents[0] == "DTM+163":
                    cur_date_period_start = subcomponents[1]

                if subcomponents[0] == "DTM+164":
                    cur_date_period_end = subcomponents[1]
                    save_cur_qty_value = True

                if subcomponents[2] != "303":
                    self.logger.warning("different date format")

            if save_cur_qty_value and start_saving:
                if "qty" not in mscons_dict:
                    mscons_dict["qty"] = {}
                if current_loc not in mscons_dict["qty"]:
                    mscons_dict["qty"][current_loc] = list()
                mscons_dict["qty"][current_loc].append((cur_qty, cur_date_period_start, cur_date_period_end))

        return mscons_dict

    def convert_to_csv(self, file_name, csv_header_values):
        """
        (obj, str) -> None

        Converting MSCONS data to CSV.
        """

        self.logger.debug(f"parsing MSCONS file: {file_name}")
        mscons = self.parse_mscons(file_name)

        self.logger.debug("saving data to CSV")

        self.to_csv(mscons, csv_header_values)

    def __parse_date_to_csv(self, input_date: str, format_date: str = "303") -> str:
        """Parsing data only for '303' MSCONS format

        Args:
            input_date (str): date to per parsed
            format_date (str, optional): format of the date. Defaults to "303".

        Returns:
            str: _description_
        """

        if format_date == "303":
            year = input_date[0:4]
            month = input_date[4:6]
            day = input_date[6:8]
            hour = input_date[8:10]
            minute = input_date[10:12]
            utc = input_date[12:]
            return '"{1}"{0}"{2}"{0}"{3}"{0}"{4}"{0}"{5}"{0}"{6}"{0}"{7}"'.format(
                CSV_DELIMITER, input_date, year, month, day, hour, minute, utc
            )
        else:
            self.logger.error("only parses date that is in 303 format specification")

        return None

    def __verify_single_entry(self, entry_line: str, csv_header_values: list) -> None:
        """Verifies consistency of each single CSV line on creation

        Args:
            entry_line (str): line to be saved into CSV
            csv_header_values (list): list of headers to be used for CSV

        Raises:
            EntryHeaderCSVConflict: raised if non-consistent
        """

        header_size = len(csv_header_values)
        tmp_len = len(entry_line.split(CSV_DELIMITER))
        validity_shift = 0

        if CSV_DELIMITER == self.MSCONS_DECIMAL_MARK:
            validity_shift = -1
        if header_size == tmp_len or header_size == (tmp_len + validity_shift):
            pass
        else:
            raise EntryHeaderCSVConflict(
                f"check CSV merger header (elements = {header_size}) does not equals to constructed row (elements = {tmp_len})"
            )

    def __read_file_content(self, file_name: str) -> str:
        """Reads file content line by line

        Args:
            file_name (str): file name

        Returns:
            str: content of the file
        """
        mscons_data = ""
        read_file = open(file_name, "r")
        for line in read_file.readline():
            mscons_data += line
        read_file.close()

        return mscons_data
