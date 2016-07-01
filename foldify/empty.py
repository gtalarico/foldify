import os
import sys
import shutil
import logging
import re

from pathlib import *

logger = logging.getLogger('empty_label')

# TO DO:

# Add logger
# Run with Arg or local
# Show Confirmation
# Function Remove Labels

# Args: Ignore,


# from Tree import Tree
# try:
    # shutil.rmtree('WDRIVE_COPY')
# except:
    # print('Not deleted')
    # pass

# tree = Tree('tests/wdrive')
# tree.write_tree('WDRIVE_COPY')
# sys.exit()

EMPTY_LABEL = '_EMPTY'

IGNORE = ['(desktop.ini)']
# IGNORE = ['(desktop.txt)', '(.*\.txt)']
IGNORE_PATTERN = r'|'.join(IGNORE)

used_folders = []
empty_folders = []

def label_empty(path):
    print('LABEL: Checking for label:: ', path)
    if not path.name.endswith(EMPTY_LABEL):
        print('LABEL: Adding LABEL: ', path)
        new_path = Path(path.parent, path.name + EMPTY_LABEL)
        try:
            path.rename(new_path)
        except:
            print(sys.exc_info()[0].__name__)
        else:
            print('LABEL: RENAMED: ', new_path)

def remove_label(path):
    print('REMOVE LABEL: Checking for label:: ', path)
    if path.name.endswith(EMPTY_LABEL):
        print('REMOVE LABEL: Removing:: ', path)
        new_name = Path(path.parent, path.name.split(EMPTY_LABEL)[0])
        path.rename(new_name)
        print('REMOVE LABEL: RENAMED: ', path)


def listDirs(dir):
    for root, subFolders, files in os.walk(dir, topdown=False):
        print('ROOT:', root)
        print('SUBS:', subFolders)
        print('FILES:', files)
        path = Path(root)
        # print('PAT:', any([re.match(IGNORE_PATTERN, f) for f in files]))
        if not files or any([re.match(IGNORE_PATTERN, f) for f in files]):
            # print('EMPTY')
            empty_folders.append(path)
        else:
            # print('>>>>>>>USED')
            used_folders.append(path)

        # for folder in subFolders:
            # print('>>FOLDER:', folder)
            # yield Path(root, folder)

listDirs('tests/root')
# for i in listDirs('tests/root'):
    # pass
    # os.rename(i, '{}_EMPTY'.format(i))

# listDirs('tests/root')

used_folders_ancestors = []
for used in used_folders:
    for dependend in used.parents:
        used_folders_ancestors.append(dependend)

print('USED:' , used_folders)
print('USED DEPENDENDS:' , used_folders_ancestors)


[label_empty(x) for x in empty_folders if x not in used_folders_ancestors]
[remove_label(x) for x in used_folders + used_folders_ancestors]

# [remove_label(x) for x in used_folders + used_folders_ancestors + empty_folders]
