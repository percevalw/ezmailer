from lxml import etree


class TrancludeMarker:
    prefix = "TRANSCLUDE"
    root = '__root__'

    def __init__(self, key=None):
        self.key = key or TrancludeMarker.root

    def __str__(self):
        return "<{} id=\"{}\" key=\"{}\"/>".format(TrancludeMarker.prefix, id(self), self.key)


class Component:
    def __init__(self, text):
        self.tree = etree.fromstring(text)
        markers = self.tree.findall('.//{}'.format(TrancludeMarker.prefix))
        self.transclude_markers = {}
        for marker in markers:
            key = marker.get("key")
            if key in self.transclude_markers:
                raise Exception("Keys must be unique in component definition, {} is not".format(key))
            self.transclude_markers[key] = marker

    def transclude(self, **replacements):
        for key, replacement in replacements.items():
            if not key in self.transclude_markers:
                raise Exception("Component '{}' has no transclusion parameter {}".format(type(self), key))
            marker = self.transclude_markers[key]
            if not isinstance(replacement, list):
                replacement = [replacement]
            for element in replacement:
                marker.addnext(element.tree)
            marker.getparent().remove(marker)