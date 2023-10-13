#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from leatherman.fuzzy import *


def test_match_type_enum():
    print("Testing MatchType Enum...")
    assert MatchType.EXACT.value == 0
    assert MatchType.IGNORECASE.value == 1
    assert MatchType.PREFIX.value == 2
    assert MatchType.SUFFIX.value == 3
    assert MatchType.CONTAINS.value == 4
    assert MatchType.GLOB.value == 5
    assert MatchType.REGEX.value == 6
    print("MatchType Enum test passed.")


def test_match_list():
    print("Testing match_list function...")
    assert match_list(["apple", "banana"], ["apple"], MATCH_FUNCS[MatchType.EXACT], str, True) == True
    assert match_list(["apple", "banana"], ["mango"], MATCH_FUNCS[MatchType.EXACT], str, True) == False
    print("match_list function test passed.")


def test_match_item():
    print("Testing match_item function...")
    assert match_item("apple", ["apple"], MATCH_FUNCS[MatchType.EXACT], str, True) == True
    assert match_item("apple", ["mango"], MATCH_FUNCS[MatchType.EXACT], str, True) == False
    print("match_item function test passed.")


def test_match_items():
    print("Testing match_items function...")
    assert match_items(["apple", "banana"], ["apple"], [MatchType.EXACT], str, True) == ["apple"]
    assert match_items(["apple", "banana"], ["mango"], [MatchType.EXACT], str, True) == []
    print("match_items function test passed.")


def test_empty_patterns():
    print("Testing empty patterns...")
    f = fuzzy(["apple", "banana"])
    result = f.include("", match_types=[MatchType.EXACT])
    assert result.defuzz() == []
    print("Empty patterns test passed.")


def test_item_func():
    print("Testing item_func function...")
    assert item_func([]) == match_list
    assert item_func({}) == match_dict
    assert item_func("string") == match_item
    print("item_func function test passed.")


def test_invalid_fuzzy_type_error():
    print("Testing InvalidFuzzyTypeError...")
    with pytest.raises(InvalidFuzzyTypeError):
        fuzzy(42)
    print("InvalidFuzzyTypeError test passed.")


def test_fuzzy_tuple_include_exact():
    print("Testing FuzzyTuple include with EXACT match...")
    f = fuzzy(("apple", "banana", "cherry"))
    result = f.include("apple", match_types=[MatchType.EXACT])
    assert result.defuzz() == ("apple",)
    print("FuzzyTuple include with EXACT match test passed.")


def test_fuzzy_tuple_include_ignorecase():
    print("Testing FuzzyTuple include with IGNORECASE match...")
    f = fuzzy(("apple", "banana", "cherry"))
    result = f.include("APPLE", match_types=[MatchType.IGNORECASE])
    assert result.defuzz() == ("apple",)
    print("FuzzyTuple include with IGNORECASE match test passed.")


def test_fuzzy_tuple_include_prefix():
    print("Testing FuzzyTuple include with PREFIX match...")
    f = fuzzy(("apple", "banana", "cherry"))
    result = f.include("app", match_types=[MatchType.PREFIX])
    assert result.defuzz() == ("apple",)
    print("FuzzyTuple include with PREFIX match test passed.")


def test_fuzzy_tuple_include_suffix():
    print("Testing FuzzyTuple include with SUFFIX match...")
    f = fuzzy(("apple", "banana", "cherry"))
    result = f.include("ana", match_types=[MatchType.SUFFIX])
    assert result.defuzz() == ("banana",)
    print("FuzzyTuple include with SUFFIX match test passed.")


def test_fuzzy_tuple_include_contains():
    print("Testing FuzzyTuple include with CONTAINS match...")
    f = fuzzy(("apple", "banana", "cherry"))
    result = f.include("ana", match_types=[MatchType.CONTAINS])
    assert result.defuzz() == ("banana",)
    print("FuzzyTuple include with CONTAINS match test passed.")


def test_fuzzy_tuple_include_glob():
    print("Testing FuzzyTuple include with GLOB match...")
    f = fuzzy(("apple", "banana", "cherry"))
    result = f.include("*a*", match_types=[MatchType.GLOB])
    assert result.defuzz() == ("apple", "banana")


def test_fuzzy_tuple_include_regex():
    print("Testing FuzzyTuple include with REGEX match...")
    f = fuzzy(("apple", "banana", "cherry"))
    result = f.include("a.*e", match_types=[MatchType.REGEX])
    assert result.defuzz() == ("apple",)
    print("FuzzyTuple include with REGEX match test passed.")


def test_fuzzy_list_exclude_exact():
    f = fuzzy(["apple", "banana", "cherry"])
    result = f.exclude("apple", match_types=[MatchType.EXACT])
    assert result.defuzz() == ["banana", "cherry"]


def test_fuzzy_list_exclude_ignorecase():
    f = fuzzy(["apple", "banana", "cherry"])
    result = f.exclude("APPLE", match_types=[MatchType.IGNORECASE])
    assert result.defuzz() == ["banana", "cherry"]


def test_fuzzy_list_exclude_prefix():
    f = fuzzy(["apple", "banana", "cherry"])
    result = f.exclude("app", match_types=[MatchType.PREFIX])
    assert result.defuzz() == ["banana", "cherry"]


def test_fuzzy_list_exclude_suffix():
    f = fuzzy(["apple", "banana", "cherry"])
    result = f.exclude("ana", match_types=[MatchType.SUFFIX])
    assert result.defuzz() == ["apple", "cherry"]


def test_fuzzy_list_exclude_contains():
    f = fuzzy(["apple", "banana", "cherry"])
    result = f.exclude("ana", match_types=[MatchType.CONTAINS])
    assert result.defuzz() == ["apple", "cherry"]


def test_fuzzy_list_exclude_glob():
    f = fuzzy(["apple", "banana", "cherry"])
    result = f.exclude("*a*", match_types=[MatchType.GLOB])
    assert result.defuzz() == ["cherry"]


def test_fuzzy_list_exclude_regex():
    f = fuzzy(["apple", "banana", "cherry"])
    result = f.exclude("a.*e", match_types=[MatchType.REGEX])
    assert result.defuzz() == ["banana", "cherry"]


def test_fuzzy_tuple_exclude_exact():
    print("Testing FuzzyTuple exclude with EXACT match...")
    f = fuzzy(("apple", "banana", "cherry"))
    result = f.exclude("apple", match_types=[MatchType.EXACT])
    assert result.defuzz() == ("banana", "cherry")
    print("FuzzyTuple exclude with EXACT match test passed.")


def test_fuzzy_tuple_exclude_ignorecase():
    print("Testing FuzzyTuple exclude with IGNORECASE match...")
    f = fuzzy(("apple", "banana", "cherry"))
    result = f.exclude("APPLE", match_types=[MatchType.IGNORECASE])
    assert result.defuzz() == ("banana", "cherry")
    print("FuzzyTuple exclude with IGNORECASE match test passed.")


def test_fuzzy_tuple_exclude_prefix():
    print("Testing FuzzyTuple exclude with PREFIX match...")
    f = fuzzy(("apple", "banana", "cherry"))
    result = f.exclude("app", match_types=[MatchType.PREFIX])
    assert result.defuzz() == ("banana", "cherry")
    print("FuzzyTuple exclude with PREFIX match test passed.")


def test_fuzzy_dict_include_exact():
    f = fuzzy({"apple": 1, "banana": 2, "cherry": 3})
    result = f.include("apple", match_types=[MatchType.EXACT])
    assert result.defuzz() == {"apple": 1}


def test_fuzzy_dict_include_ignorecase():
    f = fuzzy({"apple": 1, "banana": 2, "cherry": 3})
    result = f.include("APPLE", match_types=[MatchType.IGNORECASE])
    assert result.defuzz() == {"apple": 1}


def test_fuzzy_dict_include_prefix():
    f = fuzzy({"apple": 1, "banana": 2, "cherry": 3})
    result = f.include("app", match_types=[MatchType.PREFIX])
    assert result.defuzz() == {"apple": 1}


def test_fuzzy_dict_include_suffix():
    f = fuzzy({"apple": 1, "banana": 2, "cherry": 3})
    result = f.include("ana", match_types=[MatchType.SUFFIX])
    assert result.defuzz() == {"banana": 2}


def test_fuzzy_dict_include_contains():
    f = fuzzy({"apple": 1, "banana": 2, "cherry": 3})
    result = f.include("ana", match_types=[MatchType.CONTAINS])
    assert result.defuzz() == {"banana": 2}


def test_fuzzy_dict_include_glob():
    f = fuzzy({"apple": 1, "banana": 2, "cherry": 3})
    result = f.include("*a*", match_types=[MatchType.GLOB])
    assert result.defuzz() == {"apple": 1, "banana": 2}


def test_fuzzy_dict_include_regex():
    f = fuzzy({"apple": 1, "banana": 2, "cherry": 3})
    result = f.include("a.*e", match_types=[MatchType.REGEX])
    assert result.defuzz() == {"apple": 1}


def test_fuzzy_dict_exclude_exact():
    f = fuzzy({"apple": 1, "banana": 2, "cherry": 3})
    result = f.exclude("apple", match_types=[MatchType.EXACT])
    assert result.defuzz() == {"banana": 2, "cherry": 3}


def test_fuzzy_dict_exclude_ignorecase():
    f = fuzzy({"apple": 1, "banana": 2, "cherry": 3})
    result = f.exclude("APPLE", match_types=[MatchType.IGNORECASE])
    assert result.defuzz() == {"banana": 2, "cherry": 3}


def test_fuzzy_dict_exclude_prefix():
    f = fuzzy({"apple": 1, "banana": 2, "cherry": 3})
    result = f.exclude("app", match_types=[MatchType.PREFIX])
    assert result.defuzz() == {"banana": 2, "cherry": 3}


def test_fuzzy_dict_exclude_suffix():
    f = fuzzy({"apple": 1, "banana": 2, "cherry": 3})
    result = f.exclude("ana", match_types=[MatchType.SUFFIX])
    assert result.defuzz() == {"apple": 1, "cherry": 3}


def test_fuzzy_dict_exclude_contains():
    f = fuzzy({"apple": 1, "banana": 2, "cherry": 3})
    result = f.exclude("ana", match_types=[MatchType.CONTAINS])
    assert result.defuzz() == {"apple": 1, "cherry": 3}


def test_fuzzy_dict_exclude_glob():
    f = fuzzy({"apple": 1, "banana": 2, "cherry": 3})
    result = f.exclude("*a*", match_types=[MatchType.GLOB])
    assert result.defuzz() == {"cherry": 3}


def test_fuzzy_dict_exclude_regex():
    f = fuzzy({"apple": 1, "banana": 2, "cherry": 3})
    result = f.exclude("a.*e", match_types=[MatchType.REGEX])
    assert result.defuzz() == {"banana": 2, "cherry": 3}


def test_fuzzy_list_empty():
    f = fuzzy([])
    result = f.include("apple", match_types=[MatchType.EXACT])
    assert result.defuzz() == []


def test_fuzzy_list_single_element():
    f = fuzzy(["apple"])
    result = f.include("apple", match_types=[MatchType.EXACT])
    assert result.defuzz() == ["apple"]


def test_fuzzy_list_special_characters():
    f = fuzzy(["apple!", "banana?", "cherry#"])
    result = f.include("apple!", match_types=[MatchType.EXACT])
    assert result.defuzz() == ["apple!"]


def test_fuzzy_list_non_string_elements():
    f = fuzzy([1, 2, 3])
    result = f.include("1", match_types=[MatchType.EXACT])
    assert result.defuzz() == [1]


def test_fuzzy_list_multiple_matching():
    f = fuzzy(["apple", "apple", "banana"])
    result = f.include("apple", match_types=[MatchType.EXACT])
    assert result.defuzz() == ["apple", "apple"]


def test_invalid_match_type():
    f = fuzzy(["apple", "banana"])
    with pytest.raises(ValueError):
        f.include("apple", match_types=["INVALID"])


def test_multiple_patterns():
    f = fuzzy(["apple", "banana", "cherry"])
    result = f.include("apple", "banana", match_types=[MatchType.EXACT])
    assert result.defuzz() == ["apple", "banana"]


def test_chaining():
    f = fuzzy(["apple", "banana", "cherry"])
    result = f.include("apple", match_types=[MatchType.EXACT]).exclude("banana", match_types=[MatchType.EXACT])
    assert result.defuzz() == ["apple"]


def test_custom_key_func():
    f = fuzzy([1, 2, 3], key_func=lambda x: str(x))
    result = f.include("1", match_types=[MatchType.EXACT])
    assert result.defuzz() == [1]


def test_fuzzy_tuple_mixed_types():
    f = fuzzy(("apple", 1))
    result = f.include("apple", match_types=[MatchType.EXACT])
    assert result.defuzz() == ("apple",)


def test_fuzzy_list_mixed_types():
    f = fuzzy(["apple", 1])
    result = f.include("apple", match_types=[MatchType.EXACT])
    assert result.defuzz() == ["apple"]


def test_fuzzy_dict_non_string_keys():
    f = fuzzy({"1": "apple", "2": "banana"})
    result = f.include("1", match_types=[MatchType.EXACT])
    assert result.defuzz() == {"1": "apple"}
