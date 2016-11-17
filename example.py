from ezmailer import Renderer, Component, TrancludeMarker
from ezmailer.cmp_syntax import add_transclusion_operator
from odictliteral import odict
from treeprinter import TreePrinter

rd = Renderer()
text_parent = "<div><div>{}</div><div>{}</div></div>".format(TrancludeMarker(), TrancludeMarker())
text_child = "<child>{}</child>".format(TrancludeMarker())
text_grand_child = "<grandchild></grandchild>"

tp = TreePrinter("getchildren", "tag")


cp = Component(text_parent)
cp_child = Component(text_child)
res = rd.build(odict[cp: cp_child])
tp.pprint(res[0].tree)

Component = add_transclusion_operator(Component)

print(Component(text_parent) > (
    Component(text_child) > Component(text_grand_child),
    Component(text_grand_child)
))