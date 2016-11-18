from ezmailer import Renderer, Component, TrancludeMarker
from ezmailer.cmp_syntax import add_transclusion_operator
from ezmailer.transclusion import Transclusion
from ezmailer.utils import *
from odictliteral import odict
from treeprinter import TreePrinter

rd = Renderer()
text_parent = "<div><div>{}</div><div>{}</div></div>".format(TrancludeMarker(), TrancludeMarker())
text_child = "<child>{}</child>".format(TrancludeMarker())
text_grand_child = "<grandchild></grandchild>"

tp = TreePrinter("getchildren", "tag")


cp = Component(text_parent)
cp_child = Component(text_child)
#res = rd.build(odict[cp: cp_child])
#tp.pprint(res[0].tree)

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

tpt.pprint(Component(text_parent) > {
    "head": Component(text_child) > Component(text_grand_child),
    "foot": Component(text_grand_child)
})