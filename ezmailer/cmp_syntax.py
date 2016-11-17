import collections
from treeprinter import TreePrinter


def as_sequence(obj):
    if isinstance(obj, collections.Sequence):
        return obj
    return [obj]


def collection_values(obj):
    return obj.values() if isinstance(obj, collections.Mapping) else obj


@TreePrinter(lambda obj: [o for l in collection_values(obj.children) for o in l], lambda obj: str(obj.component))
class Transclusion:
    def __init__(self, component, parent=None, children=None):
        self.component = component
        self.children = children if children else []
        self.parent = parent

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, p):
        self._parent = p

    @property
    def root(self):
        return self.parent.root if self.parent else self


def add_transclusion_operator(cls):
    new_dict = dict(cls.__dict__)

    def as_transclusion(self, obj, parent=None):
        if isinstance(obj, Transclusion):
            obj.parent = parent
            return obj
        elif hasattr(obj, 'get_or_create_transclusion'):
            return obj.get_or_create_transclusion(parent)
        else:
            raise Exception("{} should be either a Component or a Transclusion".format(type(obj)))

    def get_or_create_transclusion(self, parent=None):
        if not self.__transclusion__:
            self.__transclusion__ = Transclusion(self, parent)
        return self.__transclusion__

    def gt(self, other):
        t = self.get_or_create_transclusion()
        if isinstance(other, collections.Mapping):
            children = other.__class__({k: as_sequence(as_transclusion(t, v)) for k, v in other.items()})
        elif isinstance(other, collections.Sequence):
            children = other.__class__([as_sequence(as_transclusion(t, v)) for v in other])
        elif isinstance(other, self.__class__):
            children = [[as_transclusion(t, other)]]
        else:
            raise Exception("Right member in > inclusion must be either a mapping, a sequence or a includable element")
        t.children = children
        return t.root

    def init(self, *args, **kwargs):
        cls.__dict__['__init__'](self, *args, **kwargs)
        self.__transclusion__ = None

    new_dict['__gt__'] = gt
    new_dict['__init__'] = init
    new_dict['get_or_create_transclusion'] = get_or_create_transclusion
    new_type = type(cls.__name__, cls.__bases__, new_dict)
    return new_type
