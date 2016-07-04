import unittest
import os
import json
import shutil
import sys
sys.path.append('../foldify')
sys.path.append('foldify')

from foldify.tree import Tree, Node, get_type, read_path
from foldify.empty import generate_transactions, apply_transactions
from foldify.settings import EMPTY_LABEL, enable_debug
# from foldify python -m unittest discover -s ..


TEST_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(TEST_DIR)

TEST_FOLDER = 'root'
TEMP_JSON = 'root_temp.json'
TEMP_FOLDER = 'root_temp'

# enable_debug()


class TestNodeOpening(unittest.TestCase):

    def test_folder_not_fount(self):
        with self.assertRaises(SystemExit) as cm:
            tree = Tree('doesnotexist')
        errmsg = "Cannot find folder: doesnotexist"
        self.assertEqual(str(cm.exception), errmsg)
        self.assertIsInstance(cm.exception, SystemExit)

    def test_json_not_found(self):
        with self.assertRaises(SystemExit) as cm:
            tree = Tree('doesnotexist.json', json=True)
        errmsg = "Cannot open. Error: [Errno 2] No such file or directory: 'doesnotexist.json'"
        self.assertEqual(str(cm.exception), errmsg)
        self.assertIsInstance(cm.exception, SystemExit)

    def test_is_folder_not_json(self):
        # give folder, specify json
        with self.assertRaises(TypeError) as cm:
            tree = Tree(TEST_FOLDER, json=True)
        errmsg = "Specified JSON, gave folder: root"
        self.assertEqual(str(cm.exception), errmsg)
        self.assertIsInstance(cm.exception, TypeError)


class TestTreeFromFolder(unittest.TestCase):

    def setUp(self):
        self.tree = Tree(TEST_FOLDER)

    def test_dict(self):
        as_dict = self.tree.as_dict
        self.assertIsInstance(self.tree.as_dict, dict)
        self.assertEqual(as_dict['name'], 'root')
        self.assertEqual(len(as_dict), 3)
        self.assertEqual(as_dict['children'][0]['name'], 'Folder A')

    def test_tree(self):
        root_node = self.tree.root
        self.assertIsInstance(root_node, Node)
        self.assertEqual(root_node.name, 'root')
        child = root_node.children[0]
        self.assertIsInstance(child, Node)
        self.assertEqual(child.name, 'Folder A')

    def test_write_json(self):
        #  Tree object from folder. Writes Json. Reloads Compares
        self.tree.write_json(TEMP_JSON)
        with open(TEMP_JSON, 'r') as f:
            as_json = json.load(f)
        as_dict = self.tree.as_dict
        #  tree object vs as_json
        self.assertEqual(self.tree.root.children[0].name,
                         as_json['children'][0]['name'])
        self.assertEqual(as_json['name'], as_dict['name'])
        self.assertEqual(as_json['children'][0]['name'],
                         as_dict['children'][0]['name'])

    @classmethod
    def tearDownClass(self):
        try:
            os.remove(TEMP_JSON)
        except:
            pass


class TestLabeling(unittest.TestCase):

    def setUp(self):
        tree = Tree(TEST_FOLDER)
        tree.write_tree(TEMP_FOLDER)
        self.t = generate_transactions(path=TEMP_FOLDER, add=True, remove=True,
                                       remove_all=False)
        apply_transactions(self.t, auto=True)

    def tearDown(self):
            try:
                shutil.rmtree(TEMP_FOLDER)
            except:
                print(sys.exc_info[0])
                # pass

    def test_verify_transactions(self):
        t = self.t
        self.assertEqual(len(t), 5)  # 5 Renaming transactions would apply
        old_path, new_path = t[0][0].name, t[0][1].name
        self.assertEqual(old_path, 'Folder A-B')
        self.assertEqual(new_path, 'Folder A-B' + EMPTY_LABEL)

    def test_verify_renaming(self):
        subfolders = os.listdir(TEMP_FOLDER)
        temp_subfolder = ['Folder A', 'Folder B', 'File Root']
        labeled_temp_subfolder = ['Folder A', 'Folder B_EMPTY', 'File Root']
        self.assertEqual(os.listdir(TEST_FOLDER), temp_subfolder)
        self.assertEqual(os.listdir(TEMP_FOLDER), labeled_temp_subfolder)


if __name__ == '__main__':
    unittest.main()
