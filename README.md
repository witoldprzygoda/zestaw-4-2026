# Zestaw 4 - Język Python

Cztery zadania laboratoryjne. Pełna treść zadań znajduje się w dokumencie PDF zestawu.

## Zawartość repozytorium

| Katalog    | Pliki do uzupełnienia      | Testy                    | Punkty |
|------------|----------------------------|--------------------------|--------|
| `ZADANIE1` | `loty.py`, `baza.py`       | `tests/test_zadanie1.py` | 2      |
| `ZADANIE2` | `zadanie2.py`              | `tests/test_zadanie2.py` | 1      |
| `ZADANIE3` | `zadanie3.py`              | `tests/test_zadanie3.py` | 1      |
| `ZADANIE4` | `zadanie4.py`              | `tests/test_zadanie4.py` | 1      |

Program główny zadania 1 (`ZADANIE1/main.py`) jest kompletny; uruchamiamy go z głównego katalogu
repozytorium poleceniem `python -m ZADANIE1.main`. W katalogu `ZADANIE2/UML` są diagramy klas
i sekwencji (język Mermaid), wyświetlane przez GitHub w pliku `ZADANIE2/UML/README.md`.

## Przygotowanie

```
python -m pip install -r requirements.txt
```

## Uruchamianie testów

```
python -m pytest            # wszystkie zadania
python -m pytest ZADANIE1   # jedno zadanie
python -m pytest -v         # z listą poszczególnych testów
```

Testy nie korzystają z sieci. Nie zmieniaj plików z testami ani nazw funkcji w kodzie początkowym.
