###########
weather-nlp
###########


About
=====
Ask for weather information like a human.


Goals
=====
Understand typical questions like:

- Hourly temperatures in Potsdam on 2020-09-15.
- Rain probability tomorrow in Berlin.
- Will it rain next week?
- Wird es morgen heiss?
- Wird es morgen regnen?
- Ist es morgen regnerisch?


Status
======
This is just a humble evaluation for parsing human-readable sentences into a
structured type in order to be passed on to a weather data acquisition library
like `Wetterdienst`_. Currently, this is not implemented yet.

For the `NLP`_ task, the program evaluates the fine Python libraries `spaCy`_
and `Flair`_.

As this is project is in its early stages, contributions are very welcome.
Specifically, it would be sweet to see tests for languages other than English
or German.


Setup
=====
::

    make setup


Run tests
=========
::

    make test


Usage
=====
::

    source .venv/bin/activate

    # English
    python wq.py Snow depth on Zugspitze
    python wq.py Sunshine in Kharagpur
    python wq.py Rain in Chengdu
    python wq.py Temperature in Nanchang
    python wq.py Particulates in Stuttgart on 2020-09-17
    python wq.py hourly temperatures in Potsdam on 2020-09-15
    python wq.py maximum temperature in Munich tomorrow
    python wq.py Tell me the weather in Tokyo, Japan on the 6th January 1975.
    python wq.py What will the weather be in London, England next Wednesday?
    python wq.py What was the weather in Washington,DC last 4th July?

    # German
    python wq.py Sonnenschein auf Helgoland
    python wq.py Ozonwerte in Freiburg
    python wq.py Nebel im Taunus
    python wq.py Feinstaub in Stuttgart am 17.09.2020
    python wq.py Stuendliche Temperaturen in Berlin, gestern um 23:00 Uhr
    python wq.py Berliner Temperaturen um 11:00 Uhr
    python wq.py Taegliche Berliner Temperaturen im Juli
    python wq.py Berliner Tagestemperatur um 11:00 Uhr
    python wq.py Berliner Tagestemperaturen um 11:00 Uhr

    # Chinese
    python wq.py 成都的雨
    python wq.py 南昌的温度
    python wq.py 南昌明天的温度
    python wq.py 2020年9月17日南昌市的温度

    # Hindi
    python wq.py खड़गपुर में बारिश
    python wq.py खड़गपुर में धूप
    python wq.py कल खड़गपुर में धूप
    python wq.py 2020-09-17 को खड़गपुर में धूप


Other implementations
=====================

The article `How to find weather data using NLP (Natural Language Processing)`_
by Andrew Wigmore of `Visual Crossing Corporation`_ describes how to use
`Natural language processing`_ (NLP) to create a sample Java application that
can find weather data using "natural language" text questions. This allows
users to find weather data using queries such as:

- Tell me the weather in Tokyo, Japan on the 6th January 1975.
- What will the weather be in London, England next Wednesday?
- What was the weather in Washington,DC last 4th July?

It is based on `Stanford CoreNLP`_. Find the code example at
`NLPWeatherDataSample.java`_.



.. _Flair: https://pypi.org/project/flair/
.. _How to find weather data using NLP (Natural Language Processing): https://www.visualcrossing.com/resources/documentation/weather-api/how-to-find-weather-data-using-nlp/
.. _Natural language processing: https://en.wikipedia.org/wiki/Natural_language_processing
.. _NLP: https://en.wikipedia.org/wiki/Natural_language_processing
.. _NLPWeatherDataSample.java: https://github.com/visualcrossing/WeatherApi/blob/master/Java/com/visualcrossing/weather/samples/NLPWeatherDataSample.java
.. _spaCy: https://pypi.org/project/spacy/
.. _Stanford CoreNLP: https://stanfordnlp.github.io/CoreNLP/
.. _Visual Crossing Corporation: https://github.com/visualcrossing
.. _Wetterdienst: https://github.com/earthobservations/wetterdienst
