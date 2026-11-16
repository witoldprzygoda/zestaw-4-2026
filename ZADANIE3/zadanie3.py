"""
Zadanie 3 - pojedyncza dyspozycja (singledispatch): rozne wersje funkcji i metody
wybierane na podstawie typu pierwszego argumentu.
"""

from collections.abc import Mapping, Sequence  # noqa: F401
from functools import singledispatch, singledispatchmethod


@singledispatch
def opisz(obiekt):
    """Wersja domyslna: typ, dla ktorego nie zarejestrowano osobnej wersji."""
    return f"inny obiekt: {type(obiekt).__name__}"


# TODO: zarejestrowac wersje funkcji opisz (adnotacje typow, np. def _(obiekt: str):) dla:
#   int i float (jedna wersja, typ int | float) -> "liczba: 42"
#   bool                                        -> "wartość logiczna: prawda" / "wartość logiczna: fałsz"
#   str                                         -> "napis: Kraków"
#   Sequence (lista, krotka, range...)          -> "sekwencja, elementów: 3"
#   Mapping (slownik)                           -> "słownik, kluczy: 2"


class ObslugaZdarzen:
    def __init__(self):
        self.licznik = 0
        self.dziennik = []

    def _zapisz(self, tekst):
        """Zapisuje obsluzone zdarzenie w dzienniku i zwraca jego opis."""
        self.licznik += 1
        self.dziennik.append(tekst)
        return tekst

    @singledispatchmethod
    def obsluz(self, zdarzenie):
        raise TypeError(f"Nieobsługiwany typ zdarzenia: {type(zdarzenie).__name__}")

    # TODO: zarejestrowac wersje metody obsluz dla:
    #   str  -> self._zapisz("komunikat: ...")
    #   int  -> self._zapisz("kod: ...")
    #   list -> lista wynikow self.obsluz(z) dla kazdego elementu z


class ObslugaRozszerzona(ObslugaZdarzen):
    # TODO: wlasna metoda obsluz z dekoratorem @singledispatchmethod; wersja domyslna
    #       przekazuje zdarzenie do klasy bazowej: return super().obsluz(zdarzenie);
    #       rejestracje: int -> "kod rozszerzony: ...", float -> "pomiar: ..."
    pass


def main():
    print("=== funkcja opisz ===")
    for obiekt in [42, 2.5, True, "Kraków", [1, 2, 3], (4, 5), range(10), {"a": 1, "b": 2}, {1, 2}]:
        print(f"{obiekt!r:>18} -> {opisz(obiekt)}")

    print("\n=== ObslugaZdarzen ===")
    baza = ObslugaZdarzen()
    print(baza.obsluz("start systemu"))
    print(baza.obsluz(404))
    print(baza.obsluz(["dysk pełny", 507]))
    try:
        baza.obsluz(3.14)
    except TypeError as e:
        print(e)
    print(f"Obsłużonych zdarzeń: {baza.licznik}")

    print("\n=== ObslugaRozszerzona ===")
    rozszerzona = ObslugaRozszerzona()
    print(rozszerzona.obsluz("start systemu"))
    print(rozszerzona.obsluz(404))
    print(rozszerzona.obsluz(3.14))
    print(rozszerzona.obsluz([1, "x", 2.0]))
    print(f"Obsłużonych zdarzeń: {rozszerzona.licznik}")

    print("\nKlasa bazowa nadal działa po swojemu:", baza.obsluz(500))


if __name__ == "__main__":
    main()
