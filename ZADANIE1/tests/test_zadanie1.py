import json
import math
import os
import re
import sqlite3

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
import pytest  # noqa: E402
import schedule  # noqa: E402

import ZADANIE1.main as program  # noqa: E402
from ZADANIE1 import baza, loty  # noqa: E402

# prawdziwa odpowiedz OpenSky: okolice lotniska FRA, 55 samolotow
PROBKA = os.path.join(os.path.dirname(__file__), "opensky_probka.json")


class FalszywaOdpowiedz:
    def __init__(self, dane):
        self.dane = dane

    def json(self):
        return self.dane

    def raise_for_status(self):
        pass


@pytest.fixture
def odpowiedz():
    with open(PROBKA, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def zapytania(monkeypatch, odpowiedz):
    """Zastepuje requests.get atrapa i zapamietuje argumenty wywolan."""
    wywolania = []

    def falszywe_get(url, *args, **kwargs):
        wywolania.append((url, args, kwargs))
        return FalszywaOdpowiedz(odpowiedz)

    monkeypatch.setattr(loty.requests, "get", falszywe_get)
    return wywolania


@pytest.fixture
def plik_bazy(tmp_path):
    return str(tmp_path / "test.db")


def wiersz(icao24, callsign, velocity, geo_altitude, vertical_rate=0.0, on_ground=False, czas=100):
    return {"icao24": icao24, "callsign": callsign, "origin_country": "Poland", "lon": 19.8, "lat": 50.1,
            "baro_altitude": geo_altitude, "on_ground": on_ground, "velocity": velocity, "true_track": 90.0,
            "vertical_rate": vertical_rate, "geo_altitude": geo_altitude, "czas_pobrania": czas}


# ---------------------------------------------------------------- loty.py

def test_lotniska():
    for kod in ("KRK", "WAW", "FRA", "ATL"):
        assert {"nazwa", "lat", "lon"} <= set(loty.LOTNISKA[kod])


def test_obszar():
    assert loty.obszar(50.0, 20.0, 111.2) == {"lamin": 49.0, "lomin": 18.4443, "lamax": 51.0, "lomax": 21.5557}
    rownik = loty.obszar(0.0, 0.0, 55.6)
    assert rownik == {"lamin": -0.5, "lomin": -0.5, "lamax": 0.5, "lomax": 0.5}


def test_pobierz_zapytanie(zapytania):
    loty.pobierz("FRA")
    assert len(zapytania) == 1
    url, args, kwargs = zapytania[0]
    assert url == "https://opensky-network.org/api/states/all"
    lotnisko = loty.LOTNISKA["FRA"]
    assert kwargs.get("params") == loty.obszar(lotnisko["lat"], lotnisko["lon"], 100), "Obszar w parametrze params"
    assert kwargs.get("timeout"), "Zapytanie z limitem czasu (timeout)"


def test_pobierz_tabela(zapytania, odpowiedz):
    df = loty.pobierz("FRA")
    assert list(df.columns) == loty.KOLUMNY_BAZY
    assert len(df) == 55
    assert df["callsign"].iloc[0] == "CFG1CD", "Znak wywolawczy bez spacji na koncu"
    assert (df["czas_pobrania"] == odpowiedz["time"]).all()
    assert df["icao24"].iloc[0] == odpowiedz["states"][0][0]


def test_pobierz_brak_samolotow(monkeypatch):
    monkeypatch.setattr(loty.requests, "get", lambda *a, **k: FalszywaOdpowiedz({"time": 1, "states": None}))
    df = loty.pobierz("KRK")
    assert df.empty
    assert list(df.columns) == loty.KOLUMNY_BAZY


def test_rysuj(tmp_path, monkeypatch):
    monkeypatch.setattr(plt, "show", lambda *a, **k: pytest.fail("Bez plt.show() w funkcji rysuj"))
    df = pd.DataFrame([wiersz("a", "DLH1", 230.0, 11000.0, 0.0), wiersz("b", "RYR2", 120.0, 2500.0, -6.0)])
    plik = tmp_path / "wykres.png"
    loty.rysuj(df, str(plik), "test")
    assert plik.stat().st_size > 10_000


# ---------------------------------------------------------------- baza.py

def test_utworz_tabele(plik_bazy):
    baza.utworz_tabele(plik_bazy)
    with sqlite3.connect(plik_bazy) as polaczenie:
        kolumny = polaczenie.execute("PRAGMA table_info(samoloty)").fetchall()
    assert [k[1] for k in kolumny] == loty.KOLUMNY_BAZY
    typy = {k[1]: k[2] for k in kolumny}
    assert typy["velocity"] == "REAL" and typy["geo_altitude"] == "REAL" and typy["icao24"] == "TEXT"
    assert typy["czas_pobrania"] == "INTEGER"


def test_utworz_tabele_od_nowa(plik_bazy):
    df = pd.DataFrame([wiersz("a", "DLH1", 200.0, 9000.0)])
    baza.utworz_tabele(plik_bazy)
    baza.zapisz(df, plik_bazy)
    baza.utworz_tabele(plik_bazy)
    assert len(baza.wczytaj(plik_bazy)) == 1, "Bez od_nowa dane zostaja"
    baza.utworz_tabele(plik_bazy, od_nowa=True)
    assert len(baza.wczytaj(plik_bazy)) == 0, "od_nowa=True: pusta tabela"


def test_zapisz_i_wczytaj(plik_bazy, zapytania):
    df = loty.pobierz("FRA")
    baza.utworz_tabele(plik_bazy)
    baza.zapisz(df, plik_bazy)
    baza.zapisz(df, plik_bazy)
    wynik = baza.wczytaj(plik_bazy)
    assert len(wynik) == 110
    assert list(wynik.columns) == loty.KOLUMNY_BAZY
    assert wynik["velocity"].dtype.kind == "f"


def test_najszybsze_pomiary(plik_bazy):
    df = pd.DataFrame([
        wiersz("a", "DLH1", 150.0, 3000.0, 8.0, czas=1),
        wiersz("a", "DLH1", 210.0, 6000.0, 5.0, czas=2),    # najszybszy pomiar samolotu a
        wiersz("a", "DLH1", 180.0, 4500.0, 6.0, czas=3),
        wiersz("b", "RYR7", 120.0, 1500.0, -4.0),
        wiersz("c", "LOT3", 10.0, 120.0, 0.0, on_ground=True),   # na ziemi
        wiersz("d", "WZZ5", None, 8000.0, 0.0),                  # brak predkosci
    ])
    baza.utworz_tabele(plik_bazy)
    baza.zapisz(df, plik_bazy)
    wynik = baza.najszybsze_pomiary(plik_bazy).sort_values("icao24").reset_index(drop=True)
    assert list(wynik["icao24"]) == ["a", "b"]
    assert list(wynik["velocity"]) == [210.0, 120.0]
    assert list(wynik["geo_altitude"]) == [6000.0, 1500.0], "Wysokosc z tego samego pomiaru co predkosc"
    assert {"icao24", "velocity", "geo_altitude", "vertical_rate"} <= set(wynik.columns)


def test_linie_lotnicze(plik_bazy):
    df = pd.DataFrame([
        wiersz("a", "DLH1", 200.0, 9000.0), wiersz("a", "DLH1", 210.0, 9000.0),   # ten sam samolot dwa razy
        wiersz("b", "DLH4AB", 200.0, 9000.0), wiersz("c", "DLH77", 200.0, 9000.0),
        wiersz("d", "RYR123", 200.0, 9000.0), wiersz("e", "RYR9K", 200.0, 9000.0),
        wiersz("f", "LOT3", 200.0, 9000.0),
        wiersz("g", "N464DA", 200.0, 9000.0), wiersz("h", "DEIAB", 200.0, 9000.0),   # nie linie lotnicze
        wiersz("i", "JOKER31", 200.0, 9000.0), wiersz("j", "", 200.0, 9000.0),
    ])
    baza.utworz_tabele(plik_bazy)
    baza.zapisz(df, plik_bazy)
    assert baza.linie_lotnicze(plik_bazy) == [("DLH", 3), ("RYR", 2), ("LOT", 1)]
    assert baza.linie_lotnicze(plik_bazy, ile=1) == [("DLH", 3)]


def test_linie_lotnicze_probka(plik_bazy, zapytania):
    baza.utworz_tabele(plik_bazy)
    baza.zapisz(loty.pobierz("FRA"), plik_bazy)
    assert baza.linie_lotnicze(plik_bazy, ile=3) == [("DLH", 12), ("CFG", 4), ("DLA", 2)]


# ---------------------------------------------------------------- main.py

def test_main(monkeypatch, tmp_path, capsys, zapytania):
    monkeypatch.setattr(program, "PLIK_BAZY", str(tmp_path / "loty.db"))
    monkeypatch.setattr(program, "PLIK_WYKRESU", str(tmp_path / "loty.png"))
    monkeypatch.setattr(program, "POWTORZENIA", 2)
    monkeypatch.setattr(program, "CO_ILE_S", 1)
    try:
        program.main()
    finally:
        schedule.clear()
    out = capsys.readouterr().out
    assert len(zapytania) == 2, "Dwa pobrania danych"
    assert re.search(r"W bazie: 110 pomiarów, 55 różnych samolotów", out)
    assert re.search(r"DLH\s+Lufthansa\s+12", out)
    assert (tmp_path / "loty.png").exists()
