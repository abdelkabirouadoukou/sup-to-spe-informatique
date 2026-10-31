"""Tests des algorithmes de recherche."""

import pytest

from revision import dichotomie, recherche_lineaire


def test_dichotomie_liste_vide():
    assert dichotomie(3, []) is None


def test_dichotomie_un_seul_element():
    assert dichotomie(5, [5]) == 0
    assert dichotomie(4, [5]) is None


def test_dichotomie_tous_les_elements():
    liste = [1, 3, 5, 7, 9, 11]
    for indice, valeur in enumerate(liste):
        assert dichotomie(valeur, liste) == indice


def test_dichotomie_absent():
    liste = [1, 3, 5, 7, 9]
    assert dichotomie(0, liste) is None
    assert dichotomie(4, liste) is None
    assert dichotomie(10, liste) is None


def test_dichotomie_doublons_renvoie_une_occurrence_valide():
    liste = [1, 2, 2, 2, 3]
    indice = dichotomie(2, liste)
    assert indice is not None
    assert liste[indice] == 2


def test_dichotomie_grande_liste():
    liste = list(range(0, 1000, 2))
    assert dichotomie(500, liste) == 250
    assert dichotomie(501, liste) is None


@pytest.mark.parametrize(
    "liste,cherche,attendu",
    [
        ([], 1, None),
        ([1], 1, 0),
        ([1], 2, None),
        ([1, 2, 3], 2, 1),
        ([1, 2, 2, 3], 2, 1),  # première occurrence
        ([1, 2, 3], 9, None),
    ],
)
def test_recherche_lineaire(liste, cherche, attendu):
    assert recherche_lineaire(cherche, liste) == attendu
