from ezmailer import Renderer, Component, TrancludeMarker
from ezmailer.cmp_syntax import add_transclusion_operator
from ezmailer.transclusion import Transclusion
from ezmailer.utils import *
from odictliteral import odict
from treeprinter import TreePrinter

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

Component = add_transclusion_operator(Component, Transclusion)

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

tp.pprint(rd.render(Component(text_parent) > {
    "foot": Component(text_child) > Component(text_grand_child),
    "head": Component(text_grand_child)
}))
