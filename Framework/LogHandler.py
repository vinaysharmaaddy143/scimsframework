import logging
import os
import sys
from datetime import datetime
"""This class is for handling logging"""


date_stamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
# creating file path
file_path = os.path.join(os.getcwd(), f"ScimsFramework_{date_stamp}.log")

# setting configuration for Logger
logging.basicConfig(format='%(asctime)s\t%(filename)s\t%(levelname)s\t%(message)s', datefmt='%m/%d/%Y %H:%M:%S',
                    filemode="w", filename=file_path,
                    level=logging.DEBUG, force=True)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

output_file_handler = logging.FileHandler(file_path)
stdout_handler = logging.StreamHandler(sys.stdout)

logger.addHandler(output_file_handler)
logger.addHandler(stdout_handler)


def print_debug_log(text):
    """
    Print DEBUG Logs
    :param text: text which need to be print
    :return: None
    """
    logging.debug(text)


def print_error_log(text):
    """
    Print ERROR Logs
    :param text: text which need to be print
    :return: None
    """
    logging.error(text)


def print_warning_log(text):
    """
    Print WARNING Logs
    :param text: text which need to be print
    :return: None
    """
    logging.warning(text)


def print_info_log(text):
    """
    Print INFO Logs
    :param text: text which need to be print
    :return: None
    """
    logging.info(text)
