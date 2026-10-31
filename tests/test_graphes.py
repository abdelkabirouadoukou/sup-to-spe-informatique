"""Tests des graphes : BFS, DFS, composantes, représentations."""

import pytest

from revision import (
    bfs,
    composantes_connexes,
    dfs,
    est_connexe,
    liste_successeurs,
    matrice_adjacence,
)


def test_bfs_graphe_vide():
    assert bfs({}, 0) == {0: 0}


def test_bfs_chaine():
    graphe = {0: [1], 1: [0, 2], 2: [1]}
    assert bfs(graphe, 0) == {0: 0, 1: 1, 2: 2}


def test_bfs_graphe_deconnecte():
    graphe = {0: [1], 1: [0], 2: [3], 3: [2]}
    assert bfs(graphe, 0) == {0: 0, 1: 1}


def test_dfs_chaine():
    graphe = {0: [1], 1: [0, 2], 2: [1]}
    assert dfs(graphe, 0) == [0, 1, 2]


def test_dfs_etoile():
    graphe = {0: [1, 2, 3], 1: [0], 2: [0], 3: [0]}
    assert dfs(graphe, 0) == [0, 1, 2, 3]


def test_composantes_connexes_vide():
    assert composantes_connexes({}) == []


def test_composantes_connexes_sommets_isoles():
    composantes = composantes_connexes({0: [], 1: []})
    assert {frozenset(c) for c in composantes} == {frozenset({0}), frozenset({1})}


def test_composantes_connexes_deux_composantes():
    graphe = {0: [1], 1: [0], 2: [3], 3: [2]}
    composantes = composantes_connexes(graphe)
    assert {frozenset(c) for c in composantes} == {
        frozenset({0, 1}),
        frozenset({2, 3}),
    }


@pytest.mark.parametrize(
    "graphe,attendu",
    [
        ({}, True),
        ({0: []}, True),
        ({0: [1], 1: [0]}, True),
        ({0: [], 1: []}, False),
    ],
)
def test_est_connexe(graphe, attendu):
    assert est_connexe(graphe) is attendu


def test_matrice_adjacence():
    matrice = matrice_adjacence(3, [(0, 1), (1, 2)])
    assert matrice == [
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0],
    ]
    assert matrice == [list(ligne) for ligne in zip(*matrice)]  # symétrique


def test_matrice_adjacence_vide():
    assert matrice_adjacence(0, []) == []


def test_matrice_adjacence_arete_invalide():
    with pytest.raises(ValueError):
        matrice_adjacence(2, [(0, 2)])
    with pytest.raises(ValueError):
        matrice_adjacence(-1, [])


def test_liste_successeurs():
    assert liste_successeurs(3, [(0, 1)]) == {0: [1], 1: [0], 2: []}
    assert liste_successeurs(0, []) == {}


def test_liste_successeurs_arete_invalide():
    with pytest.raises(ValueError):
        liste_successeurs(2, [(0, 5)])
    with pytest.raises(ValueError):
        liste_successeurs(-1, [])
