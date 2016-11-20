from .component import TreeComponent, TrancludeMarker
from lxml import etree
from ..utils import make_tag as mt


# __all__ = ['P', 'Link', 'Cell', 'Row', 'Button']


class P(TreeComponent):
    def __init__(self, **kwargs):
        tree_string = mt("p", kwargs, TrancludeMarker())
        super().__init__(etree.fromstring(tree_string))


class Link(TreeComponent):
    def __init__(self, **kwargs):
        tree_string = mt("a", kwargs, TrancludeMarker())
        super().__init__(etree.fromstring(tree_string))

    def __repr__(self):
        return etree.tostring(self.tree).decode('utf-8')


class Box(TreeComponent):
    def __init__(self, **kwargs):
        tree_string = mt("table", kwargs,
                         mt("tbody", {}, TrancludeMarker()))
        super().__init__(etree.fromstring(tree_string))


class Row(TreeComponent):
    def __init__(self, **kwargs):
        tree_string = mt("tr", kwargs, TrancludeMarker())
        super().__init__(etree.fromstring(tree_string))


class Cell(TreeComponent):
    def __init__(self, **kwargs):
        tree_string = mt("td", kwargs, TrancludeMarker())
        super().__init__(etree.fromstring(tree_string))


class Button(Link):
    def __init__(self, **kwargs):
        super().__init__(cl="btn btn-primary", **kwargs)


class Email(TreeComponent):
    def __init__(self, style=None):
        tree_string = mt("html", {},
                         mt("head", {},
                            mt("style", {}, style) if style else "") +
                         mt("body", {}, TrancludeMarker()))
        super().__init__(etree.fromstring(tree_string))
