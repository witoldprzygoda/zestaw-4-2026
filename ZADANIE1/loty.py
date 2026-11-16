"""
Zadanie 1 - pobieranie stanow samolotow z OpenSky Network (REST API, bez konta)
oraz wykres wysokosci w funkcji predkosci.
"""

import math

import matplotlib.pyplot as plt
import pandas as pd
import requests
from matplotlib.colors import TwoSlopeNorm  # noqa: F401 (przyda sie w rysuj)

URL = "https://opensky-network.org/api/states/all"
PROMIEN_KM = 100
STOPIEN_KM = 111.2  # dlugosc luku 1 stopnia poludnika (szerokosci geograficznej) w km

# punkty odniesienia lotnisk (szerokosc, dlugosc geograficzna w stopniach)
LOTNISKA = {
    "KRK": {"nazwa": "Kraków-Balice", "lat": 50.0777, "lon": 19.7848},
    "KTW": {"nazwa": "Katowice-Pyrzowice", "lat": 50.4743, "lon": 19.0800},
    "WAW": {"nazwa": "Warszawa-Okęcie", "lat": 52.1657, "lon": 20.9671},
    "GDN": {"nazwa": "Gdańsk", "lat": 54.3776, "lon": 18.4662},
    "FRA": {"nazwa": "Frankfurt nad Menem", "lat": 50.0333, "lon": 8.5706},
    "AMS": {"nazwa": "Amsterdam-Schiphol", "lat": 52.3105, "lon": 4.7683},
    "LHR": {"nazwa": "Londyn-Heathrow", "lat": 51.4700, "lon": -0.4543},
    "ATL": {"nazwa": "Atlanta", "lat": 33.6407, "lon": -84.4277},
}

# kody ICAO wybranych linii lotniczych (pierwsze trzy litery znaku wywolawczego)
LINIE_LOTNICZE = {
    "AFR": "Air France", "AUA": "Austrian", "BAW": "British Airways", "BEL": "Brussels Airlines",
    "CFG": "Condor", "CLH": "Lufthansa CityLine", "DAL": "Delta", "DLA": "Air Dolomiti",
    "DLH": "Lufthansa", "EJU": "easyJet Europe", "ENT": "Enter Air", "EWG": "Eurowings",
    "EXS": "Jet2", "EZY": "easyJet", "KLM": "KLM", "LOT": "LOT", "QTR": "Qatar Airways",
    "RYR": "Ryanair", "SWR": "Swiss", "THY": "Turkish Airlines", "UAE": "Emirates",
    "AAL": "American Airlines", "UAL": "United", "SWA": "Southwest", "WZZ": "Wizz Air",
    "TVS": "Smartwings", "GEC": "Lufthansa Cargo", "BCS": "DHL", "FDX": "FedEx",
    "OCN": "Discover Airlines", "LHX": "Lufthansa City", "SXS": "SunExpress", "TUI": "TUIfly",
}

# kolejnosc pol w odpowiedzi OpenSky (indeksy 0..16)
KOLUMNY_OPENSKY = ["icao24", "callsign", "origin_country", "time_position", "last_contact",
                   "lon", "lat", "baro_altitude", "on_ground", "velocity", "true_track",
                   "vertical_rate", "sensors", "geo_altitude", "squawk", "spi", "position_source"]

# kolumny zapisywane w bazie danych
KOLUMNY_BAZY = ["icao24", "callsign", "origin_country", "lon", "lat", "baro_altitude", "on_ground",
                "velocity", "true_track", "vertical_rate", "geo_altitude", "czas_pobrania"]


def obszar(lat, lon, km):
    """
    Prostokat wspolrzednych wokol punktu (lat, lon) w odleglosci km na polnoc, poludnie, wschod i zachod.
    Zwraca slownik {"lamin": ..., "lomin": ..., "lamax": ..., "lomax": ...}, wartosci zaokraglone do 4 miejsc.
    """
    pass


def pobierz(kod_lotniska, km=PROMIEN_KM):
    """
    Aktualne stany samolotow w obszarze wokol lotniska (zapytanie bez logowania).
    Zwraca DataFrame z kolumnami KOLUMNY_BAZY; callsign bez spacji na koncu,
    czas_pobrania to pole "time" odpowiedzi (czas uniksowy).
    """
    # TODO: requests.get(URL, params=..., timeout=...), odpowiedz.json(), DataFrame z pola "states"
    pass


def rysuj(df, plik_png, tytul):
    """
    Wykres punktowy: predkosc [km/h] na osi X (0-1200), wysokosc geo_altitude [km] na osi Y (0-14),
    kolor punktu: predkosc pionowa vertical_rate [m/s] (mapa kolorow "coolwarm", 0 w srodku skali),
    pasek kolorow z opisem. Zapis do pliku plik_png, bez plt.show().
    """
    pass
