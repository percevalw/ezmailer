import collections

from lxml import etree

import six
from ezmailer._cmp_syntax import USE_CMP_SYNTAX
from ezmailer.utils import as_sequence
from .transclusion import Transclusion


def add_transclusion_operator(cls, transclusion_cls):
    new_dict = dict(cls.__dict__)

    def as_transclusion(obj, parent=None):
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
        print(self, other)
        t = self.get_or_create_transclusion()
        if isinstance(other, collections.Mapping):
            children = {key: [as_transclusion(comp, t) for comp in as_sequence(components)]
                        for key, components in other.items()}
        elif isinstance(other, collections.Sequence) and not isinstance(other, six.string_types):
            children = {TrancludeMarker.root: [as_transclusion(v, t) for v in other]}
        elif isinstance(other, new_type):
            children = {TrancludeMarker.root: [as_transclusion(other, t)]}
        elif isinstance(other, Transclusion):
            other.parent = t
            children = {TrancludeMarker.root: [other]}
        elif isinstance(other, six.string_types):
            children = {TrancludeMarker.root: [as_transclusion(TextComponent(other), t)]}
        else:
            raise Exception("Right member in > inclusion must be either a mapping, a sequence or a includable element, not {}".format(repr(other)))
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


class TrancludeMarker:
    prefix = "TRANSCLUDE"
    root = '__root__'

    def __init__(self, key=None):
        self.key = key or TrancludeMarker.root

    def __str__(self):
        return "<{} id=\"{}\" key=\"{}\"/>".format(TrancludeMarker.prefix, id(self), self.key)


class Component:
    def __init__(self):
        pass

    def transclude(self, **replacements):
        raise NotImplementedError()


print("CREATING COMPONENT")

if USE_CMP_SYNTAX[0]:
    print("OK!")
    Component = add_transclusion_operator(Component, Transclusion)


class TextComponent(Component):
    def __init__(self, text):
        super(TextComponent, self).__init__()
        self.text = text

    def transclude(self, **replacements):
        pass

    def __repr__(self):
        return '<{} text="{}">'.format(self.__class__.__name__, self.text)


class TreeComponent(Component):
    def __init__(self, tree):
        super(TreeComponent, self).__init__()
        self.tree = tree
        markers = self.tree.findall('.//{}'.format(TrancludeMarker.prefix))
        self.transclude_markers = {}
        for marker in markers:
            key = marker.get("key")
            if key in self.transclude_markers:
                raise Exception("Keys must be unique in component definition, {} is not".format(key))
            self.transclude_markers[key] = marker

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    @staticmethod
    def fromstring(s):
        return TreeComponent(etree.fromstring(s))

    def transclude(self, **replacements):
        for key, replacement in replacements.items():
            if key not in self.transclude_markers:
                raise Exception("Component '{}' has no transclusion parameter {}".format(type(self), key))
            marker = self.transclude_markers[key]
            if not isinstance(replacement, list):
                replacement = [replacement]
            previous = marker.getprevious()
            for i, element in enumerate(replacement):
                if isinstance(element, TreeComponent):
                    marker.addnext(element.tree)
                    previous = element.tree
                elif isinstance(element, TextComponent):
                    if previous is not None:
                        previous.tail = (previous.tail or "") + element.text
                    else:
                        marker.getparent().text = (marker.getparent().text or "") + element.text
            marker.getparent().remove(marker)
