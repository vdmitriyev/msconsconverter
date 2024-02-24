import random
import string
from time import gmtime, strftime

RAND_RANGE = 7


def gen_file_name(extension: str = ".html", prefix: str = None) -> str:
    """Generate a file name

    Args:
        extension (str, optional): extension to be used. Defaults to ".html".
        prefix (str, optional): prefix of the file name. Defaults to None.

    Returns:
        str: new file name
    """

    rand_path_range = "".join(random.choice(string.ascii_lowercase + string.digits) for x in range(RAND_RANGE))
    if prefix is None:
        new_file_name = strftime("%Y-%m-%d", gmtime()) + "-" + rand_path_range + extension
    else:
        new_file_name = prefix + "-" + rand_path_range + extension

    return new_file_name
