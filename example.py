from ezmailer.utils import *

import ezmailer.cmp_syntax
from ezmailer.api import Renderer, TreeComponent, TextComponent, TrancludeMarker, Transclusion
from ezmailer.api.components import *
from treeprinter import TreePrinter
from lxml import etree

rd = Renderer()
text_parent = "<parent><head>{}</head><foot>{}</foot></parent>".format(TrancludeMarker("head"), TrancludeMarker("foot"))
text_child = "<child>{}</child>".format(TrancludeMarker())
text_grand_child = "<grandchild></grandchild>"

tp = TreePrinter("getchildren", "tag")


# cp = Component(text_parent)
# cp_child = Component(text_child)
# cp_grand_child = Component(text_grand_child)
# res = cp_child.transclude(__root__= cp_grand_child)
# tp.pprint(cp_child.tree)


def get_tree_children(obj):
    if isinstance(obj, Transclusion):
        return list(obj.children.items())
    elif isinstance(obj, tuple):
        return obj[1]


def get_tree_tag(obj):
    if isinstance(obj, Transclusion):
        return str(obj.component)
    elif isinstance(obj, tuple):
        return obj[0]

tpt = TreePrinter(get_tree_children, get_tree_tag)

tree_comp = (
    TreeComponent.fromstring(text_parent) > {
        "foot": P() > TreeComponent.fromstring(text_grand_child),
        "head": Cell() > Link() > [
            "Ceci est du texte",
            TreeComponent.fromstring(text_grand_child),
            "Ceci aussi"
        ]
    }
)
#print(tree_comp)
tpt.pprint(tree_comp)
html = etree.tostring(rd.render(tree_comp), pretty_print=True).decode('utf-8')
print(html)
# with open("example.html", 'w') as f:
#    f.write(html)
