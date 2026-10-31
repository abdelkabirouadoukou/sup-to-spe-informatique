"""Tests des piles, files et utilitaires de structures."""

import pytest

from revision import File, Pile, bien_parenthese, compter_occurrences


def test_pile_lifo():
    pile = Pile()
    assert pile.est_vide() and len(pile) == 0
    pile.empiler(10)
    pile.empiler(20)
    assert len(pile) == 2
    assert pile.sommet() == 20
    assert pile.depiler() == 20
    assert pile.depiler() == 10
    assert pile.est_vide()


def test_pile_vide_leve_index_error():
    pile = Pile()
    with pytest.raises(IndexError):
        pile.depiler()
    with pytest.raises(IndexError):
        pile.sommet()


def test_file_fifo():
    file = File()
    assert file.est_vide() and len(file) == 0
    file.enfiler(10)
    file.enfiler(20)
    assert len(file) == 2
    assert file.tete() == 10
    assert file.defiler() == 10
    assert file.defiler() == 20
    assert file.est_vide()


def test_file_vide_leve_index_error():
    file = File()
    with pytest.raises(IndexError):
        file.defiler()
    with pytest.raises(IndexError):
        file.tete()


@pytest.mark.parametrize(
    "texte,attendu",
    [
        ("", True),
        ("()", True),
        ("([])", True),
        ("([]{})", True),
        ("((()))", True),
        ("(]", False),
        ("([)]", False),
        ("((", False),
        (")", False),
        (")(", False),
        ("((", False),
        ("abc", True),
    ],
)
def test_bien_parenthese(texte, attendu):
    assert bien_parenthese(texte) is attendu


@pytest.mark.parametrize(
    "elements,attendu",
    [
        ("", {}),
        ([], {}),
        ("abca", {"a": 2, "b": 1, "c": 1}),
        ([1, 1, 2], {1: 2, 2: 1}),
        ([1, 2, 3], {1: 1, 2: 1, 3: 1}),
    ],
)
def test_compter_occurrences(elements, attendu):
    assert compter_occurrences(elements) == attendu
