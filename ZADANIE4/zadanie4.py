"""
Zadanie 4 - wielokrotna dyspozycja (multiple dispatch) z biblioteka plum:
wersja funkcji wybierana na podstawie typow wszystkich argumentow.
"""

import math  # noqa: F401
from itertools import combinations  # noqa: F401

from plum import dispatch  # noqa: F401


class Figura:
    """Klasa bazowa figur."""


class Kolo(Figura):
    def __init__(self, x, y, r):
        self.x, self.y, self.r = x, y, r

    def __repr__(self):
        return f"Kolo({self.x}, {self.y}, {self.r})"


class Prostokat(Figura):
    """Prostokat o bokach rownoleglych do osi: lewy dolny rog (x1, y1), prawy gorny (x2, y2)."""

    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

    def __repr__(self):
        return f"Prostokat({self.x1}, {self.y1}, {self.x2}, {self.y2})"


class Kwadrat(Prostokat):
    """Kwadrat o lewym dolnym rogu (x, y) i boku a."""

    def __init__(self, x, y, a):
        super().__init__(x, y, x + a, y + a)
        self.a = a

    def __repr__(self):
        return f"Kwadrat({self.x1}, {self.y1}, {self.a})"


# TODO: wersje funkcji pole (dekorator @dispatch, typ argumentu w adnotacji):
#   Kolo      -> pi * r**2
#   Prostokat -> (x2 - x1) * (y2 - y1); Kwadrat korzysta z tej wersji przez dziedziczenie
# TODO: wersje funkcji czy_przecinaja(a, b) dla par:
#   (Kolo, Kolo), (Prostokat, Prostokat), (Kolo, Prostokat), (Prostokat, Kolo)
#   figury stykajace sie (wspolny punkt brzegu) tez sie przecinaja
# Ponizsze zaslepki zastapic wersjami z dekoratorem @dispatch.

def pole(f):
    raise NotImplementedError("pole: do napisania")


def czy_przecinaja(a, b):
    raise NotImplementedError("czy_przecinaja: do napisania")


def kolizje(figury):
    """Lista par indeksow (i, j), i < j, figur, ktore sie przecinaja."""
    pass


def main():
    figury = [Kolo(0, 0, 1), Kolo(1.5, 0, 1), Prostokat(2, -1, 4, 1), Kwadrat(-3, -3, 1.5),
              Kolo(4.8, 1.8, 1), Kwadrat(2.6, 0.6, 1)]
    for i, f in enumerate(figury):
        print(f"{i}: {f!r:<24} pole = {pole(f):6.2f}")
    print("\nPrzecinające się pary:")
    for i, j in kolizje(figury):
        print(f"  {i} i {j}: {figury[i]!r} oraz {figury[j]!r}")


if __name__ == "__main__":
    main()
