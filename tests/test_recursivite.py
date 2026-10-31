"""Tests des fonctions récursives."""

import pytest

from revision import (
    a_doublon,
    factorielle,
    fib_memo,
    fib_naif,
    hanoi_coups,
    maximum_dichotomie,
    renverse,
    somme_chiffres,
)


@pytest.mark.parametrize(
    "n,attendu", [(0, 1), (1, 1), (2, 2), (5, 120), (10, 3628800)]
)
def test_factorielle(n, attendu):
    assert factorielle(n) == attendu


def test_factorielle_negative():
    with pytest.raises(ValueError):
        factorielle(-1)


@pytest.mark.parametrize("n,attendu", [(0, 0), (9, 9), (10, 1), (1234, 10)])
def test_somme_chiffres(n, attendu):
    assert somme_chiffres(n) == attendu


def test_somme_chiffres_negative():
    with pytest.raises(ValueError):
        somme_chiffres(-1)


def test_fibonacci_naif_et_memoises_concordent():
    for n in range(0, 21):
        assert fib_naif(n) == fib_memo(n)


def test_fibonacci_valeurs_connues():
    assert fib_naif(15) == 610
    assert fib_memo(90) == 2880067194370816120


def test_fibonacci_negative():
    with pytest.raises(ValueError):
        fib_naif(-1)
    with pytest.raises(ValueError):
        fib_memo(-1)


@pytest.mark.parametrize(
    "n,attendu",
    [(0, 0), (1, 1), (2, 3), (4, 15)],
)
def test_hanoi_nombre_de_coups(n, attendu):
    assert len(hanoi_coups(n)) == attendu


def test_hanoi_premier_et_dernier_coup():
    assert hanoi_coups(1) == [("A", "C")]
    coups = hanoi_coups(2)
    assert coups[0] == ("A", "B")
    assert coups[-1] == ("B", "C")


def test_hanoi_negative():
    with pytest.raises(ValueError):
        hanoi_coups(-1)


@pytest.mark.parametrize(
    "liste,attendu",
    [
        ([5], 5),
        ([3, 9, 2, 7], 9),
        ([1, 2, 3, 4], 4),
        ([4, 3, 2, 1], 4),
        ([-5, -1, -9], -1),
        ([2, 2, 2], 2),
    ],
)
def test_maximum_dichotomie(liste, attendu):
    assert maximum_dichotomie(liste) == attendu


def test_maximum_dichotomie_liste_vide():
    with pytest.raises(ValueError):
        maximum_dichotomie([])


@pytest.mark.parametrize(
    "liste,attendu",
    [([], []), ([1], [1]), ([1, 2, 3], [3, 2, 1])],
)
def test_renverse(liste, attendu):
    original = list(liste)
    assert renverse(liste) == attendu
    assert liste == original


@pytest.mark.parametrize(
    "liste,attendu",
    [
        ([], False),
        ([1], False),
        ([1, 2, 3], False),
        ([1, 2, 1], True),
        ([2, 2], True),
    ],
)
def test_a_doublon(liste, attendu):
    assert a_doublon(liste) is attendu
