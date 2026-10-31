"""Algorithmes de tri et vérification d'ordre.

Toutes les fonctions travaillent sur des séquences comparables (nombres,
chaînes, tuples…). Les tris « en place » renvoient ``None`` et modifient la
liste reçue ; :func:`tri_fusion` renvoie une nouvelle liste.
"""

from __future__ import annotations

from typing import List, Sequence, TypeVar

T = TypeVar("T")


def fusion(gauche: Sequence[T], droite: Sequence[T]) -> List[T]:
    """Fusionne deux séquences triées en une seule liste triée.

    La comparaison ``<=`` garantit la stabilité : à égalité, l'élément de
    ``gauche`` est placé avant celui de ``droite``.

    Complexité : O(len(gauche) + len(droite)) en temps et en espace.

    Exemple :
        >>> fusion([1, 3, 5], [2, 4])
        [1, 2, 3, 4, 5]
    """
    resultat: List[T] = []
    i = j = 0
    while i < len(gauche) and j < len(droite):
        if gauche[i] <= droite[j]:
            resultat.append(gauche[i])
            i += 1
        else:
            resultat.append(droite[j])
            j += 1
    resultat.extend(gauche[i:])
    resultat.extend(droite[j:])
    return resultat


def tri_selection(liste: List[T]) -> None:
    """Trie ``liste`` en place par sélection du minimum restant.

    Complexité : O(n²) comparaisons dans tous les cas, O(1) espace
    auxiliaire. Le tri n'est pas stable.

    Exemple :
        >>> L = [3, 1, 2]
        >>> tri_selection(L)
        >>> L
        [1, 2, 3]
    """
    n = len(liste)
    for i in range(n - 1):
        indice_min = i
        for j in range(i + 1, n):
            if liste[j] < liste[indice_min]:
                indice_min = j
        liste[i], liste[indice_min] = liste[indice_min], liste[i]


def tri_insertion(liste: List[T]) -> None:
    """Trie ``liste`` en place par insertion dans la partie déjà triée.

    Complexité : O(n²) au pire (liste inversée), O(n) au meilleur cas
    (liste déjà triée), O(1) espace auxiliaire. Le tri est stable.

    Exemple :
        >>> L = [3, 1, 2]
        >>> tri_insertion(L)
        >>> L
        [1, 2, 3]
    """
    for i in range(1, len(liste)):
        valeur = liste[i]
        j = i - 1
        while j >= 0 and liste[j] > valeur:
            liste[j + 1] = liste[j]
            j -= 1
        liste[j + 1] = valeur


def tri_fusion(liste: Sequence[T]) -> List[T]:
    """Renvoie une nouvelle liste triée (diviser pour régner).

    La liste d'entrée n'est pas modifiée. Le tri est stable.

    Complexité : O(n log n) en temps dans tous les cas, O(n) en espace
    auxiliaire.

    Exemple :
        >>> tri_fusion([3, 1, 2])
        [1, 2, 3]
    """
    if len(liste) <= 1:
        return list(liste)
    milieu = len(liste) // 2
    return fusion(tri_fusion(liste[:milieu]), tri_fusion(liste[milieu:]))


def est_triee(liste: Sequence[T]) -> bool:
    """Indique si ``liste`` est croissante au sens large.

    Complexité : O(n) en temps, O(1) en espace.

    Exemple :
        >>> est_triee([1, 2, 2, 5])
        True
        >>> est_triee([2, 1])
        False
    """
    return all(liste[i] <= liste[i + 1] for i in range(len(liste) - 1))
