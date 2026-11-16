from datetime import date

import pytest

from ZADANIE2.zadanie2 import (Autobus, FabrykaAutobusow, FabrykaPojazdow, FabrykaSamochodow, Pojazd,
                               Samochod, main)


# ---------------------------------------------------------------- pojazdy

def test_pojazd_jest_abstrakcyjny():
    with pytest.raises(TypeError):
        Pojazd("Prototyp", 2020)


def test_samochod():
    s = Samochod("Toyota", 2022, liczba_drzwi=5)
    assert isinstance(s, Pojazd)
    assert (s._model, s._rok, s.liczba_drzwi) == ("Toyota", 2022, 5)
    assert Samochod("Fiat", 2020).liczba_drzwi == 4, "Domyslnie 4 drzwi"
    assert s.opis() == "Samochód Toyota (2022), drzwi: 5"
    assert repr(s) == "Samochod('Toyota', 2022)"


def test_autobus():
    a = Autobus("Solaris", 2024, liczba_miejsc=60)
    assert isinstance(a, Pojazd)
    assert a.liczba_miejsc == 60
    assert Autobus("Autosan", 2019).liczba_miejsc == 50, "Domyslnie 50 miejsc"
    assert a.opis() == "Autobus Solaris (2024), miejsc: 60"
    assert repr(a) == "Autobus('Solaris', 2024)"


def test_predkosc_getter_setter_deleter():
    s = Samochod("Ford", 2023)
    assert s.predkosc == 0
    s.predkosc = 100
    assert s.predkosc == 100
    assert s._predkosc == 100
    del s.predkosc
    assert s.predkosc == 0


def test_predkosc_ujemna():
    s = Samochod("BMW", 2023)
    s.predkosc = 30
    with pytest.raises(ValueError, match="Prędkość nie może być ujemna"):
        s.predkosc = -10
    assert s.predkosc == 30, "Po bledzie predkosc bez zmian"


def test_predkosc_jest_wlasciwoscia():
    assert isinstance(Pojazd.__dict__.get("predkosc"), property)


# ---------------------------------------------------------------- fabryki

def test_fabryka_pojazdow_jest_abstrakcyjna():
    with pytest.raises(TypeError):
        FabrykaPojazdow("Fabryka")


def test_nazwa_tylko_do_odczytu():
    f = FabrykaSamochodow("Fabryka Samochodów")
    assert f.nazwa == "Fabryka Samochodów"
    with pytest.raises(AttributeError):
        f.nazwa = "Inna nazwa"


def test_fabryka_samochodow():
    f = FabrykaSamochodow("Fabryka Samochodów")
    s = f.stworz_pojazd("Fiat", 2020, liczba_drzwi=5)
    assert isinstance(s, Samochod)
    assert (s._model, s._rok, s.liczba_drzwi) == ("Fiat", 2020, 5)
    f.stworz_pojazd("Fiat", 2021)
    assert f.ile_wyprodukowano() == 2


def test_fabryka_autobusow():
    f = FabrykaAutobusow("Fabryka Autobusów")
    a = f.stworz_pojazd("Volvo", 2019, liczba_miejsc=60)
    assert isinstance(a, Autobus)
    assert a.liczba_miejsc == 60
    assert f.ile_wyprodukowano() == 1


def test_licznik_osobny_dla_kazdej_fabryki():
    f1, f2 = FabrykaSamochodow("A"), FabrykaSamochodow("B")
    f1.stworz_pojazd("Fiat", 2020)
    assert (f1.ile_wyprodukowano(), f2.ile_wyprodukowano()) == (1, 0)


def test_zly_rok():
    f = FabrykaSamochodow("Fabryka Samochodów")
    with pytest.raises(ValueError, match="Nieprawidłowy rok produkcji"):
        f.stworz_pojazd("Fiat", 1899)
    with pytest.raises(ValueError, match="Nieprawidłowy rok produkcji"):
        FabrykaAutobusow("Fabryka").stworz_pojazd("Jelcz", date.today().year + 1)
    assert f.ile_wyprodukowano() == 0, "Nieudana produkcja nie zwieksza licznika"


def test_sprawdz_rok_metoda_statyczna():
    biezacy = date.today().year
    assert FabrykaPojazdow.sprawdz_rok(1900) and FabrykaPojazdow.sprawdz_rok(biezacy)
    assert not FabrykaPojazdow.sprawdz_rok(1899)
    assert not FabrykaPojazdow.sprawdz_rok(biezacy + 1)
    assert isinstance(FabrykaPojazdow.__dict__.get("sprawdz_rok"), staticmethod)


def test_utworz_fabryke():
    fs = FabrykaPojazdow.utworz_fabryke("samochod", "Fabryka Samochodów")
    fa = FabrykaPojazdow.utworz_fabryke("autobus", "Fabryka Autobusów")
    assert isinstance(fs, FabrykaSamochodow) and fs.nazwa == "Fabryka Samochodów"
    assert isinstance(fa, FabrykaAutobusow) and fa.nazwa == "Fabryka Autobusów"
    assert isinstance(FabrykaPojazdow.__dict__.get("utworz_fabryke"), classmethod)


def test_utworz_fabryke_nieznany_typ():
    with pytest.raises(ValueError, match="Nieznany typ fabryki"):
        FabrykaPojazdow.utworz_fabryke("rakieta", "Kosmodrom")


def test_rejestracja_przez_init_subclass():
    class Rower(Pojazd):
        def opis(self):
            return f"Rower {self._model}"

    class FabrykaRowerow(FabrykaPojazdow, typ="rower"):
        def stworz_pojazd(self, model, rok):
            self._zwieksz_licznik()
            return Rower(model, rok)

    try:
        assert FabrykaPojazdow.dostepne_typy() == ["autobus", "rower", "samochod"]
        f = FabrykaPojazdow.utworz_fabryke("rower", "Fabryka Rowerów")
        assert isinstance(f, FabrykaRowerow)
        assert f.stworz_pojazd("Kross", 2024).opis() == "Rower Kross"
    finally:
        FabrykaPojazdow._rejestr.pop("rower", None)


def test_dostepne_typy():
    assert FabrykaPojazdow.dostepne_typy() == ["autobus", "samochod"]


def test_main(capsys):
    main()
    out = capsys.readouterr().out
    assert "Samochod('Fiat', 2023) -> Samochód Fiat (2023), drzwi: 5" in out
    assert "Prędkość po usunięciu: 0" in out
    assert "Wyprodukowano samochodów: 1" in out
