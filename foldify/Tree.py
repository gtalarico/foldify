import os
import sys
import json
import shutil
from collections import OrderedDict

from settings import ALLOWED_FILES


class PATH_TYPES:
    FOLDER = 'folder'
    FILE = 'file'


class PATH_KEYS:
    NAME = 'name'
    TYPE = 'type'
    CHILDREN = 'children'


class Node(object):
    ''' Node Instance Class.
    node = Node(path_data)
    path_data = {}
    : param : self.name
    : param : self.type
    : param : self.children
    : method : node.get_dict() > dict({
                                       PATH_KEYS.NAME : self.name,
                                       PATH_KEYS.TYPE = self.type,
                                       PATH_KEYS.CHILDREN = self.children
                                       })
    '''
    def __init__(self, path_data):
        self.parent = None
        self.name = path_data.get(PATH_KEYS.NAME, None)
        self.type = path_data.get(PATH_KEYS.TYPE, None)
        self.children = [
            Node(child)
            for child in path_data.get(PATH_KEYS.CHILDREN, [])
        ]
        for child in self.children:
            child.parent = self

    def get_dict(self):
        d = OrderedDict()
        d[PATH_KEYS.NAME] = self.name
        d[PATH_KEYS.TYPE] = self.type
        d[PATH_KEYS.CHILDREN] = [child.get_dict() for child in self.children]
        return d

    def __iter__(self):
        for child in self.children:
            yield child

    def __repr__(self):
        return '<NODE: {} | TYPE:{}>'.format(self.name, self.type)


class Tree(object):
    ''' Create a Tree Object from a path or valid json.
    tree = Tree(path, json=False)
    path: a valid relative path_data ('tests/foldername')
    json: true to make tree from json file instead of path_data

    : param : self.root > returns root Node


    Methods:
    tree.write_json(destination)
    tree.write_tree(destination)

    Properties:
    tree.as_dict > self.root.get_dict()
    tree.as_json_string > json.dumps(self.root.get_dict())
    '''

    def __init__(self, path, json=False):
        read_func = read_json if json else read_path
        path_dict = read_func(path)
        self.root = Node(path_dict)

    def write_json(self, path):
        with open(path, 'w') as f:
            json.dump(self.root.get_dict(), f, indent=2)

    def delete_if_dir_exists(self, path):
        if os.path.isdir(path):
            try:
                shutil.rmtree(path)
                print('WARNING: Existing directory deleted.')
            except:
                print('ERROR: Could not overwrite:')
                print(sys.exc_info()[0].__name__)
                sys.exit()


    def write_tree(self, path):
        self.delete_if_dir_exists(path)

        join = os.path.join
        path, name = os.path.split(path)
        self.root.name = name

        def make(path, node):
            path = join(path, node.name)
            if node.type == PATH_TYPES.FOLDER:
                try:
                    os.makedirs(path)
                except:
                    raise
            elif node.type == PATH_TYPES.FILE:
                with open(path, 'a') as f:
                    pass

            for child in node.children:
                make(path, child)
        make(path, self.root)
        print('write_tree completed [{}]'.format(path))

    @property
    def as_dict(self):
        return self.root.get_dict()

    @property
    def as_json_string(self):
        return json.dumps(self.as_dict)

    def print_tree(self):

        def print_node(node, level=0):
            print('{level} {name}'.format(level='|'*level or '|',
                                          name=node.name))
            level += 1
            for child in node.children:
                print_node(child, level)

        print_node(self.root)

    def __repr__(self):
        return '<TREE: {}>'.format(self.root.name)

#  Helper functions
def get_type(path):
    exists = os.path.exists
    isdir = os.path.isdir
    if isdir(path):
        return PATH_TYPES.FOLDER
    return PATH_TYPES.FILE


def read_path(path):
    if not os.path.exists(path):
        print('Cannot find foder: {}'.format(path))
        sys.exit()
    else:
        path_dict = {
            PATH_KEYS.NAME: os.path.basename(path),
            PATH_KEYS.TYPE: get_type(path)
        }
        splittext = os.path.splitext  # returns tuple (filename, extension)

        if path_dict[PATH_KEYS.TYPE] == PATH_TYPES.FOLDER:
            join = os.path.join
            path_dict[PATH_KEYS.CHILDREN] = [
                read_path(join(path, file_name))
                for file_name in os.listdir(path)
                if splittext(file_name)[1] in ALLOWED_FILES]

        return path_dict


def read_json(path):
    try:
        with open(path, 'r') as f:
            path_dict = json.load(f)
            return path_dict
    except IOError as errmsg:
        print('Cannot open json File. Error: {}'.format(errmsg))
        sys.exit()


if __name__ == '__main__':

    tree = Tree('tests/wdrive')
    tree.print_tree()
