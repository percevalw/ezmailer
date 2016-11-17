from .component import Component
import collections


class Renderer:
    def __init__(self, **params):
        pass

    def build(self, components_tree):
        if isinstance(components_tree, collections.Mapping):
            return [parent
                    for parent, content in components_tree.items()
                    for (_) in (parent.transclude(self.build(content)),)]
        if isinstance(components_tree, collections.Sequence):
            return [self.build(content)
                    for content in components_tree]
        if isinstance(components_tree, Component):
            return components_tree
        raise Exception("build parameter should be a mapping, a list or a Component")
