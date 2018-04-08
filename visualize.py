import xml.etree.cElementTree as ET
from ete3 import Tree, TreeStyle
import re

class Node(object):
    def __init__(self, val, parent=None):
        self.val = val
        self.parent = parent
        self.children = {}
        self.nchild = 0 # num of children
        self.ncount= 0 # num of ImageNet1K children

    def update_child(self, node):
        self.children[self.nchild] = node
        self.nchild += 1

    def is_leaf(self):
        if len(self.children) == 0:
            return True
        else:
            return False

class ImageNet10K(object):
    def __init__(self, file):
        self.wnid = self.load(file)

    def load(self, file):
        with open(file,'r') as f:
            return ''.join(f.readlines()).split()


dic = ImageNet10K('wnid.txt')

def convert_treeAux(node, newick):
    """
    Convert tree to newick string format.
    """
    if node.is_leaf():
        newick.append(node.val)
    else:
        newick.append('(')
        for k,v in node.children.items():
            convert_treeAux(v, newick)
            newick.append(',')
        newick.append(')')



def pruning_count(node):
    """
    Counting the the number of leaves that are contained in ImageNet1K.
    """
    if node.is_leaf():
        if not node.val in dic.wnid:
            node.ncount = 0
            return 0
        else:
            node.ncount = 1
            return 1
    else:
        count = 0
        for i in node.children.keys():
            count += pruning(node.children[i])
        node.ncount = count
        return count



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
            dic[wnid] = Node(wnid, cur_tree)
            cur_tree.update_child(dic[wnid])

    return dic['fall11']


def remove_dumb(newick):
    p1 = r'\(,*\)'
    #result = re.findall(p1, newick)
    #print(newick)
    old_result = newick
    result = re.sub(p1, '', newick)
    c = 1
    while result != old_result:
        old_result = result
        result = re.sub(p1, '', result)
        print('replace %i times'%c)
        c+=1

    print(result)
    return result


def pruning(node):
    """
    Pruning the total tree, only reserve the subtrees that contrains 1000 classes.
    """
    queue = [node]
    pid  = [0]
    parent = None
    while len(queue)>0:
        x = queue.pop(0)
        id = pid.pop(0)
        if x.ncount == 0:
            x.parent.children.pop(id)
        else:
            for k,v in x.children.items():
                queue.append(v)
                pid.append(k)
            # parent =
        # print(pid)


tree = (vis_imagenet_structure())
pruning_count(tree)
pruning(tree)


newick = []
convert_treeAux(tree, newick)

newick = ''.join(newick)
newick = newick.replace(',)',')')
t = Tree(newick+';')
# print(t)

ts = TreeStyle()
ts.show_leaf_name = True
ts.branch_vertical_margin = 10
ts.rotation = 90
ts.mode = "c"
ts.arc_start = -180 # 0 degrees = 3 o'clock
ts.arc_span = 180
t.show(tree_style=ts)


t.render('tree.png', dpi=200, tree_style=ts)
# with open('imagenet_strcuture.txt','w') as f:
#    f.write(newick+';')

