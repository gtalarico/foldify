import os
import json
from collections import OrderedDict


class PathO(object):

    def __init__(self, name, static_fullpath=None, children=[], parent=None):
        self.name = name
        self.children = children
        self.parent = parent
        self.static_fullpath = static_fullpath
        self.path_type = None

    @property
    def exists(self):
        return os.path.exists(self.static_fullpath)

    @property
    def isdir(self):
        if self.exists:
            return os.path.isdir(self.static_fullpath)

    @property
    def isfile(self):
        if self.exists:
            return not self.isdir
    # @property
    def get_path_type(self):
        if self.isdir:
            self.path_type = 'folder'
            return self.path_type
        elif self.isfile:
            self.path_type = 'file'
            return self.path_type

    @property
    def ancestors(self):
        return [a for a in self.iter_up()]

    @property
    def ancestors_fullpath(self):
        """Similar to fullpath, but it's build from path ancestors"""
        return os.path.join(*[x.name for x in reversed(self.ancestors)])

    @property
    def root(self):
        return self.ancestors[-1]


    def iter_up(self):
        ''' Iterates upwards: yields self first, and ends with root
        Does not iterate over cousings or ancestors not in a direct inheritance
        line towards root
         '''
        yield self
        if self.parent is None:
            pass
        else:
            for parent in self.parent.iter_up():
                yield parent

    def iter_down(self):
        ''' Iterates downwards
        yields self first, then iterates over
        its children's children recursevely
        ending with last lowest child
        '''
        yield self
        for child in self.children:
            # yield child
            for c in child.iter_down():
                yield c


    def get_json_dict(self, detailed=False):
        d = OrderedDict()
        d['name'] = self.name
        d['type'] = self.path_type
        d['children'] = [x.get_json_dict() for x in self.children]
        if detailed:
            d['parent'] = getattr(self.parent, 'name', None)
        return d

    def get_json_string(self):
        return json.dumps(self.get_json_dict(), encoding='utf-8',
                          ensure_ascii=False, sort_keys=False, indent=2,
                          separators=(',', ': '))


    def __repr__(self):
        return '<PATH:{0}|PARENT:{1}|CHILDS:{2}>'.format(
                                            self.name,
                                            getattr(self.parent,'name', None),
                                            len(self))


    def __len__(self):
        '''Returns number of children, files or folders'''
        if self.children:
            return len(self.children)
        else:
            return 0


def tree_from_folder(source_folder):
    ''' creates patho tree of patho objects from a local folder name'''
    patho = PathO(os.path.basename(source_folder), static_fullpath=source_folder)
    patho.get_path_type()
    try:
        patho.children = [tree_from_folder(os.path.join(source_folder,x)) for x in os.listdir(source_folder)]
    except OSError as errmsg:
        pass # if is file, listdir will fail
    else:
        for child in patho.children:
            child.parent = patho
    return patho


def tree_from_json_dict(json_dict):
    ''' creates a patho tree from a json_dict created by a patho tree'''
    patho = PathO(json_dict['name'])
    patho.path_type = json_dict['type']
    # import pdb; pdb.set_trace()
    try:
        patho.children = [tree_from_json_dict(x) for x in json_dict['children']]
    except KeyError:
        pass
    else:
        for child in patho.children:
            child.parent = patho
    return patho



if __name__ == '__main__':

    # TESTS
    def test_tree_from_folder():
        tree = tree_from_folder('root')
        # print tree.get_json_string()
        for i in tree.iter_down():
            print i.static_fullpath
            print i.ancestors_fullpath
            print i.path_type
        # print tree.children[0].children[1].root
        # for i in tree.children[0].children[1].iter_up():
        #     print i
        # print tree.children[0].children[1].fullpath
        return tree
    tree = test_tree_from_folder()

    json_dict = tree.get_json_dict()
    print '='*20
    print json_dict



    def test_tree_from_json_dict(json_dict):
        tree = tree_from_json_dict(json_dict)
        print tree
        print tree.root
        print tree.get_json_string()
    test_tree_from_json_dict(json_dict)
