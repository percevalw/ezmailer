import collections

def as_sequence(obj):
    if isinstance(obj, collections.Sequence):
        return obj
    return [obj]


def collection_values(obj):
    return obj.values() if isinstance(obj, collections.Mapping) else obj
