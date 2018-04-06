import xml.etree.cElementTree as ET
from ete3 import Tree


class Node(object):
    def __init__(self, val):
        self.val = val
        self.children = []

    def update_child(self, node):
        self.children.append(node)

    def is_leaf(self):
        if len(self.children) == 0:
            return True
        else:
            return False


def convert_treeAux(node, newick):
    if node.is_leaf():
        newick.append(node.val)
    else:
        newick.append('(')
        for i in node.children:
            convert_treeAux(i, newick)
            newick.append(',')
        newick.append(')')

def vis_imagenet_structure():
    tree=ET.ElementTree(file='structure_released.xml')
    root = tree.getroot()

    synset = root[1]
    dic = {'fall11':Node('fall11')}
    tree = dic['fall11']

    queue = [synset]

    while len(queue) > 0:
        node = queue.pop(0)
        cur_tree = dic[node.attrib['wnid']]
        for c in node:
            queue.append(c)
            wnid = c.attrib['wnid']
            dic[wnid] = Node(wnid)
            cur_tree.update_child(dic[wnid])

    return dic['fall11']

tree = (vis_imagenet_structure())
newick = []
convert_treeAux(tree, newick)
# print(tree.children[0].children)
# print(''.join(newick))

newick = ''.join(newick)
newick = newick.replace(',)',')')
# print(newick)
# print(newick.count('('),newick.count(')'))

t = Tree(newick+';')
# print(t)
t.render('tree.png', dpi=800)
# with open('imagenet_strcuture.txt','w') as f:
#    f.write(newick+';')
