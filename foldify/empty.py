import os
import sys
import shutil
import logging
import re
import itertools

from pathlib import *

from settings import IGNORE_PATTERN, EMPTY_LABEL

LEVEL = logging.INFO
# LEVEL = logging.DEBUG
logging.basicConfig(level=LEVEL)
logger = logging.getLogger('')


def add_label_transaction(path):
    if not path.name.endswith(EMPTY_LABEL):
        new_path = Path(path.parent, path.name + EMPTY_LABEL)
        return (path, new_path)


def remove_label_transaction(path):
    if path.name.endswith(EMPTY_LABEL):
        new_path = Path(path.parent, path.name.split(EMPTY_LABEL)[0])
        return (path, new_path)


def apply_transactions(*transactions):
    transactions = [transaction for sublist in transactions
                    for transaction in sublist
                    if transaction is not None]

    print('='*30)
    if not transactions:
        logger.info('NO TRANSACTIONS')
        return

    for t in transactions:
        print('[{}] > [{}]'.format(t[0].name, t[1].name))
    print('{} Transactions.'.format(len(transactions)))
    if input('EXECUTE ? [y]') == 'y':
        for src, dst in transactions:
            try:
                src.rename(dst)
            except:
                logger.error(sys.exc_info()[0].__name__)
                logger.error('Could not rename: [{}]>[{}]'.format(src, dst))


''' Iterates through directory.
used_folders: folders that have files
empty_folders: folders that DO NOT have files
'''
empty_folders = []
used_folders = []
used_folders_ancestors = []

ROOT_DIR = os.getcwd()

for root, subFolders, files in os.walk(ROOT_DIR, topdown=False):
    logger.debug('<ROOT:{}|SUBS:{}|FILES:{}>'.format(root, subFolders,
                                                     files))

    path = Path(root)
    matches_all_filters = all([re.match(IGNORE_PATTERN, f) for f in files])
    logger.debug('MATCH FILTER: %s', matches_all_filters)

    logger.debug('<FILES:{}>'.format(files))
    if files and not matches_all_filters:
        used_folders.append(path)
    elif not re.match(IGNORE_PATTERN, str(path)):
        empty_folders.append(path)

''' Adds dependends/ancestors of used folders'''

for used in used_folders:
    for dependend in used.parents:
        used_folders_ancestors.append(dependend)

def generate_transactions(add=True, remove=True, remove_all=False):
    trans_add_labels, trans_remove_labels, trans_remove_all = [], [], []
    if add and not remove_all:
        trans_add_labels = [add_label_transaction(x) for x in empty_folders
                            if x not in used_folders_ancestors]

    if remove and not remove_all:
        trans_remove_labels = [remove_label_transaction(x) for x in
                            used_folders + used_folders_ancestors]

    if remove_all:
        trans_remove_all = [remove_label_transaction(x) for x in
                            used_folders + used_folders_ancestors + empty_folders]

    return trans_add_labels + trans_remove_labels + trans_remove_all


if __name__ == '__main__':
    transactions = generate_transactions()
    # transactions = generate_transactions(remove_all=True)
    apply_transactions(transactions)
