# Diagramy do zadania 2

Pliki `.mmd` to źródła diagramów w języku Mermaid (np. https://mermaid.live).
GitHub wyświetla poniższe diagramy bezpośrednio na stronie repozytorium.

## Diagram klas

```mermaid
classDiagram
    direction TB
    class Pojazd {
        <<abstract>>
        #str _model
        #int _rok
        #float _predkosc
        +predkosc: float «property»
        +opis()* str
        +\_\_repr\_\_() str
    }
    class Samochod {
        +int liczba_drzwi
        +opis() str
    }
    class Autobus {
        +int liczba_miejsc
        +opis() str
    }
    class FabrykaPojazdow {
        <<abstract>>
        -dict _rejestr$
        #str _nazwa
        #int _liczba_wyprodukowanych
        +nazwa: str «property»
        +\_\_init_subclass\_\_(typ)$
        +utworz_fabryke(typ, nazwa)$ FabrykaPojazdow
        +dostepne_typy()$ list
        +sprawdz_rok(rok)$ bool
        +stworz_pojazd(model, rok, **parametry)* Pojazd
        #_zwieksz_licznik()
        +ile_wyprodukowano() int
    }
    class FabrykaSamochodow {
        +stworz_pojazd(model, rok, liczba_drzwi) Samochod
    }
    class FabrykaAutobusow {
        +stworz_pojazd(model, rok, liczba_miejsc) Autobus
    }
    Pojazd <|-- Samochod
    Pojazd <|-- Autobus
    FabrykaPojazdow <|-- FabrykaSamochodow : typ="samochod"
    FabrykaPojazdow <|-- FabrykaAutobusow : typ="autobus"
    FabrykaSamochodow ..> Samochod : tworzy
    FabrykaAutobusow ..> Autobus : tworzy
```

## Diagram sekwencji: działanie main()

```mermaid
sequenceDiagram
    participant M as main()
    participant FP as FabrykaPojazdow
    Note over FP: definicja klasy FabrykaSamochodow<br/>wywołuje __init_subclass__(typ="samochod"),<br/>który zapisuje ją w _rejestr
    M->>FP: utworz_fabryke("samochod", "Fabryka Samochodów Warszawa")
    create participant FS as FabrykaSamochodow
    FP->>FS: _rejestr["samochod"](nazwa)
    FP-->>M: obiekt FabrykaSamochodow
    M->>FS: stworz_pojazd("Fiat", 2023, liczba_drzwi=5)
    activate FS
    FS->>FS: sprawdz_rok(2023)
    create participant S as Samochod
    FS->>S: Samochod("Fiat", 2023, 5)
    FS->>FS: _zwieksz_licznik()
    FS-->>M: samochod
    deactivate FS
    M->>S: opis()
    S-->>M: "Samochód Fiat (2023), drzwi: 5"
    M->>S: predkosc = 50, del predkosc
    M->>FS: ile_wyprodukowano()
    FS-->>M: 1
```
