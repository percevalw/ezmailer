from .component import Component
from .transclusion import Transclusion
import collections


class Renderer:
    def __init__(self, **params):
        pass

    def render(self, transclusion):
        return transclusion.build().tree
