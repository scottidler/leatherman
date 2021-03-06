#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import deepcopy


class MergeError(Exception):
    def __init__(self, message):
        super(MergeError, self).__init__(message)


class DictDoesntHaveHeadError(Exception):
    def __init__(self, d):
        keys = list(d.keys())
        message = f"dictionary.keys(): {keys} does not have a single key to be considered a head"
        super(DictDoesntHaveHeadError, self).__init__(message)


class NotDictError(Exception):
    def __init__(self, o):
        t = type(o)
        message = f"{o} is {t}, not a dict as required"
        super(NotDictError, self).__init__(message)


def dict_to_attrs(obj, d):
    for k, v in d.items():
        setattr(obj, k, v)
    return obj


def update(d1, d2):
    d1.update(d2)
    return d1


def isstr(obj):
    return isinstance(obj, str)


def isint(obj):
    return isinstance(obj, int)


def isfloat(obj):
    return isinstance(obj, float)


def isscalar(obj):
    return (obj is None) or isstr(obj) or isint(obj) or isfloat(obj)


def _merge(obj1, obj2):
    """merges obj2 into obj1 and return merged result

    NOTE: tuples and arbitrary objects are not handled as it is totally
    ambiguous what should happen"""
    key = None
    result = deepcopy(obj1)
    try:
        if isscalar(result):
            result = obj2
        elif isinstance(result, list):
            if isinstance(obj2, list):
                result.extend(obj2)
            else:
                result.append(obj2)
        elif isinstance(result, dict):
            if isinstance(obj2, dict):
                for key in obj2:
                    if key in result:
                        result[key] = _merge(result[key], obj2[key])
                    else:
                        result[key] = obj2[key]
            else:
                raise MergeError(
                    'Cannot merge non-dict "%s" into dict "%s"' % (obj2, result)
                )
        else:
            raise MergeError('NOT IMPLEMENTED "%s" into "%s"' % (obj2, result))
    except TypeError as e:
        raise MergeError(
            f'TypeError "{e}" in key "{key}" when merging "{obj2}" into "{result}"'
        )
    return result


def merge(*objs):
    if len(objs) == 0:
        return {}
    elif len(objs) == 1:
        return objs[0]
    result = objs[0]
    for obj in objs[1:]:
        result = _merge(result, obj)
    return result


def head(d):
    if not isinstance(d, dict):
        raise NotDictError(d)
    keys = list(d.keys())
    if len(keys) == 1:
        return keys[0]
    raise DictDoesntHaveHeadError(d)


def body(d):
    return d[head(d)]


def head_body(d):
    head_ = head(d)
    return head_, d[head_]


def keys_ending(d, suffix):
    return [k for k in d.keys() if k.endswith(suffix)]


def dictify(items, sep=":"):
    result = {}
    if items:
        for item in items:
            key, value = item.split(sep)
            result[key] = result.get(key, []) + [value]
    return result
