"""Arithmétique et évaluation de polynômes."""

from __future__ import annotations

from typing import List, Sequence, Union

Nombre = Union[int, float]


def puissance_rec(x: Nombre, n: int) -> Nombre:
    """Calcule ``x ** n`` par exponentiation rapide récursive.

    ``n`` doit être positif ou nul. Un seul appel récursif par niveau.

    Complexité : O(log n) en temps, O(log n) en espace (pile d'appels).

    Exemple :
        >>> puissance_rec(2, 10)
        1024
    """
    if n < 0:
        raise ValueError("l'exposant doit être positif ou nul")
    if n == 0:
        return 1
    y = puissance_rec(x, n // 2)
    return y * y if n % 2 == 0 else y * y * x


def puissance_iter(x: Nombre, n: int) -> Nombre:
    """Calcule ``x ** n`` par exponentiation rapide itérative.

    ``n`` doit être positif ou nul.

    Complexité : O(log n) en temps, O(1) en espace.

    Exemple :
        >>> puissance_iter(2, 10)
        1024
    """
    if n < 0:
        raise ValueError("l'exposant doit être positif ou nul")
    resultat: Nombre = 1
    while n > 0:
        if n % 2 == 1:
            resultat *= x
        x *= x
        n //= 2
    return resultat


def pgcd(a: int, b: int) -> int:
    """Calcule le plus grand commun diviseur par l'algorithme d'Euclide.

    Renvoie toujours un entier positif ; ``pgcd(0, 0)`` vaut 0.

    Complexité : O(log min(|a|, |b|)) en temps, O(1) en espace (récursion
    terminale).

    Exemple :
        >>> pgcd(48, 18)
        6
        >>> pgcd(0, 5)
        5
    """
    a, b = abs(a), abs(b)
    return a if b == 0 else pgcd(b, a % b)


def horner(coeffs: Sequence[float], x: float) -> float:
    """Évalue un polynôme par la méthode de Horner.

    ``coeffs`` est donnée du degré le plus bas au plus haut :
    ``coeffs = [a0, a1, ..., an]`` évalue ``a0 + a1*x + ... + an*x**n``.

    Complexité : O(n) en temps, O(1) en espace.

    Exemple :
        >>> horner([1, 2, 3], 2)
        17.0
    """
    resultat: float = 0.0
    for coefficient in reversed(coeffs):
        resultat = resultat * x + coefficient
    return resultat


def crible(n: int) -> List[int]:
    """Renvoie la liste des nombres premiers inférieurs ou égaux à ``n``.

    Complexité : O(n log log n) en temps, O(n) en espace.

    Exemple :
        >>> crible(20)
        [2, 3, 5, 7, 11, 13, 17, 19]
        >>> crible(1)
        []
    """
    if n < 2:
        return []
    est_premier = [True] * (n + 1)
    est_premier[0] = est_premier[1] = False
    for p in range(2, int(n**0.5) + 1):
        if est_premier[p]:
            for multiple in range(p * p, n + 1, p):
                est_premier[multiple] = False
    return [k for k in range(n + 1) if est_premier[k]]
