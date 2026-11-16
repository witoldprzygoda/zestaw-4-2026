from collections.abc import Mapping, Sequence
from functools import singledispatchmethod

import pytest

from ZADANIE3.zadanie3 import ObslugaRozszerzona, ObslugaZdarzen, main, opisz


# ---------------------------------------------------------------- opisz (singledispatch)

@pytest.mark.parametrize("obiekt, oczekiwane", [
    (42, "liczba: 42"),
    (2.5, "liczba: 2.5"),
    ("Kraków", "napis: Kraków"),
    ([1, 2, 3], "sekwencja, elementów: 3"),
    ((4, 5), "sekwencja, elementów: 2"),
    (range(10), "sekwencja, elementów: 10"),
    ({"a": 1, "b": 2}, "słownik, kluczy: 2"),
    ({1, 2}, "inny obiekt: set"),
    (None, "inny obiekt: NoneType"),
])
def test_opisz(obiekt, oczekiwane):
    assert opisz(obiekt) == oczekiwane


def test_opisz_bool_przed_int():
    assert opisz(True) == "wartość logiczna: prawda"
    assert opisz(False) == "wartość logiczna: fałsz"


def test_opisz_rejestr():
    for typ in (int, float, bool, str, Sequence, Mapping):
        assert typ in opisz.registry, f"Brak wersji opisz dla typu {typ.__name__}"


# ---------------------------------------------------------------- ObslugaZdarzen (singledispatchmethod)

def test_obsluga_str_int():
    h = ObslugaZdarzen()
    assert h.obsluz("start") == "komunikat: start"
    assert h.obsluz(404) == "kod: 404"
    assert h.licznik == 2
    assert h.dziennik == ["komunikat: start", "kod: 404"]


def test_obsluga_listy():
    h = ObslugaZdarzen()
    assert h.obsluz(["a", 1]) == ["komunikat: a", "kod: 1"]
    assert h.obsluz(["b", [2, 3]]) == ["komunikat: b", ["kod: 2", "kod: 3"]], "Lista w liscie"
    assert h.licznik == 5, "Kazdy element listy to osobne zdarzenie"


def test_obsluga_nieobslugiwany_typ():
    h = ObslugaZdarzen()
    with pytest.raises(TypeError, match="Nieobsługiwany typ zdarzenia: set"):
        h.obsluz({1, 2})
    assert h.licznik == 0


def test_licznik_osobny_dla_obiektu():
    h1, h2 = ObslugaZdarzen(), ObslugaZdarzen()
    h1.obsluz("x")
    assert (h1.licznik, h2.licznik) == (1, 0)


# ---------------------------------------------------------------- ObslugaRozszerzona

def test_rozszerzona_nowe_wersje():
    r = ObslugaRozszerzona()
    assert r.obsluz(404) == "kod rozszerzony: 404"
    assert r.obsluz(3.14) == "pomiar: 3.14"
    assert r.licznik == 2


def test_rozszerzona_korzysta_z_klasy_bazowej():
    r = ObslugaRozszerzona()
    assert r.obsluz("start") == "komunikat: start"
    assert r.obsluz([1, "x", 2.0]) == ["kod rozszerzony: 1", "komunikat: x", "pomiar: 2.0"]
    with pytest.raises(TypeError, match="Nieobsługiwany typ zdarzenia: set"):
        r.obsluz({1})


def test_klasa_bazowa_bez_zmian():
    ObslugaRozszerzona().obsluz(1)
    h = ObslugaZdarzen()
    assert h.obsluz(7) == "kod: 7", "Rejestracje klasy pochodnej nie zmieniaja klasy bazowej"
    with pytest.raises(TypeError):
        h.obsluz(1.5)


def test_rozszerzona_ma_wlasna_metode():
    assert isinstance(ObslugaRozszerzona.__dict__.get("obsluz"), singledispatchmethod)
    assert isinstance(ObslugaZdarzen.__dict__.get("obsluz"), singledispatchmethod)


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "wartość logiczna: prawda" in out
    assert "Klasa bazowa nadal działa po swojemu: kod: 500" in out
