#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Viktor Dmitriyev'
__license__ = 'MIT'
__version__ = '1.0.0'
__maintainer__ = '-'
__email__ = ''
__status__ = 'dev'
__date__ = '05.02.2016'
__description__ = 'MSCONS (EDIFACT) format converter (to CSV).'

import os
import sys
import time
import uuid
from docopt import docopt
from pprint import pprint
from datetime import datetime
from directory_helper import DirectoryHelper

# set 'True' for debugging (stdout will be more verbose)
DEBUG = False
VERIFY = True

# CONSTANTS
CSV_DELIMITER = ','
CSV_FILE_PREFIX = 'MSCONS'

class MSCONSConverter():

    def __init__(self, target_dir=None):

        if DEBUG: print ('[i] class "MSCONSConverter" created')

        self.helper = DirectoryHelper(target_dir=target_dir)
        self.helper.prepare_working_directory()
        self.temp_dir = self.helper.temp_dir

    def to_csv(self, data, csv_header_values):
        """
            (obj, str) -> list()

            Converting from Python dict to predefined CSV format.
        """

        new_file_name = '{0}{1}-{2}'.format(self.temp_dir,
                                            CSV_FILE_PREFIX,
                                            self.helper.gen_file_name(extention='.csv'))
        csv = open(new_file_name, "w")
        csv.write(CSV_DELIMITER.join(csv_header_values) + '\n')
        header_size = len(csv_header_values)

        loc_mscons = data['loc_mscons']
        loc_mscons_plz = loc_mscons[8:13]
        loc_mscons_eegkey = loc_mscons[-20:]

        # parsing results evaluation
        if (loc_mscons) != (loc_mscons[:8] + loc_mscons_plz + loc_mscons_eegkey):
            print ('[e] wrong parsing of LOC')

        def parse_date_to_csv(input_date, format_date='303'):
            """ Parsing data only for '303' MSCONS format """

            if format_date == '303':
                year = input_date[0:4]
                month = input_date[4:6]
                day = input_date[6:8]
                hour = input_date[8:10]
                minute = input_date[10:12]
                utc = input_date[12:]
                return '"{1}"{0}"{2}"{0}"{3}"{0}"{4}"{0}"{5}"{0}"{6}"{0}"{7}"'.format(CSV_DELIMITER, input_date, year, month, day, hour, minute, utc)
            else:
                print('[e] only parses date that is in 303 format specification')

            return None

        tmp_line = ''
        for item in data['qty']:
            tmp_line =   '"{0}"{1}'.format(loc_mscons, CSV_DELIMITER)
            tmp_line +=  '"{0}"{1}'.format(loc_mscons_plz, CSV_DELIMITER)
            tmp_line +=  '"{0}"{1}'.format(loc_mscons_eegkey, CSV_DELIMITER)
            tmp_line +=  '{0}{1}'.format(parse_date_to_csv(item[1]), CSV_DELIMITER)
            tmp_line +=  '{0}{1}'.format(parse_date_to_csv(item[2]), CSV_DELIMITER)
            tmp_line +=  '"{0}"'.format(item[0])
            tmp_line += '\n'

            if VERIFY:
                tmp_len = len(tmp_line.split(CSV_DELIMITER))
                validity_shift = 0
                if CSV_DELIMITER == self.MSCONS_DECIMAL_MARK:
                    validity_shift = -1
                if header_size == tmp_len or \
                   header_size == (tmp_len + validity_shift):
                   pass
                else:
                    print('[e] check CSV merger header (elements = {0}) does not equals to constructed row (elements = {1})'.format(header_size, tmp_len))

            csv.write(tmp_line)

        csv.close()

        if DEBUG: print('[i] parsing results saved into file "{0}"'.format(new_file_name))


    def parse_mscons(self, file_name):
        """ Parsing MSCONS format """

        mscons_data = ''
        mscons_dict = {}
        mscons_dict['qty'] = []

        read_file = open(file_name , "r")
        for line in read_file.readline():
            mscons_data += line
        read_file.close()

        if DEBUG: print ('[i] identified special characters of MSCONS')

        COMPONENT_SEPARATOR = ':'
        ELEMENT_SEPARATOR = '+'
        DECIMAL_MARK = '.'
        RELEASE_SYMBOL = '?'
        SEGMENTAION_SYMBOL = '\''

        if mscons_data.startswith('UNA'):
            offset = 2
            COMPONENT_SEPARATOR = mscons_data[offset + 1]
            ELEMENT_SEPARATOR = mscons_data[offset + 2]
            DECIMAL_MARK = mscons_data[offset + 3]
            RELEASE_SYMBOL = mscons_data[offset + 4]
            SEGMENTAION_SYMBOL = mscons_data[offset + 6]
        else:
            print ('[i] no special characters were found, default will be used')

        self.MSCONS_DECIMAL_MARK = DECIMAL_MARK

        if DEBUG:
            print ('[i] special symbols that will be used')
            print ('\tCOMPONENT_SEPARATOR {0}'.format(COMPONENT_SEPARATOR))
            print ('\tELEMENT_SEPARATOR {0}'.format(ELEMENT_SEPARATOR))
            print ('\tDECIMAL_MARK {0}'.format(DECIMAL_MARK))
            print ('\tRELEASE_SYMBOL {0}'.format(RELEASE_SYMBOL))
            print ('\tSEGMENTAION_SYMBOL {0}'.format(SEGMENTAION_SYMBOL))

        mscons_tokens = mscons_data.split(SEGMENTAION_SYMBOL)
        cur_qty = 0.0
        start_saving = False
        save_cur_qty_value = False

        # main pricing
        for token in mscons_tokens:

            if token.startswith('LOC'):
                subtoken = token.split(ELEMENT_SEPARATOR)
                if DEBUG: print (subtoken)
                if subtoken[1] == '172':
                    mscons_dict['loc_mscons'] = subtoken[2]

            if token.startswith('PIA'):
                if DEBUG: print ('[i] PIA was found, but ignored')

            if token.startswith('QTY'):
                start_saving = True
                subcomponents = token.split(COMPONENT_SEPARATOR)
                if subcomponents[0] == 'QTY+220':
                    cur_qty = subcomponents[1]
                else:
                    print ('[i] strange numeric code fro QTY was found, value will be save as 0.0')
                    cur_qty = 0.0

            if token.startswith('DTM'):
                subcomponents = token.split(COMPONENT_SEPARATOR)
                subcomponents[1] = subcomponents[1].replace(RELEASE_SYMBOL,'')

                if subcomponents[0] == 'DTM+163':
                    cur_date_period_start = subcomponents[1]

                if subcomponents[0] == 'DTM+164':
                    cur_date_period_end = subcomponents[1]
                    save_cur_qty_value = True

                if subcomponents[2] != '303':
                    print('[i] different date format')

            if save_cur_qty_value and start_saving:
                save_cur_values = False
                mscons_dict['qty'].append((cur_qty, cur_date_period_start, cur_date_period_end))

        return mscons_dict


    def convert_to_csv(self, file_name, csv_header_values):
        """
            (obj, str) -> None

            Converting MSCONS data to CSV.
        """

        if DEBUG: print ('[i] parsing MSCONS')
        mscons = self.parse_mscons(file_name)

        if DEBUG: print ('[i] saving data to CSV')
        self.to_csv(mscons, csv_header_values)

class Logger(object):

    def __init__(self):
        """ Initializing log file with random name"""

        self.terminal = sys.stdout
        suffix = '{0}-{1}'.format(datetime.fromtimestamp(time.time()).strftime('%Y%m%d-%H%M'), str(uuid.uuid1())[:2])
        self.log = open('logfile-{0}.log'.format(suffix), "a")
        if DEBUG: print('[i] saving debugging info into file "{0}"'.format('logfile-{0}.log'.format(suffix)))

    def write(self, message):
        """ Overriding writing method to write to file and stdout at once"""

        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        """flush method is needed for python 3 compatibility
           handles the flush command by doing nothing
           you might want to specify some extra behavior here
        """

        pass

def main(folder=None, files=None):
    """ Creating classes and running methods"""

    if not files:
        files = [
                 'MSCONS_TL_SAMPLE01.txt'
                ]

    if not folder:
        folder = '../data'

    obj = MSCONSConverter(target_dir=folder)

    for _file in files:
        if DEBUG: print ('[i] processing file {0}'.format(_file))
        obj.convert_to_csv(file_name = folder + '/' + _file,
                            csv_header_values = ['LOC_MSCONS',
                                          'LOC_PLZ',
                                          'LOC_EEGKEY',
                                          'DATE_PERIOD_START',
                                          'YEAR_PS',
                                          'MONTH_PS',
                                          'DAY_PS',
                                          'HOUR_PS',
                                          'MINUTE_PS',
                                          'UTC_PS',
                                          'DATE_PERIOD_END',
                                          'YEAR_PE',
                                          'MONTH_PE',
                                          'DAY_PE',
                                          'HOUR_PE',
                                          'MINUTE_PE',
                                          'UTC_PE',
                                          'VALUE'])

if __name__ == '__main__':


    #sample()
    __help__ = """

    MSCONS (EDIFACT) format converter (to CSV)

    Usage:
        msconsconverter.py <input_folder> <files> [--verbose]
                                                  [--sample]

        msconsconverter.py -h | --help
        The <input_folder> argument must be a path to folder with data.
        The <files> argument must be a file/files with data located in given folder (comma separated).

        Options:
          -h --help     Show this screen.
          --sample      Will ignore all given options and try to run sample.
          --verbose     If given, debug output is also writen to the stdout.
          """

    opts = docopt(__help__)

    input_folder = opts["<input_folder>"][1:-1]
    files = opts["<files>"][1:-1].split(',')
    print (files)

    # running sample
    if opts["--sample"]:
        DEBUG = True
        main()
        exit()

    # activating logger
    if opts["--verbose"]:
        DEBUG = True
        sys.stdout = Logger()

    main(folder=input_folder, files=files)



