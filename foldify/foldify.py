import sys
import os
import shutil
from collections import OrderedDict
from pprint import pprint

from deepdiff import DeepDiff

import compat
from Tree import Tree


def prompt_source():
    source = input('Name of Source: \n>'.format())

    if os.path.exists(source):
        return source
    else:
        print('Path not found: [{}]'.format(source))


def prompt_dest(default_name, json=None):
    if json:
        rm_method = os.remove
        dest = input(
            'Name of JSON (.json will be added). Blank for folder name): \n>')
        dest = '{0}.json'.format(dest or default_name)
    else:
        rm_method = shutil.rmtree
        dest = input('Name of Desination Folder (Blank for NAME_copy): \n>')
        dest = dest or '{0}_copy'.format(default_name)

    if os.path.exists(dest):
        if input('Path already exists [{}]. Overwrite? (y/n): \n>'.format(
                                                                dest)) == 'y':
            try:
                rm_method(dest)
            except OSError as errmsg:
                print('Could not delete. {}'.format(errmsg))
            else:
                print('Deleted. ')
        else:
            print('Will Not overwritting.')
            return

    return dest


def menu_copy_folder_tree():
    """Copy Folder Tree."""
    source_folder = prompt_source()
    if not source_folder:
        return

    dest_folder = prompt_dest(source_folder)
    if not dest_folder:
        return

    tree = Tree(source_folder)
    tree.write_tree(dest_folder)
    # tree.print_tree()

    print('Folder Structure of [{0}] successfully copied to [{1}]'.format(
                                            source_folder, dest_folder))


def menu_json_from_folder():
    """Make Json from Folder."""
    source_folder = prompt_source()
    if not source_folder:
        return

    dest_file = prompt_dest(source_folder, json=True)
    if not dest_file:
        return

    tree = Tree(source_folder)
    tree.write_json(dest_file)
    print('New Json template created for folder [{}]'.format(source_folder))


def menu_folder_from_json():
    """Make Folder from Json."""
    source_file = prompt_source()
    if not source_file:
        return

    dest_folder = prompt_dest(source_file.replace('.json', ''))
    if not dest_folder:
        return

    tree = Tree(source_file, json=True)
    if hasattr(tree, 'root'):
        tree.write_tree(dest_folder)
        print('New folder [{}] created from json [{}]'.format(dest_folder,
                                                              source_file))


def menu_diff_trees():
    """Prints a diff betwen two trees."""
    source_first = prompt_source()
    if not source_first:
        return
    source_second = prompt_source()
    if not source_second:
        return

    first_is_file = os.path.isfile(source_first)
    second_is_file = os.path.isfile(source_second)

    first_dict = Tree(source_first, json=first_is_file).as_dict
    second_dict = Tree(source_second, json=second_is_file).as_dict

    ddiff = DeepDiff(first_dict, second_dict)

    pprint(ddiff, indent=2)


def menu_exit():
    """Exit the program."""
    sys.exit()

menu = (
    ('1', menu_copy_folder_tree),
    ('2', menu_json_from_folder),
    ('3', menu_folder_from_json),
    ('4', menu_diff_trees),
    ('5', menu_exit),
        )
menu = OrderedDict(menu)

if __name__ == '__main__':

    while True:
        print('='*30)
        print('Foldify - 2.1')
        print('='*30)
        for n, func in menu.items():
            print('{0} - {1}'.format(n, func.__doc__))
        selection = input('Select an option:')

        try:
            menu[selection]()
        except KeyError:
            print('Invalid Option')
