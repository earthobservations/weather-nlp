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

For the NLP task, the program evaluates the fine Python libraries `spaCy`_ and
`Flair`_.

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


.. _Flair: https://pypi.org/project/flair/
.. _spaCy: https://pypi.org/project/spacy/
.. _Wetterdienst: https://github.com/earthobservations/wetterdienst
