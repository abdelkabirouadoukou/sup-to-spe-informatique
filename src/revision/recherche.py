"""Recherche d'un élément dans une séquence."""

from __future__ import annotations

from typing import Optional, Sequence, TypeVar

T = TypeVar("T")


def dichotomie(x: T, liste: Sequence[T]) -> Optional[int]:
    """Cherche ``x`` dans ``liste`` **triée** par dichotomie.

    Renvoie un indice ``i`` tel que ``liste[i] == x``, ou ``None`` si absent.
    Si ``x`` est présent plusieurs fois, l'indice renvoyé n'est pas garanti.

    Complexité : O(log n) en temps, O(1) en espace.

    Exemple :
        >>> dichotomie(7, [1, 3, 5, 7, 9])
        3
        >>> dichotomie(4, [1, 3, 5, 7, 9]) is None
        True
    """
    gauche, droite = 0, len(liste) - 1
    while gauche <= droite:
        milieu = (gauche + droite) // 2
        if liste[milieu] == x:
            return milieu
        if liste[milieu] < x:
            gauche = milieu + 1
        else:
            droite = milieu - 1
    return None


def recherche_lineaire(x: T, liste: Sequence[T]) -> Optional[int]:
    """Cherche ``x`` dans ``liste`` par parcours séquentiel.

    Renvoie l'indice de la **première** occurrence, ou ``None`` si absent.
    Aucune hypothèse d'ordre n'est nécessaire.

    Complexité : O(n) en temps, O(1) en espace.

    Exemple :
        >>> recherche_lineaire(2, [1, 2, 2, 3])
        1
    """
    for indice, valeur in enumerate(liste):
        if valeur == x:
            return indice
    return None
