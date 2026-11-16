"""
Zadanie 1 - program glowny (kompletny): pobieranie danych co CO_ILE_S sekund, POWTORZENIA razy,
zapis do bazy, a na koniec zestawienie i wykres.

Uruchomienie z glownego katalogu repozytorium:
    python -m ZADANIE1.main
"""

import time
from datetime import datetime

import schedule

from ZADANIE1 import baza, loty

LOTNISKO = "FRA"  # kod z loty.LOTNISKA
CO_ILE_S = 60  # odstep miedzy pobraniami w sekundach
POWTORZENIA = 10  # liczba pobran; 0 oznacza: bez pobierania, tylko analiza zapisanej bazy
PLIK_BAZY = "loty.db"
PLIK_WYKRESU = "loty.png"


def pobieraj():
    """Pobiera dane POWTORZENIA razy, co CO_ILE_S sekund, i zapisuje je w bazie."""
    baza.utworz_tabele(PLIK_BAZY, od_nowa=True)
    licznik = 0

    def zadanie():
        nonlocal licznik
        df = loty.pobierz(LOTNISKO)
        baza.zapisz(df, PLIK_BAZY)
        licznik += 1
        print(f"{datetime.now():%H:%M:%S}  pobranie {licznik}/{POWTORZENIA}: {len(df)} samolotów", flush=True)
        if licznik >= POWTORZENIA:
            return schedule.CancelJob

    if zadanie() is schedule.CancelJob:  # pierwsze pobranie od razu
        return
    schedule.every(CO_ILE_S).seconds.do(zadanie)
    while schedule.get_jobs():
        schedule.run_pending()
        time.sleep(1)  # krotka przerwa, zeby petla nie obciazala procesora


def main():
    if POWTORZENIA > 0:
        pobieraj()

    df = baza.wczytaj(PLIK_BAZY)
    print(f"\nW bazie: {len(df)} pomiarów, {df['icao24'].nunique()} różnych samolotów")
    print("Linie lotnicze z największą liczbą samolotów:")
    for kod, ile in baza.linie_lotnicze(PLIK_BAZY):
        print(f"  {kod}  {loty.LINIE_LOTNICZE.get(kod, '?'):<20}{ile:>4}")

    najszybsze = baza.najszybsze_pomiary(PLIK_BAZY)
    nazwa = loty.LOTNISKA[LOTNISKO]["nazwa"]
    tytul = f"{LOTNISKO} ({nazwa}), {loty.PROMIEN_KM} km: {len(najszybsze)} samolotów w powietrzu"
    loty.rysuj(najszybsze, PLIK_WYKRESU, tytul)
    print(f"Wykres zapisano w pliku {PLIK_WYKRESU}")


if __name__ == "__main__":
    main()
