from ezmailer import Renderer, Component, TrancludeMarker
from odictliteral import odict
from treeprinter import TreePrinter

rd = Renderer()
text = "<div><div>{}</div><div>{}</div></div>".format(TrancludeMarker(), TrancludeMarker())
text_child = "<child></child>"

tp = TreePrinter("getchildren", "tag")

cp = Component(text)
cp_child = Component(text_child)
res = rd.build(odict[cp: cp_child])
tp.pprint(res[0].tree)
