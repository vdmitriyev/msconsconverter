# -*- coding: utf-8 -*-

import codecs
import os
import random
import shutil
import string
from time import gmtime, strftime

RAND_RANGE = 7
TEMP_DIRECTORY = "__temp__"


class DirectoryHelper:

    def __init__(self, target_dir=None):

        if target_dir:
            self.current_dir = target_dir + os.sep
        else:
            self.current_dir = os.path.dirname(os.path.abspath(__file__)) + os.sep

        self.temp_dir = os.path.join(self.current_dir, TEMP_DIRECTORY)

    def clear_directory(self, directory):
        """
        (obj, str) -> None

        Clears given 'directory'.
        """

        for root, dirs, files in os.walk(directory):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    def create_directory_ondemand(self, directory):
        """
        (obj, str) -> None

        Creating directory on demand.
        """

        if not os.path.exists(directory):
            os.makedirs(directory)

    def prepare_working_directory(self):
        """
        (obj) -> None

        Prepearing current directory for working:
            -   checking if temp folder is existing and creating it;
            -   clearing temp directory;
            -
        """

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

        self.clear_directory(self.temp_dir)

    def move_from_temp_directory(self):
        """
        (obj) -> None

        Current method will implement versioning of publication.
        """

    def upper_directory(self):
        """
        (obj) -> None

        Identify upper directory.
        """

        cur_dir = os.path.dirname(os.path.abspath(__file__))
        up_dir = cur_dir[: cur_dir.rfind("\\")] + "\\"
        return up_dir

    def save_file(self, file_name, text, encoding="utf-8"):
        """
        (obj, str, str, str) -> None

        Save to 'file_name' given 'text'.
        """
        _file = codecs.open(file_name, "w", encoding)
        _file.write(text)
        _file.close()

    def save_img_file(
        self,
        file_name,
        img,
    ):
        """
        (obj,str,str) -> None

        Save to 'file_name' given 'img'.
        """
        _file = codecs.open(file_name, "wb")
        _file.write(img)
        _file.close()

        # with open(file_name, 'w') as content_file:
        #   content = content_file.write(text)

    def read_file(self, file_name):
        """
        (obj, str) -> (str)

        Reads text from 'file_name' and return it
        """
        with open(file_name, "r") as file_input:
            file_content = file_input.read()
        return file_content


def gen_file_name(extention=".html", name=None):
    """
    (obj, str) -> (str)

    Generates file name
    """

    rand_path_range = "".join(random.choice(string.ascii_lowercase + string.digits) for x in range(RAND_RANGE))
    if name is None:
        new_file_name = strftime("%Y-%m-%d", gmtime()) + "-" + rand_path_range + extention
    else:
        new_file_name = name + "-" + rand_path_range + extention

    return new_file_name
