# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas.motl@panodata.org>
# Distributed under the AGPLv3 License. See LICENSE for more info.

from wq import Result, analyze_spacy


def test_english_wigmore_tokyo():
    result = analyze_spacy(
        "Tell me the weather in Tokyo, Japan on the 6th January 1975."
    )
    assert result == Result(
        where="Tokyo, Japan", when="the 6th January 1975", what="The Weather"
    )


def test_english_wigmore_london():
    result = analyze_spacy(
        "What will the weather be in London, England next Wednesday?"
    )
    assert result == Result(
        where="London, England", when="next Wednesday", what="The Weather"
    )


def test_english_wigmore_washington():
    result = analyze_spacy("What was the weather in Washington,DC last 4th July?")
    assert result == Result(
        where="Washington,DC", when="last 4th July", what="The Weather"
    )
