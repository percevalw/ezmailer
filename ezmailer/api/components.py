from .component import TreeComponent, TrancludeMarker
from lxml import etree
from ..utils import make_tag

__all__ = ['P', 'Link', 'Cell']


class P(TreeComponent):
    def __init__(self, **kwargs):
        tree_string = make_tag("p", kwargs, TrancludeMarker())
        super().__init__(etree.fromstring(tree_string))


class Link(TreeComponent):
    def __init__(self, **kwargs):
        tree_string = make_tag("a", kwargs, TrancludeMarker())
        super().__init__(etree.fromstring(tree_string))

    def __repr__(self):
        return etree.tostring(self.tree).decode('utf-8')


class Cell(TreeComponent):
    def __init__(self, **kwargs):
        tree_string = make_tag("table", kwargs,
                               make_tag("tbody", {}, TrancludeMarker()))
        super().__init__(etree.fromstring(tree_string))
