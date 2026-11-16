"""
Zadanie 2 - klasy abstrakcyjne (ABC), wlasciwosci (@property z setterem i deleterem),
metody klasy i statyczne oraz wzorzec "metoda wytworcza" z rejestracja fabryk
przez __init_subclass__.
"""

from abc import ABC, abstractmethod  # noqa: F401
from datetime import date  # noqa: F401


class Pojazd(ABC):
    def __init__(self, model, rok):
        self._model = model
        self._rok = rok
        self._predkosc = 0.0

    # TODO: wlasciwosc predkosc: getter, setter (dla wartosci ujemnej ValueError
    #       z komunikatem "Prędkość nie może być ujemna"), deleter (ustawia 0.0)

    # TODO: metoda abstrakcyjna opis()

    def __repr__(self):
        # TODO: nazwa klasy, model i rok, np. Samochod('Fiat', 2023)
        pass


class Samochod(Pojazd):
    def __init__(self, model, rok, liczba_drzwi=4):
        # TODO: wywolac __init__ klasy bazowej i zapamietac liczba_drzwi
        pass

    def opis(self):
        # TODO: np. "Samochód Fiat (2023), drzwi: 5"
        pass


class Autobus(Pojazd):
    def __init__(self, model, rok, liczba_miejsc=50):
        # TODO: wywolac __init__ klasy bazowej i zapamietac liczba_miejsc
        pass

    def opis(self):
        # TODO: np. "Autobus Solaris (2024), miejsc: 60"
        pass


class FabrykaPojazdow(ABC):
    _rejestr = {}  # typ fabryki (napis) -> klasa fabryki

    def __init_subclass__(cls, typ=None, **kwargs):
        super().__init_subclass__(**kwargs)
        # TODO: jesli podano typ, zapisac klase cls w slowniku FabrykaPojazdow._rejestr

    def __init__(self, nazwa):
        self._nazwa = nazwa
        self._liczba_wyprodukowanych = 0

    # TODO: wlasciwosc nazwa (tylko do odczytu)
    # TODO: metoda abstrakcyjna stworz_pojazd(self, model, rok, **parametry)
    # TODO: metoda klasy utworz_fabryke(cls, typ, nazwa); dla nieznanego typu ValueError
    #       z komunikatem "Nieznany typ fabryki: ..."
    # TODO: metoda klasy dostepne_typy(cls): posortowana lista zarejestrowanych typow
    # TODO: metoda statyczna sprawdz_rok(rok): czy 1900 <= rok <= biezacy rok
    # TODO: metody _zwieksz_licznik() i ile_wyprodukowano()


class FabrykaSamochodow(FabrykaPojazdow, typ="samochod"):
    def stworz_pojazd(self, model, rok, liczba_drzwi=4):
        # TODO: sprawdzic rok (ValueError "Nieprawidłowy rok produkcji: ..."),
        #       utworzyc Samochod, zwiekszyc licznik, zwrocic pojazd
        pass


class FabrykaAutobusow(FabrykaPojazdow, typ="autobus"):
    def stworz_pojazd(self, model, rok, liczba_miejsc=50):
        # TODO: jak w FabrykaSamochodow, ale tworzymy Autobus
        pass


def main():
    print("Dostępne typy fabryk:", ", ".join(FabrykaPojazdow.dostepne_typy()))
    fabryka_samochodow = FabrykaPojazdow.utworz_fabryke("samochod", "Fabryka Samochodów Warszawa")
    fabryka_autobusow = FabrykaPojazdow.utworz_fabryke("autobus", "Fabryka Autobusów Kraków")
    print(f"Fabryka: {fabryka_samochodow.nazwa}")
    print(f"Fabryka: {fabryka_autobusow.nazwa}")

    samochod = fabryka_samochodow.stworz_pojazd("Fiat", 2023, liczba_drzwi=5)
    autobus = fabryka_autobusow.stworz_pojazd("Solaris", 2024, liczba_miejsc=60)
    print(repr(samochod), "->", samochod.opis())
    print(repr(autobus), "->", autobus.opis())

    samochod.predkosc = 50  # setter
    print(f"Prędkość samochodu: {samochod.predkosc}")  # getter
    del samochod.predkosc  # deleter
    print(f"Prędkość po usunięciu: {samochod.predkosc}")
    try:
        samochod.predkosc = -10
    except ValueError as e:
        print(f"Błąd: {e}")
    try:
        fabryka_samochodow.stworz_pojazd("Ford T", 1899)
    except ValueError as e:
        print(f"Błąd: {e}")

    print(f"Wyprodukowano samochodów: {fabryka_samochodow.ile_wyprodukowano()}")
    print(f"Wyprodukowano autobusów: {fabryka_autobusow.ile_wyprodukowano()}")


if __name__ == "__main__":
    main()
