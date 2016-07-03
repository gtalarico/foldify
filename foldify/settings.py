import logging

ALLOWED_FILES = ['.txt',''] # blank is for folders

# IGNORE = ['(desktop.ini)', '(.*\.txt)']
IGNORE = ['(desktop.ini)', '(.*\.git)']
IGNORE_PATTERN = r'|'.join(IGNORE)

EMPTY_LABEL = '_EMPTY'

default_level = logging.INFO

formatter = "[%(levelname)s] %(message)s [%(filename)s](%(lineno)d)"
logging.basicConfig(level=default_level, format=formatter)
logger = logging.getLogger('Foldify')


def enable_debug():
    logger.setLevel(logging.DEBUG)
