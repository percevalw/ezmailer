from .component import TreeComponent, TrancludeMarker
from lxml import etree
from ..utils import make_tag


class Text(TreeComponent):
    def __init__(self, text):
        super().__init__(etree.fromstring("<p>{}</p>".format(text)))


class Link(TreeComponent):
    def __init__(self, **kwargs):
        tree_string = make_tag("a", kwargs, TrancludeMarker())
        super().__init__(etree.fromstring(tree_string))
