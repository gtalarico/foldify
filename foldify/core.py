import json
import sys
import os
import shutil
import copy

from path_tree import tree_from_folder, tree_from_json_dict

# TO DO:
# Add Tests

# Functionality:
# 4. Validate Dir (print delta)
# 5. Migratation file scrips (x becomes y, z > y) -advanced
# interface:
# stage a: command line, OS folder selector
# stage b: pyside or tkinter interface


def load_file(source_file):
    ''' loads a json, returns a python list/dictionary object'''
    try:
        with open(source_file, 'r') as f:
            try:
                return json.load(f)
            except ValueError as e:
                print("Could Not Parse Json: {}".format(e))
    except IOError as errmsg:
        print errmsg
# tree = load_file('test.json')


def dump_json(filename, json_dict):
    ''' creates a .json file from a python object '''
    filename = '{0}.json'.format(filename)
    try:
        with open(filename, 'wx') as outfile:
            json.dump(json_dict, outfile, indent=2)
    except IOError as errmsg:
        print errmsg
    else:
        return True


# dump_json('test.json', tree.get_json_dict())


def mkdirs_from_json_dict(new_foldername, json_dict):
    if os.path.exists(new_foldername):
        print 'Cannot Copy. Folder already exists: ', new_foldername
        return

    new_tree = tree_from_json_dict(json_dict)
    new_tree.root.name = new_foldername     # set rootname of new folder

    failed = False
    for patho in new_tree.iter_down():
        if patho.path_type == 'folder':
            try:
                os.makedirs(patho.ancestors_fullpath)
            except OSError as errmsg:
                import pdb; pdb.set_trace()
                print errmsg
                failed = True
                break
        else:
            try:
                with open(patho.ancestors_fullpath, 'w') as f:
                    pass
            except OSError as errmsg:
                print errmsg
                failed = True
                break

    if not failed and os.path.exists(new_tree.root.ancestors_fullpath):
        return True
    else:
        print 'Make Dirs Operation Failed Deleting tree: ', new_foldername
        try:
            shutil.rmtree(new_tree.root.fullpath)
        except:
            print 'Attempted but failed to delete folder: ', new_foldername


def mkjson_from_folder(source_folder):
    """Returns Json_dict from folder, None if Folder not found or error"""
    if os.path.isdir(source_folder):
        tree = tree_from_folder(source_folder)
        return tree.get_json_dict()
    else:
        print 'Failed to make json. Folder not found: [{}]'.format(source_folder)

def compare_folders(source_folder, dest_folder):
    match, mismatch = [], []

    if os.path.isdir(source_folder) and os.path.exists(dest_folder):
        for source, dest in zip(os.walk(source_folder), os.walk(dest_folder)):
            source_children = source[1]
            dest_children = dest[1]
            if source_children == dest_children:
                match.append(source[0])
            else:
                mismatch.append((source_children,'<>', dest_children))
    return match, mismatch

if __name__ == '__main__':
    json_dict = load_file('root.json')
    tree = tree_from_json_dict(json_dict)
    # mkdirs_from_json_dict('rootnew2', tree.get_json_dict())
