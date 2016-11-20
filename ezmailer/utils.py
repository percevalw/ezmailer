import collections

def as_sequence(obj):
    if isinstance(obj, collections.Sequence):
        return obj
    return [obj]


def collection_values(obj):
    return obj.values() if isinstance(obj, collections.Mapping) else obj


def dict_to_attr(d):
    return " ".join('{}="{}"'.format(key, value)
                    for key, value in d.items()
                    if value is not None)


def make_tag(tag_name, dict_attr, content=""):
    return "<{tag_name} {attr}>{content}</{tag_name}>".format(
        tag_name=tag_name,
        attr=dict_to_attr(dict_attr),
        content=str(content)
    )