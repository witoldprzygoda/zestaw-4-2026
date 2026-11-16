import math

import plum
import pytest

from ZADANIE4.zadanie4 import Figura, Kolo, Kwadrat, Prostokat, czy_przecinaja, kolizje, main, pole


# ---------------------------------------------------------------- pole

def test_pole_kolo():
    assert pole(Kolo(0, 0, 2)) == pytest.approx(4 * math.pi)


def test_pole_prostokat():
    assert pole(Prostokat(0, 0, 2, 3)) == pytest.approx(6)
    assert isinstance(pole(Prostokat(0, 0, 2, 3)), float)


def test_pole_kwadrat_przez_dziedziczenie():
    assert pole(Kwadrat(1, 1, 3)) == pytest.approx(9)


def test_pole_figura_bez_wersji():
    with pytest.raises(plum.NotFoundLookupError):
        pole(Figura())


def test_funkcje_plum():
    assert isinstance(pole, plum.Function), "pole definiowane dekoratorem @dispatch z plum"
    assert isinstance(czy_przecinaja, plum.Function)


# ---------------------------------------------------------------- czy_przecinaja

@pytest.mark.parametrize("a, b, wynik", [
    (Kolo(0, 0, 1), Kolo(1.5, 0, 1), True),
    (Kolo(0, 0, 1), Kolo(2, 0, 1), True),          # styczne
    (Kolo(0, 0, 1), Kolo(3, 0, 1), False),
    (Kolo(0, 0, 5), Kolo(1, 1, 1), True),          # jedno w drugim
])
def test_kolo_kolo(a, b, wynik):
    assert czy_przecinaja(a, b) is wynik


@pytest.mark.parametrize("a, b, wynik", [
    (Prostokat(0, 0, 2, 2), Prostokat(1, 1, 3, 3), True),
    (Prostokat(0, 0, 2, 2), Prostokat(2, 0, 4, 2), True),    # wspolny bok
    (Prostokat(0, 0, 2, 2), Prostokat(2.1, 0, 4, 2), False),
    (Prostokat(0, 0, 2, 2), Prostokat(0, 3, 2, 4), False),   # rozne y, te same x
    (Prostokat(0, 0, 10, 10), Prostokat(4, 4, 5, 5), True),  # jeden w drugim
])
def test_prostokat_prostokat(a, b, wynik):
    assert czy_przecinaja(a, b) is wynik


@pytest.mark.parametrize("a, b, wynik", [
    (Kolo(1.5, 0, 1), Prostokat(2, -1, 4, 1), True),
    (Kolo(0, 0, 1), Prostokat(1, -1, 3, 1), True),           # styczne
    (Kolo(4.8, 1.8, 1), Prostokat(2, -1, 4, 1), False),      # przy narozniku: same prostokaty opisane sie przecinaja
    (Kolo(3, 0, 0.5), Prostokat(2, -1, 4, 1), True),         # kolo wewnatrz prostokata
    (Kolo(10, 10, 1), Prostokat(2, -1, 4, 1), False),
])
def test_kolo_prostokat_w_obie_strony(a, b, wynik):
    assert czy_przecinaja(a, b) is wynik
    assert czy_przecinaja(b, a) is wynik


def test_kwadrat_przez_dziedziczenie():
    assert czy_przecinaja(Kwadrat(2.6, 0.6, 1), Prostokat(2, -1, 4, 1)) is True
    assert czy_przecinaja(Kwadrat(0, 0, 1), Kolo(3, 3, 1)) is False
    assert czy_przecinaja(Kolo(0, 0, 1), Kwadrat(0.5, 0.5, 2)) is True


def test_brak_wersji_dla_figury_bazowej():
    with pytest.raises(plum.NotFoundLookupError):
        czy_przecinaja(Figura(), Kolo(0, 0, 1))


# ---------------------------------------------------------------- kolizje

def test_kolizje():
    figury = [Kolo(0, 0, 1), Kolo(1.5, 0, 1), Prostokat(2, -1, 4, 1), Kwadrat(-3, -3, 1.5),
              Kolo(4.8, 1.8, 1), Kwadrat(2.6, 0.6, 1)]
    assert kolizje(figury) == [(0, 1), (1, 2), (2, 5)]


def test_kolizje_puste():
    assert kolizje([]) == []
    assert kolizje([Kolo(0, 0, 1)]) == []


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "2 i 5" in out
