import unittest
import os
import json

from foldify.tree import Tree, Node, get_type, read_path

# from foldify python -m unittest discover -s ..

TEST_FOLDER = 'root'
TEST_DIR = os.path.dirname(os.path.realpath(__file__))
os.chdir(TEST_DIR)

TEMP_JSON = 'TEMP_JSON.json'


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
            tree = Tree('root', json=True)
        errmsg = "Specified JSON, gave folder: root"
        self.assertEqual(str(cm.exception), errmsg)
        self.assertIsInstance(cm.exception, TypeError)

class TestTreeFromFolder(unittest.TestCase):


    def setUp(self):
        self.tree = Tree('root')

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

    def test_json_string(self):
        as_string = self.tree.as_json_string
        as_json = json.loads(as_string)
        self.assertIsInstance(as_json, dict)

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

if __name__ == '__main__':
    unittest.main()
