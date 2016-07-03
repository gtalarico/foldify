import unittest
from foldify.tree import Tree, Node, get_type, read_path

# from foldify python -m unittest discover -s ..

TEST_FOLDER = 'root'

# TODO:
# Rewrite all tests!

class TestNode(unittest.TestCase):

    def setUp(self):
        self.tree = Tree('root.json')



        # with self.assertRaises(TypeError):
            # s.split(2)

if __name__ == '__main__':
    unittest.main()
