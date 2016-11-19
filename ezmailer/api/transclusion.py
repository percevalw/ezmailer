import collections

class Transclusion:
    def __init__(self, component, parent=None, children=None):
        self.component = component
        self._children = children if children else {}
        self._parent = parent

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, p):
        self._parent = p

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, c):
        # TODO Add test on children to only accept Transclusion list
        self._children = c

    @property
    def root(self):
        return self.parent.root if self.parent else self

    def build(self):
        rendered_children = {
            key: [t.build() for t in sub_transclusions] for key, sub_transclusions in self.children.items()
        }
        self.component.transclude(**rendered_children)
        return self.component