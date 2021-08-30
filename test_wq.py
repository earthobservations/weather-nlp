# -*- coding: utf-8 -*-
# (c) 2020-2021 Andreas Motl <andreas.motl@panodata.org>
# Distributed under the AGPLv3 License. See LICENSE for more info.
import pytest

from wq import Result, analyze_spacy


def test_english_now():
    result = analyze_spacy("Sunshine in Portland")
    assert result == Result(where="Portland", when="now", what="Sunshine")


def test_english_long():
    result = analyze_spacy("hourly temperatures in Potsdam on 2020-09-15")
    assert result == Result(
        where="Potsdam", when="2020-09-15", what="Hourly Temperature"
    )


def test_english_forecast_maxtemp():
    result = analyze_spacy("maximum temperature in munich tomorrow")
    assert result == Result(where="Munich", when="tomorrow", what="Maximum Temperature")


def test_english_forecast_rain():
    result = analyze_spacy("rain probability tomorrow in berlin")
    assert result == Result(where="Berlin", when="tomorrow", what="Rain Probability")


def test_english_snowdepth():
    result = analyze_spacy("snow depth on Zugspitze")
    assert result == Result(where="Zugspitze", when="now", what="Snow Depth")


def test_english_particulates():
    result = analyze_spacy("Particulates in Stuttgart on 2020-09-17")
    assert result == Result(where="Stuttgart", when="2020-09", what="Particulate")


def test_english_city_from_india():
    result = analyze_spacy("Sunshine in Kharagpur")
    assert result == Result(where="Kharagpur", when="now", what="Sunshine")


def test_english_city_from_china():
    result = analyze_spacy("Temperature in Nanchang")
    assert result == Result(where="Nanchang", when="now", what="Temperature")


def test_english_city_without_named_entity():
    result = analyze_spacy("Rain in Chengdu")
    assert result == Result(where="Chengdu", when="now", what="Rain")


def test_german_long():
    result = analyze_spacy("Stuendliche Temperaturen in Berlin, gestern um 23:00 Uhr")
    assert result == Result(
        where="Berlin", when="gestern um 23:00 Uhr", what="Stuendliche Temperatur"
    )


def test_german_location_as_adjective():
    result = analyze_spacy("Berliner Temperaturen um 11:00 Uhr")
    assert result == Result(where="Berliner", when="um 11:00 Uhr", what="Temperatur")


def test_german_regen():
    result = analyze_spacy("Regen in der Deutschen Bucht")
    assert result == Result(where="Deutsche Bucht", when="now", what="Regen")


def test_german_nebel():
    result = analyze_spacy("Nebel im Taunus")
    assert result == Result(where="Taunus", when="now", what="Nebel")


def test_german_sonnenschein():
    result = analyze_spacy("Sonnenschein auf Helgoland")
    assert result == Result(where="Helgoland", when="now", what="Sonnenschein")


def test_german_ozon():
    result = analyze_spacy("Ozonwerte in Freiburg")
    assert result == Result(where="Freiburg", when="now", what="Ozonwerte")


def test_german_particulates():
    result = analyze_spacy("Feinstaub in Stuttgart am 17.09.2020")
    assert result == Result(where="Stuttgart", when="am 17.09.2020", what="Feinstaub")
