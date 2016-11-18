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
        self.transclude_markers = self.tree.findall('.//{}'.format(TrancludeMarker.prefix))

    def transclude(self, replacements):
        if not isinstance(replacements, list):
            replacements = [replacements]
        for marker, replacement in zip(self.transclude_markers, replacements):
            if not isinstance(replacement, list):
                replacement = [replacement]
            for element in replacement:
                marker.addnext(element.tree)
            marker.getparent().remove(marker)