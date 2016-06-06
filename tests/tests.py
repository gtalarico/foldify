import unittest
from foldify.path_tree import PathO, tree_from_folder, tree_from_json_dict

TEST_FOLDER = 'root'

class TestPa
class TestPathTreeClass(unittest.TestCase):

    def setUp(self):
        root = PathO('rootpath')
        child1 = PathO('child1')
        child2 = PathO('child2')
        root.children = [child1, child2]
        self.tree = root

    def test_tree(self):
        assert isinstance(self.tree, PathO)
        assert self.tree.root.name == 'rootpath'
        assert len(self.tree) == 2

    def test_children(self):
        child1 = self.tree.children[0]
        assert isinstance(child1, PathO)
        assert len(child1) == 0
        assert child1.name == 'child1'
        assert child1.root.name == 'rootpath'
        import pdb; pdb.set_trace()
        assert child1.parent.name == 'rootpath'

        # with self.assertRaises(TypeError):
            # s.split(2)

if __name__ == '__main__':
    unittest.main()
