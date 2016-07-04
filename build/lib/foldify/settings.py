import logging

#  Files allowed to be copied when copying tree, or making tree json
ALLOWED_FILES = ['.txt','']  # blank string is for folders

#  Files that should be ignoring when determing if a folder is "empty"
#  IGNORE = ['(desktop.ini)', '(.*\.txt)']
IGNORE = ['(desktop.ini)', '(.*\.git)']
IGNORE_PATTERN = r'|'.join(IGNORE)

#  Default label added to empty folders
EMPTY_LABEL = '_EMPTY'

#  Logger Setup
default_level = logging.INFO
formatter = "[%(levelname)s] %(message)s [%(filename)s](%(lineno)d)"
logging.basicConfig(level=default_level, format=formatter)
logger = logging.getLogger('Foldify')


def enable_debug():
    logger.setLevel(logging.DEBUG)


def disable_logger():
    logger.setLevel(logging.ERROR)
