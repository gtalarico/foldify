import sys
from collections import OrderedDict

from helper import mkjson_from_folder, mkdirs_from_json_dict
from helper import load_file, dump_json


def menu_copy_folder_tree():
    """Copy Folder Tree."""
    source_folder = raw_input('Name of Source Folder: \n>>>')
    dest_folder = raw_input('Name of Destination Folder (Blank for X-copy): \n>>>')
    if dest_folder == '':
        dest_folder = '{}_copy'.format(source_folder)
    json_dict = mkjson_from_folder(source_folder)
    if json_dict and mkdirs_from_json_dict(dest_folder, json_dict):
        print 'Folder Structure of [{0}] successfully copied to [{1}]'.format(
                                            source_folder, dest_folder)


def menu_json_from_folder():
    """Make Json from Folder."""
    source_folder = raw_input('Name of Source Folder: \n>>>')
    dest_file = raw_input('Name of JSON (.json will be added; blank for same name): \n>>>')
    if dest_file == '':
        dest_file = source_folder

    json_dict = mkjson_from_folder(source_folder)
    if json_dict and dump_json(dest_file, json_dict):
        print 'New Json template created for folder [{}]'.format(source_folder)


def menu_folder_from_json():
    """Make Folder from Json."""
    source_file = raw_input('Name of Source JSON: \n>>>')
    dest_folder = raw_input('Name of Destination Folder (Leave Blank to try use json root): \n>>>')
    json_dict = load_file(source_file)
    if dest_folder == '':
        dest_folder = json_dict['name']
    if json_dict and mkdirs_from_json_dict(dest_folder, json_dict):
        print 'New folder [{}] created from json [{}]'.format(dest_folder,
                                                             source_file)



def menu_exit():
    """Exit the program."""
    sys.exit()


menu = (
    ('1', menu_copy_folder_tree),
    ('2', menu_json_from_folder),
    ('3', menu_folder_from_json),
    ('4', menu_exit)
        )
menu = OrderedDict(menu)

while True:
    print '='*30
    print 'Foldify'
    print '='*30
    for n, func in menu.items():
        print '{0} - {1}'.format(n, func.__doc__)
    selection = raw_input('Select an option:')
    try:
        menu[selection]()
    except KeyError:
        print 'Invalid Option'
