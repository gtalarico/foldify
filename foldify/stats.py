import os
from Tree import Tree, Node

class TreeStats(Tree):

    def __init__(self, *args, **kwargs):
        super(TreeStats, self).__init__(*args, **kwargs)
        self.iter_down()

    def iter_down(self):
        def iter_children(node, ancestors='', level=0):
            level += 1
            ancestors = os.path.join(ancestors, str(node.name))
            self.flat_nodes.append(node.name)
            # self.flat_nodes.append((node.name, ancestors, level))

            for child in node.children:
                iter_children(child, ancestors, level)

        self.flat_nodes = [self.root.name]
        # self.flat_nodes = [(self.root.name, 0)]
        iter_children(self.root)

    @property
    def node_count(self):
        return len(self.flat_nodes)

    @property
    def levels(self):
        return max([level for name, level in self.flat_nodes])


class TreeDiff(object):
    def __init__(self, tree_left, tree_right):
        self.set_left = set(tree_left.flat_nodes)
        self.set_right= set(tree_right.flat_nodes)

        self.union = self.set_left.union(self.set_right)
        self.diff_left = self.set_left.difference(self.set_right)
        self.diff_right = self.set_right.difference(self.set_left)



stree = TreeStats('tests/wdrive', json=False)
stree2 = TreeStats('tests/wdrive2', json=False)

diff = TreeDiff(stree, stree2)

# print(stree.as_dict)
# stree.iter_down()
# print(stree.flat_nodes)
# print(stree.node_count)
# print(stree.levels)

# stree.iter_up(stree.root.children[0].children[0])
# print(stree.ancestors)
