#!/usr/bin/env python

import sys
import os
import argparse
import re
from argparse import RawDescriptionHelpFormatter as help_formatter

from tree import Tree, is_json
from empty import generate_transactions, apply_transactions
from settings import logger, enable_debug
from compat import input

from __init__ import __version__, __author__


def main():
    usage = 'python foldify.py source_file [destination_file] [--label] [--help]'
    description = '''
    ======================================================
    Foldify - CLI tools for managing directory Trees.
    Version: {version}
    Author: {author}

    Operations:

    ## Print a directory tree ##
    $ foldify directory1

    ## Label empty Folder in tree ##
    $ foldify directory1 --label [update, remove]

    ## Copy a directory Tree ##
    $ foldify directory1 directory2

    ## Create Json from a directory ##
    $ foldify directory1 directory1.json

    ## Create Directory from json ##
    $ foldify directory1.json directory1

    ======================================================
    '''.format(version=__version__, author=__author__)

    parser = argparse.ArgumentParser(prog='Foldify', description=description,
                                     usage=usage,
                                     formatter_class=help_formatter,
                                     )

    parser.add_argument('source_file', type=str,
                        help='Source filepath.')

    parser.add_argument('-l', '--label', choices=['update', 'remove'],
                        help='Adds Label _EMPTY to empty folders.')

    parser.add_argument('--custom-label', help='Customizes empty label.')

    parser.add_argument('dest_file', type=str, nargs='?',
                        help='Destination filepath.')

    parser.add_argument('-v', '--verbose', action='store_true')

    args_dict = vars(parser.parse_args())
    globals().update(args_dict)
    # print(args_dict)

    if verbose:
        enable_debug()

    # ensure source_file exists, if not exit.
    exists = os.path.exists
    if not exists(source_file):
        print('=' * 40)
        parser.print_help()
        print('=' * 40)
        print('ERROR: source_file does not exist.')
        sys.exit()

    #  If no dest_file, print source_tree
    if not dest_file:
        if label:
            t = generate_transactions(path=source_file, label=custom_label,
                                      remove_all=bool(label == 'remove'))
            apply_transactions(t)
        else:
            tree = Tree(source_file, json=is_json(source_file))
            print('=' * 40)
            tree.print_tree()
            print('=' * 40)
        sys.exit('Done.')

    # if dest_file exists, prompt for overwite before continuing.
    if exists(dest_file):
        if label:
            sys.exit('Must use only source_file with --label option.')
        if input('WARNING: dest_file already exists. Overwrite? (y/n)') != 'y':
            print('Exiting.')
            print('=' * 40)
            sys.exit()

    # Copy folder, json from dir, or dir from json, depending on formats.
    tree = Tree(source_file, json=is_json(source_file))
    write_dest = tree.write_json if is_json(dest_file) else tree.write_tree
    write_dest(dest_file)

if __name__ == '__main__':
    main()
