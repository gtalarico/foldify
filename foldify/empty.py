import os
import sys
import shutil
import re
import sys

from pathlib import Path

from settings import IGNORE_PATTERN, EMPTY_LABEL, logger, enable_debug
from compat import input


def add_label_transaction(path, label=EMPTY_LABEL):
    if not path.name.endswith(label):
        new_path = Path(path.parent, path.name + label)
        return (path, new_path)


def remove_label_transaction(path, label=EMPTY_LABEL):
    if path.name.endswith(label):
        new_path = Path(path.parent, path.name.split(label)[0])
        return (path, new_path)


def apply_transactions(transactions, auto=False):
    ''' Apply renaming transactions.
    apply_transactions(transactions)
    transactions = [(old_path, new_path),(old_path),(new_path),...]
    Manual review of transactions is required.
    '''
    if auto:
        logger.warning('Auto is On. No confirmation required.')
    print('='*30)
    if not transactions:
        logger.debug('NO TRANSACTIONS')
        sys.exit('No Transactions to apply.')
        return

    for t in transactions:
        print('[{}] > [{}]'.format(t[0].name, t[1].name))
    print('{} Transactions to apply. Renaming...'.format(len(transactions)))
    count = 0
    if auto or input('EXECUTE ? [y]\n>') == 'y':
        for src, dst in transactions:
            try:
                src.rename(dst)
            except:
                logger.error(sys.exc_info()[0].__name__)
                logger.error('Could not rename: [{}]>[{}]'.format(src, dst))
            else:
                logger.debug('[{}] renamed to [{}]'.format(src, dst))
                count += 1

        print('{} folders renamed.'.format(count))


def generate_transactions(path=os.getcwd(), label=None,
                          add=True, remove=True, remove_all=False):
    ''' Iterates through directory.
    used_folders: folders that have files
    empty_folders: folders that DO NOT have files
    '''
    # Could be handled with default, but this allows arparse label=None.
    if label is None:
        label = EMPTY_LABEL

    empty_folders = []
    used_folders = []
    used_folders_ancestors = []

    for root, subFolders, files in os.walk(path, topdown=False):
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

    ''' Adds dependends/ancestors of used folders.
    if x/folder/folder2 is not empty,
    x, and x/folder will get added to used_folders_ancestors
    to ensure the "parents" are not tagged as empty.'''
    for used in used_folders:
        for dependend in used.parents:
            used_folders_ancestors.append(dependend)

    trans_add_labels, trans_remove_labels, trans_remove_all = [], [], []

    if add and not remove_all:

        trans_add_labels = [add_label_transaction(x, label=label)
                            for x in empty_folders
                            if x not in used_folders_ancestors and
                            add_label_transaction(x, label=label)
                            is not None]

    if remove and not remove_all:
        trans_remove_labels = [remove_label_transaction(x, label=label)
                               for x in used_folders + used_folders_ancestors
                               if remove_label_transaction(x, label=label)
                               is not None]

    if remove_all:
        trans_remove_all = [remove_label_transaction(x, label=label)
                            for x in used_folders + used_folders_ancestors +
                            empty_folders
                            if remove_label_transaction(x, label=label)
                            is not None]

    return trans_add_labels + trans_remove_labels + trans_remove_all


if __name__ == '__main__':
    # enable_debug()
    transactions = generate_transactions()
    # transactions = generate_transactions(label='_EMP')
    transactions = generate_transactions(remove_all=True)
    apply_transactions(transactions, auto=True)
