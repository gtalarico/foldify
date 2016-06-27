import sys
import os
import argparse
import re
from argparse import RawDescriptionHelpFormatter as help_formatter

from Tree import Tree

# TODO:
# Improvements: Add reddit suggestions
# bug: handle overwite folder


def is_json(filename):
    try:
        if filename.split('.')[1].lower() == 'json':
            return True
    except:
        pass
    return False

def prep_path(path):
    ''' Ensure path complies with system'''
    path = re.sub(r'(\\)|(/)(\\\\)','/', path)
    return os.path.join(path)



usage = 'python foldify.py source_file [destination_file] [--help]'
description = '''
-------------------------------------------------------

Foldify - CLI tools for managing directory Trees.
Operations:

## Print a directory tree ##
$ foldify directory1

## Copy a directory Tree ##
$ foldify directory1 directory2

## Create Json from a directory ##
$ foldify directory1 directory1.json

## Create Directory from json ##
$ foldify directory1.json directory1

Json data must be stored in a file with .json extension

-------------------------------------------------------
'''


parser = argparse.ArgumentParser(prog='Foldify', description=description,
                                 usage=usage,
                                 formatter_class=help_formatter,
                                 )

parser.add_argument('source_file', type=str,
                    help='Source filepath.')

parser.add_argument('dest_file', type=str, nargs='?',
                    help='Destination filepath.')

args_dict = vars(parser.parse_args())
globals().update(args_dict)

# ensure source_file exists, if not exit.
exists = os.path.exists
if not exists(source_file):
    print('='*40)
    parser.print_help()
    print('='*40)
    print('ERROR: source_file does not exist.')
    sys.exit()


# If no dest_file, print source_tree
if not dest_file:
    tree = Tree(source_file, json=is_json(source_file))
    print('='*40)
    tree.print_tree()
    print('='*40)
    sys.exit()

# if dest_file exists, prompt for overwite before continuing.
if exists(dest_file):
    if input('WARNING: dest_file already exists. Overwrite? (y/n)') != 'y':
        print('Exiting.')
        print('='*40)
        sys.exit()


# Copy folder, json from dir, or dir from json, depending on formats.
tree = Tree(source_file, json=is_json(source_file))
write_dest = tree.write_json if is_json(dest_file) else tree.write_tree
write_dest(dest_file)
