"""
Zadanie 1 - baza danych SQLite: tabela samoloty, zapis i odczyt (pandas), zapytania SQL.
"""

import sqlite3
from contextlib import closing

import pandas as pd

TABELA = "samoloty"

SQL_TABELA = """
CREATE TABLE IF NOT EXISTS samoloty (
    icao24         TEXT,
    callsign       TEXT,
    origin_country TEXT,
    lon            REAL,
    lat            REAL,
    baro_altitude  REAL,
    on_ground      INTEGER,
    velocity       REAL,
    true_track     REAL,
    vertical_rate  REAL,
    geo_altitude   REAL,
    czas_pobrania  INTEGER
)
"""


def utworz_tabele(plik, od_nowa=False):
    """Tworzy tabele samoloty (jesli jej nie ma); od_nowa=True najpierw usuwa istniejaca tabele."""
    pass


def zapisz(df, plik):
    """Dopisuje wiersze tabeli df do tabeli samoloty."""
    pass


def wczytaj(plik):
    """Cala tabela samoloty jako DataFrame."""
    pass


def najszybsze_pomiary(plik):
    """
    Dla kazdego samolotu w powietrzu (on_ground = 0) jeden pomiar: ten z najwieksza predkoscia.
    Pomijamy wiersze bez velocity, geo_altitude lub vertical_rate.
    Kolumny wyniku: icao24, callsign, velocity, geo_altitude, vertical_rate.
    """
    # TODO: zapytanie SQL (GROUP BY, MAX) i pd.read_sql_query()
    pass


def linie_lotnicze(plik, ile=5):
    """
    Linie lotnicze z najwieksza liczba roznych samolotow: lista krotek (kod, liczba), malejaco,
    przy rownej liczbie alfabetycznie. Kod linii to trzy pierwsze litery znaku wywolawczego,
    bierzemy tylko znaki postaci: trzy wielkie litery i cyfra (np. DLH4AB, RYR1234).
    """
    # TODO: zapytanie SQL z parametrem ? w LIMIT, wynik: kursor.fetchall()
    pass
