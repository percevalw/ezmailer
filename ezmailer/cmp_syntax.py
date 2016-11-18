import collections
from .utils import as_sequence
from .component import TrancludeMarker


def add_transclusion_operator(cls, transclusion_cls):
    new_dict = dict(cls.__dict__)

    def as_transclusion(self, obj, parent=None):
        if isinstance(obj, transclusion_cls):
            obj.parent = parent
            return obj
        elif hasattr(obj, 'get_or_create_transclusion'):
            return obj.get_or_create_transclusion(parent)
        else:
            raise Exception("{} should be either a Component or a Transclusion".format(type(obj)))

    def get_or_create_transclusion(self, parent=None):
        if not self.__transclusion__:
            self.__transclusion__ = transclusion_cls(self, parent)
        return self.__transclusion__

    def gt(self, other):
        t = self.get_or_create_transclusion()
        if isinstance(other, collections.Mapping):
            children = {key: [as_transclusion(t, comp) for comp in as_sequence(components)]
                        for key, components in other.items()}
        elif isinstance(other, collections.Sequence):
            children = {TrancludeMarker.root: [as_transclusion(t, v) for v in other]}
        elif isinstance(other, new_type):
            children = {TrancludeMarker.root: [as_transclusion(t, other)]}
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
