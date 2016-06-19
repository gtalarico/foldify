import os
import json
from collections import OrderedDict


class PATH_TYPE:
    FOLDER = 'folder'
    FILE = 'file'
    OTHER = 'N/A'


class PATH_DATA:
    NAME = 'name'
    TYPE = 'type'
    CHILDREN = 'children'


class Node(object):
    def __init__(self, path_data):
        self.name = path_data.get(PATH_DATA.NAME, None)
        self.parent = None
        self.type = path_data.get(PATH_DATA.TYPE, PATH_TYPE.OTHER)
        self.children = [
            Node(child)
            for child in path_data.get(PATH_DATA.CHILDREN, [])
        ]
        for child in self.children:
            child.parent = self

    def get_dict(self):
        return OrderedDict({
            PATH_DATA.NAME: self.name,
            PATH_DATA.TYPE: self.type,
            PATH_DATA.CHILDREN: [child.get_dict() for child in self.children]
        })


class Tree(object):
    ''' Create a Tree Object from a path or valid json.
    tree = Tree('folder', json=False)
    path: a valid relative path_data
    json: true to make tree from json file instead of path_data

    Methods:
    tree.write_json(destination)
    tree.write_tree(destination)
    '''

    def __init__(self, path, json=False):
        read_func = read_json if json else read_path
        data = read_func(path)
        if data:
            self.root = Node(data)

    def write_json(self, path):
        with open(path, 'w') as f:
            json.dump(self.root.get_dict(), f, indent=2)

    def write_tree(self, path):
        join = os.path.join
        path, name = os.path.split(path)
        self.root.name = name

        def make(path, node):
            path = join(path, node.name)
            if node.type == PATH_TYPE.FOLDER:
                os.makedirs(path)
            elif node.type == PATH_TYPE.FILE:
                with open(path, 'a') as f:
                    pass

            for child in node.children:
                make(path, child)
        make(path, self.root)

    def print_tree(self):
        print(json.dumps(self.root.get_dict(), indent=2))


#  Helper functions
def get_type(path):
    exists = os.path.exists
    isdir = os.path.isdir
    if not exists(path):
        print('[{}] does not exist.'.format(path))
        return PATH_TYPE.OTHER
    if isdir(path):
        return PATH_TYPE.FOLDER
    return PATH_TYPE.FILE


def read_path(path):
    obj = {
        PATH_DATA.NAME: os.path.basename(path),
        PATH_DATA.TYPE: get_type(path)
    }
    if obj[PATH_DATA.TYPE] == PATH_TYPE.FOLDER:
        join = os.path.join
        obj[PATH_DATA.CHILDREN] = [
            read_path(join(path, file_name))
            for file_name in os.listdir(path)
        ]

    # Print not for directory not found.
    if obj[PATH_DATA.TYPE] == PATH_TYPE.OTHER:
        print('Path was not found. Tree is empty.')

    return obj


def read_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except IOError as errmsg:
        print('Cannot open json File. Error: {}'.format(errmsg))
