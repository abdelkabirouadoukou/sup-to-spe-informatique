"""Tests de l'arithmétique : puissances, PGCD, Horner, crible."""

import random

import pytest

from revision import crible, horner, pgcd, puissance_iter, puissance_rec


@pytest.mark.parametrize("x", [0, 1, 2, 3, 5, -2])
def test_puissance_exposant_nul(x):
    assert puissance_rec(x, 0) == 1
    assert puissance_iter(x, 0) == 1


@pytest.mark.parametrize("x", [2, 3, 5, -2])
@pytest.mark.parametrize("n", range(0, 21))
def test_puissance_rec_et_iter_concordent(x, n):
    assert puissance_rec(x, n) == x**n
    assert puissance_iter(x, n) == x**n


@pytest.mark.parametrize("n", [-1, -10])
def test_puissance_exposant_negatif_leve_value_error(n):
    with pytest.raises(ValueError):
        puissance_rec(2, n)
    with pytest.raises(ValueError):
        puissance_iter(2, n)


def test_puissance_grand_exposant():
    assert puissance_iter(2, 100) == 2**100
    assert puissance_rec(2, 100) == 2**100


@pytest.mark.parametrize(
    "a,b,attendu",
    [
        (48, 18, 6),
        (18, 48, 6),
        (0, 0, 0),
        (0, 5, 5),
        (5, 0, 5),
        (-48, 18, 6),
        (17, 5, 1),
        (100, 10, 10),
    ],
)
def test_pgcd(a, b, attendu):
    assert pgcd(a, b) == attendu


@pytest.mark.parametrize(
    "coeffs,x,attendu",
    [
        ([], 5, 0),
        ([7], 5, 7),
        ([1, 2, 3], 2, 17),
        ([0, 0, 1], 3, 9),
        ([1, -1], 2, -1),
    ],
)
def test_horner(coeffs, x, attendu):
    assert horner(coeffs, x) == attendu


def test_horner_egal_evaluation_naive():
    rng = random.Random(3)
    for _ in range(50):
        degre = rng.randint(0, 8)
        coeffs = [rng.randint(-5, 5) for _ in range(degre + 1)]
        x = rng.randint(-3, 3)
        attendu = sum(a * x**k for k, a in enumerate(coeffs))
        assert horner(coeffs, x) == attendu


@pytest.mark.parametrize("n", [-5, 0, 1])
def test_crible_petites_valeurs(n):
    assert crible(n) == []


def test_crible_valeurs_connues():
    assert crible(2) == [2]
    assert crible(20) == [2, 3, 5, 7, 11, 13, 17, 19]
    assert len(crible(100)) == 25
