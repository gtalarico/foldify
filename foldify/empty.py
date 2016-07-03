import os
import sys
import shutil
import logging
import re

from pathlib import *

LEVEL = logging.INFO
# LEVEL = logging.DEBUG

logging.basicConfig(level=LEVEL)
logger = logging.getLogger('')

# TO DO:
# Run with Arg or local
# Function Remove Labels

ROOT_DIR = 'tests/wdrive2'
# ROOT_DIR = os.getcwd()
EMPTY_LABEL = '_EMPTY'

# IGNORE = ['(desktop.ini)']
IGNORE = ['(desktop.ini)', '(.*\.txt)']
IGNORE_PATTERN = r'|'.join(IGNORE)

empty_folders = []
used_folders = []
used_folders_ancestors = []

transactions = []


def label_empty(path):
    if not path.name.endswith(EMPTY_LABEL):
        new_path = Path(path.parent, path.name + EMPTY_LABEL)
        transactions.append((path, new_path))


def unlabel_used(path):
    if path.name.endswith(EMPTY_LABEL):
        new_path = Path(path.parent, path.name.split(EMPTY_LABEL)[0])
        # path.rename(new_name)
        transactions.append((path, new_path))


def listDirs(dir):
    for root, subFolders, files in os.walk(dir, topdown=False):
        logger.debug('<ROOT:{}|SUBS:{}|FILES:{}>'.format(root, subFolders,
                                                         files))

        path = Path(root)
        matches_all_filters = all([re.match(IGNORE_PATTERN, f) for f in files])
        # logger.debug('MATCH FILTER: %s', match_ignore)
        logger.debug('<FILES:{}>'.format(files))
        if files and not matches_all_filters:
            used_folders.append(path)
            logger.debug('%s is USED', root)
        else:
            empty_folders.append(path)
            logger.debug('%s is EMPTY', root)


def apply_transactions():
    if not transactions:
        logger.info('NO TRANSACTIONS')
        return
    print('='*30)
    for t in transactions:
        print('[{}] > [{}]'.format(t[0].name, t[1].name))
    if input('EXECUTE ? [y]') == 'y':
        for src, dst in transactions:
            try:
                src.rename(dst)
            except:
                logger.error(sys.exc_info()[0].__name__)
                logger.error('Could not rename: [{}]>[{}]'.format(src,dst))

listDirs(ROOT_DIR)
for used in used_folders:
    for dependend in used.parents:
        used_folders_ancestors.append(dependend)

[label_empty(x) for x in empty_folders if x not in used_folders_ancestors]
[unlabel_used(x) for x in used_folders + used_folders_ancestors]

# [unlabel_used(x) for x in used_folders + used_folders_ancestors + empty_folders]

create_update_labels_transactions()
# create_remove_all_labels_transactions()
apply_transactions()
