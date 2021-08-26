###########
weather-nlp
###########


About
=====
Ask for weather information like a human.


Goals
=====
- Hourly temperatures in Potsdam on 2020-09-15.
- Rain probability tomorrow in Berlin.
- Will it rain next week?
- Wird es morgen heiss?
- Wird es morgen regnen?
- Ist es morgen regnerisch?


Synopsis
========
::

    python wq.py hourly temperatures in Potsdam on 2020-09-15
    python wq.py maximum temperature in Munich tomorrow
    python wq.py snow depth on Zugspitze

    python wq.py Stuendliche Temperaturen in Berlin, gestern um 23:00 Uhr

    python wq.py Berliner Temperaturen um 11:00 Uhr
    python wq.py Taegliche Berliner Temperaturen im Juli
    python wq.py Berliner Tagestemperatur um 11:00 Uhr
    python wq.py Berliner Tagestemperaturen um 11:00 Uhr

    python wq.py Sonnenschein auf Helgoland
    python wq.py Ozonwerte in Freiburg
    python wq.py Nebel im Taunus


Setup
=====
::

    make setup


Run tests
=========
::

    make test
