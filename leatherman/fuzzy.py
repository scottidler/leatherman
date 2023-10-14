#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from enum import Enum
from fnmatch import fnmatch
from collections import OrderedDict


class MatchType(Enum):
    EXACT = 0
    IGNORECASE = 1
    PREFIX = 2
    SUFFIX = 3
    CONTAINS = 4
    GLOB = 5
    REGEX = 6


class InvalidFuzzyTypeError(Exception):
    def __init__(self, obj):
        message = f"type(obj)={type(obj)} is not dict or list"
        super(InvalidFuzzyTypeError, self).__init__(message)


MATCH_FUNCS = {
    MatchType.EXACT: lambda item, pattern: pattern == item,
    MatchType.IGNORECASE: lambda item, pattern: pattern.lower() == item.lower(),
    MatchType.PREFIX: lambda item, pattern: item.startswith(pattern),
    MatchType.SUFFIX: lambda item, pattern: item.endswith(pattern),
    MatchType.CONTAINS: lambda item, pattern: pattern in item,
    MatchType.GLOB: lambda item, pattern: fnmatch(item, pattern),
    MatchType.REGEX: lambda item, pattern: re.search(pattern, item),
}

DEFAULT_MATCH_TYPES = [
    MatchType.EXACT,
    MatchType.IGNORECASE,
    MatchType.PREFIX,
    MatchType.CONTAINS,
]


def match_list(item_list, patterns, match_func, key_func, include):
    if include:
        return any([
            any([
                item_func(item)(item, patterns, match_func, key_func, include)
                for item
                in item_list
            ])
            for pattern
            in patterns
        ])
    return all([
        any([
            item_func(item)(item, patterns, match_func, key_func, include)
            for item
            in item_list
        ])
        for pattern
        in patterns
    ])


def match_item(item, patterns, match_func, key_func, include):
    item_string = key_func(item)
    if include:
        return any([
            match_func(item_string, pattern)
            for pattern
            in patterns
        ])
    return all([
        not match_func(item_string, pattern)
        for pattern
        in patterns
    ])


def match_dict(item_dict, patterns, match_func, include):
    raise NotImplementedError("This function is not yet implemented.")


def item_func(item):
    return {
        'list': match_list,
        'tuple': match_list,
        'dict': match_dict,
    }.get(item.__class__.__name__, match_item)


def match_items(items, patterns, match_types, key_func=str, include=True):
    if '*' in patterns:
        return items
    for match_type in match_types:
        if match_type not in MATCH_FUNCS:
            raise ValueError(f"Invalid match type: {match_type}")
        results = [
            item
            for item
            in items
            if item_func(item)(item, patterns, MATCH_FUNCS[match_type], key_func, include)
        ]
        if results:
            return results
    return []


class FuzzyTuple(tuple):
    def __init__(self, *args, key_func=str, match_types=None, **kwargs):
        self._type = type(args[0])
        self._key_func = key_func
        self._match_types = match_types or DEFAULT_MATCH_TYPES


    def include(self, *patterns, match_types=None):
        items = match_items(
            [item for item in self.__iter__()],
            patterns,
            match_types or self._match_types,
            key_func=self._key_func,
            include=True,
        )
        return FuzzyTuple(items, key_func=self._key_func, match_types=match_types or self._match_types)


    def exclude(self, *patterns, match_types=None):
        items = match_items(
            [item for item in self.__iter__()],
            patterns,
            match_types or self._match_types,
            key_func=self._key_func,
            include=False,
        )
        return FuzzyTuple(items, key_func=self._key_func, match_types=match_types or self._match_types)


    def defuzz(self):
        return tuple(item for item in self.__iter__())


    def __repr__(self):
        return repr(tuple(self))


class FuzzyList(list):
    def __init__(self, *args, key_func=str, match_types=None, **kwargs):
        self._type = type(args[0])
        self._key_func = key_func
        self._match_types = match_types or DEFAULT_MATCH_TYPES
        super().__init__(*args, **kwargs)


    def include(self, *patterns, match_types=None):
        items = match_items(
            [item for item in self.__iter__()],
            patterns,
            match_types or self._match_types,
            key_func=self._key_func,
            include=True,
        )
        return FuzzyList(items, key_func=self._key_func, match_types=match_types or self._match_types)


    def exclude(self, *patterns, match_types=None):
        items = match_items(
            [item for item in self.__iter__()],
            patterns,
            match_types or self._match_types,
            key_func=self._key_func,
            include=False,
        )
        return FuzzyList(items, key_func=self._key_func, match_types=match_types or self._match_types)


    def defuzz(self):
        return [item for item in self.__iter__()]


class FuzzyDict(OrderedDict):
    def __init__(self, *args, key_func=str, match_types=None, **kwargs):
        self._type = type(args[0])
        self._key_func = key_func
        self._match_types = match_types or DEFAULT_MATCH_TYPES
        for key in args[0].keys():
            if not isinstance(key, str):
                raise TypeError(f"All keys must be strings. Found key of type {type(key).__name__}")
        super().__init__(*args, **kwargs)


    def include(self, *patterns, match_types=None):
        items = match_items(
            self.keys(), patterns, match_types or self._match_types, key_func=self._key_func, include=True
        )
        return FuzzyDict({item: self.get(item) for item in items}, key_func=self._key_func, match_types=match_types or self._match_types)


    def exclude(self, *patterns, match_types=None):
        items = match_items(
            self.keys(), patterns, match_types or self._match_types, key_func=self._key_func, include=False
        )
        return FuzzyDict({item: self.get(item) for item in items}, key_func=self._key_func, match_types=match_types or self._match_types)


    def defuzz(self):
        if self._type.__name__ == 'dict':
            return dict(self.items())
        elif self._type.__name__ == 'collections.OrderedDict':
            return OrderedDict(self.items())
        raise Exception(f"unknown type: {self._type}")


def fuzzy(obj, key_func=str, match_types=None):
    if isinstance(obj, tuple):
        return FuzzyTuple(obj, key_func=key_func, match_types=match_types)
    elif isinstance(obj, list):
        return FuzzyList(obj, key_func=key_func, match_types=match_types)
    elif isinstance(obj, dict):
        return FuzzyDict(obj, key_func=key_func, match_types=match_types)
    raise InvalidFuzzyTypeError(obj)


if __name__ == "__main__":
    f = fuzzy(["a", "b"])
    print(f"f={f}")
