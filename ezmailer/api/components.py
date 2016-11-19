from .component import Component
from lxml import etree


class Text(Component):
    def __init__(self, text):
        super().__init__(etree.fromstring("<p>{}</p>".format(text)))
