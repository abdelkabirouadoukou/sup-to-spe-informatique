"""Tests des algorithmes de tri."""

import random

import pytest

from revision import est_triee, fusion, tri_fusion, tri_insertion, tri_selection


def _jeu_de_tests():
    return [
        [],
        [1],
        [2, 1],
        [1, 1, 1],
        [3, 1, 2, 1, 3],
        list(range(10)),
        list(range(10, 0, -1)),
    ]


@pytest.mark.parametrize("liste", _jeu_de_tests())
def test_tri_selection_trie_en_place(liste):
    attendu = sorted(liste)
    tri_selection(liste)
    assert liste == attendu


@pytest.mark.parametrize("liste", _jeu_de_tests())
def test_tri_insertion_trie_en_place(liste):
    attendu = sorted(liste)
    tri_insertion(liste)
    assert liste == attendu


@pytest.mark.parametrize("liste", _jeu_de_tests())
def test_tri_fusion_renvoie_nouvelle_liste(liste):
    original = list(liste)
    resultat = tri_fusion(liste)
    assert resultat == sorted(liste)
    assert liste == original  # entrée non modifiée


def test_tri_fusion_aleatoire():
    rng = random.Random(42)
    for _ in range(100):
        liste = [rng.randint(0, 50) for _ in range(rng.randint(0, 30))]
        assert tri_fusion(liste) == sorted(liste)


def test_tri_fusion_est_stable():
    paires = [(1, "a"), (0, "b"), (1, "c"), (0, "d")]
    assert tri_fusion(paires) == [(0, "b"), (0, "d"), (1, "a"), (1, "c")]


def test_tri_insertion_meilleur_cas_deja_trie():
    liste = list(range(1000))
    tri_insertion(liste)
    assert liste == list(range(1000))


def test_fusion_cas_limites():
    assert fusion([], []) == []
    assert fusion([], [1, 2]) == [1, 2]
    assert fusion([1, 2], []) == [1, 2]
    assert fusion([1, 3, 5], [2, 4]) == [1, 2, 3, 4, 5]


def test_fusion_conserve_les_doublons():
    assert fusion([1, 2, 2], [2, 3]) == [1, 2, 2, 2, 3]


@pytest.mark.parametrize(
    "liste,attendu",
    [
        ([], True),
        ([1], True),
        ([1, 1], True),
        ([1, 2, 2, 5], True),
        ([2, 1], False),
        ([1, 3, 2], False),
    ],
)
def test_est_triee(liste, attendu):
    assert est_triee(liste) is attendu
