---
title:
- Drzewa Decyzyjne i Wnioskowanie
author:
- Mateusz Jakubczak, Krzysztof Olipra, Karol Oleszek 
theme:
- Copenhagen
---


# Drzewa Decyzyjne i Wnioskowanie

Badany zbiór danych opisuje przesłanki i decyzję czy pracować w danej firmie informatycznej.


# Przesłanki

czy_zagraniczna 0/1
mozliwosci_rozwoju 0/1/2
wielkosc_firmy 0/1/2
typ_firmy 0/1/2
wynagrodzenie 0/1/2/3
Decyzja:
czy_pracowac 0/1


# Drzewo decyzyjne

```
Question: Does czy_zagraniczna equal 0?
Yes:
| Question: Does typ_firmy equal 0?
| Yes:
| | Decision: 0
| No:
| | Question: Does typ_firmy equal 1?
| | Yes:
| | | Decision: 0
| | No:
| | | Question: Does wynagrodzenie equal 0?
| | | Yes:
| | | | Decision: 0
| | | No:
| | | | Question: Does wynagrodzenie equal 1?
| | | | Yes:
| | | | | Decision: 0
| | | | No:
| | | | | Decision: 1
No:
| Question: Does wielkosc_firmy equal 0?
| Yes:
| | Question: Does typ_firmy equal 0?
| | Yes:
| | | Decision: 0
| | No:
| | | Question: Does typ_firmy equal 1?
| | | Yes:
| | | | Decision: 0
| | | No:
| | | | Question: Does wynagrodzenie equal 0?
| | | | Yes:
| | | | | Decision: 0
| | | | No:
| | | | | Question: Does wynagrodzenie equal 1?
| | | | | Yes:
| | | | | | Decision: 0
| | | | | No:
| | | | | | Decision: 1
| No:
| | Question: Does wynagrodzenie equal 0?
| | Yes:
| | | Question: Does mozliwosci_rozwoju equal 0?
| | | Yes:
| | | | Decision: 0
| | | No:
| | | | Question: Does mozliwosci_rozwoju equal 1?
| | | | Yes:
| | | | | Decision: 0
| | | | No:
| | | | | Decision: 1
| | No:
| | | Decision: 1
```