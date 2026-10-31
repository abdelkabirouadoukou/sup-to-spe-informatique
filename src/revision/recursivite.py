"""Fonctions récursives classiques de concours."""

from __future__ import annotations

from functools import lru_cache
from typing import List, Optional, Sequence, Tuple, TypeVar

T = TypeVar("T")


def factorielle(n: int) -> int:
    """Calcule ``n!`` de façon récursive.

    Complexité : O(n) en temps, O(n) en espace (pile d'appels).

    Exemple :
        >>> factorielle(5)
        120
    """
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    if n == 0:
        return 1
    return n * factorielle(n - 1)


def somme_chiffres(n: int) -> int:
    """Renvoie la somme des chiffres de l'entier positif ``n``.

    Complexité : O(log n) en temps, O(log n) en espace.

    Exemple :
        >>> somme_chiffres(1234)
        10
    """
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    return n if n < 10 else n % 10 + somme_chiffres(n // 10)


def fib_naif(n: int) -> int:
    """Renvoie le n-ième terme de Fibonacci (version naïve).

    Complexité : O(φⁿ) en temps (exponentiel), O(n) en espace.

    Exemple :
        >>> fib_naif(15)
        610
    """
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    return n if n < 2 else fib_naif(n - 1) + fib_naif(n - 2)


@lru_cache(maxsize=None)
def fib_memo(n: int) -> int:
    """Renvoie le n-ième terme de Fibonacci (version mémoïsée).

    Complexité : O(n) en temps, O(n) en espace.

    Exemple :
        >>> fib_memo(90)
        2880067194370816120
    """
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    return n if n < 2 else fib_memo(n - 1) + fib_memo(n - 2)


def hanoi_coups(
    n: int,
    depart: str = "A",
    intermediaire: str = "B",
    arrivee: str = "C",
) -> List[Tuple[str, str]]:
    """Renvoie la liste des déplacements pour résoudre les tours de Hanoï.

    Chaque déplacement est un couple ``(source, destination)``.

    Complexité : O(2ⁿ) en temps, O(2ⁿ) en espace (taille du résultat).

    Exemple :
        >>> hanoi_coups(1)
        [('A', 'C')]
    """
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    coups: List[Tuple[str, str]] = []

    def deplacer(k: int, source: str, via: str, cible: str) -> None:
        if k == 0:
            return
        deplacer(k - 1, source, cible, via)
        coups.append((source, cible))
        deplacer(k - 1, via, source, cible)

    deplacer(n, depart, intermediaire, arrivee)
    return coups


def maximum_dichotomie(
    liste: Sequence[T], gauche: int = 0, droite: Optional[int] = None
) -> T:
    """Renvoie le maximum de ``liste[gauche..droite]`` par diviser pour régner.

    La liste doit être non vide.

    Complexité : O(n) en temps (T(n) = 2T(n/2) + O(1)), O(log n) en espace.

    Exemple :
        >>> maximum_dichotomie([3, 9, 2, 7])
        9
    """
    if not liste:
        raise ValueError("la liste ne peut pas être vide")
    if droite is None:
        droite = len(liste) - 1
    if gauche == droite:
        return liste[gauche]
    milieu = (gauche + droite) // 2
    return max(
        maximum_dichotomie(liste, gauche, milieu),
        maximum_dichotomie(liste, milieu + 1, droite),
    )


def renverse(liste: Sequence[T]) -> List[T]:
    """Renvoie une nouvelle liste inversée, sans modifier l'originale.

    Complexité : O(n) en temps, O(n) en espace.

    Exemple :
        >>> L = [1, 2, 3]
        >>> renverse(L)
        [3, 2, 1]
        >>> L
        [1, 2, 3]
    """
    return list(liste)[::-1]


def a_doublon(liste: Sequence[T]) -> bool:
    """Indique si ``liste`` contient au moins deux éléments égaux.

    Les éléments doivent être hachables (utilise un ensemble).

    Complexité : O(n) en temps moyen, O(n) en espace.

    Exemple :
        >>> a_doublon([1, 2, 1])
        True
        >>> a_doublon([1, 2, 3])
        False
    """
    return len(set(liste)) != len(liste)
