"""Représentation et parcours de graphes non orientés.

Un graphe est représenté par un dictionnaire de listes de successeurs :
``{sommet: [voisins]}``.
"""

from __future__ import annotations

from collections import deque
from typing import Dict, Iterable, List, Mapping, Sequence, Set, Tuple

Graphe = Mapping[int, Sequence[int]]


def bfs(successeurs: Graphe, depart: int) -> Dict[int, int]:
    """Parcours en largeur : renvoie la distance en arêtes depuis ``depart``.

    Seuls les sommets atteignables figurent dans le résultat ; ``depart`` vaut 0.

    Complexité : O(V + E) en temps, O(V) en espace.

    Exemple :
        >>> bfs({0: [1], 1: [0, 2], 2: [1]}, 0)
        {0: 0, 1: 1, 2: 2}
    """
    distances: Dict[int, int] = {depart: 0}
    file = deque([depart])
    while file:
        sommet = file.popleft()
        for voisin in successeurs.get(sommet, ()):
            if voisin not in distances:
                distances[voisin] = distances[sommet] + 1
                file.append(voisin)
    return distances


def dfs(successeurs: Graphe, depart: int) -> List[int]:
    """Parcours en profondeur itératif : renvoie l'ordre de visite.

    Les voisins sont visités dans l'ordre de la liste de successeurs.

    Complexité : O(V + E) en temps, O(V) en espace.

    Exemple :
        >>> dfs({0: [1], 1: [0, 2], 2: [1]}, 0)
        [0, 1, 2]
    """
    vus: Set[int] = set()
    ordre: List[int] = []
    pile: List[int] = [depart]
    while pile:
        sommet = pile.pop()
        if sommet in vus:
            continue
        vus.add(sommet)
        ordre.append(sommet)
        pile.extend(reversed(successeurs.get(sommet, ())))
    return ordre


def composantes_connexes(successeurs: Graphe) -> List[Set[int]]:
    """Renvoie les composantes connexes du graphe (vu comme non orienté).

    Chaque sommet isolé forme sa propre composante.

    Complexité : O(V + E) en temps, O(V + E) en espace.

    Exemple :
        >>> sorted(map(sorted, composantes_connexes({0: [1], 1: [0], 2: []})))
        [[0, 1], [2]]
    """
    adjacence: Dict[int, Set[int]] = {u: set(voisins) for u, voisins in successeurs.items()}
    for u, voisins in list(adjacence.items()):
        for v in voisins:
            adjacence.setdefault(v, set()).add(u)

    vus: Set[int] = set()
    composantes: List[Set[int]] = []
    for depart in adjacence:
        if depart in vus:
            continue
        composante: Set[int] = set()
        pile = [depart]
        while pile:
            sommet = pile.pop()
            if sommet in vus:
                continue
            vus.add(sommet)
            composante.add(sommet)
            pile.extend(adjacence.get(sommet, ()))
        composantes.append(composante)
    return composantes


def est_connexe(successeurs: Graphe) -> bool:
    """Indique si le graphe possède au plus une composante connexe.

    Un graphe vide est considéré comme connexe (vacuously true).

    Complexité : O(V + E) en temps, O(V + E) en espace.

    Exemple :
        >>> est_connexe({0: [1], 1: [0]})
        True
        >>> est_connexe({0: [], 1: []})
        False
    """
    return len(composantes_connexes(successeurs)) <= 1


def _verifier_arete(u: int, v: int, n: int) -> None:
    if not (0 <= u < n and 0 <= v < n):
        raise ValueError(f"arête ({u}, {v}) hors des sommets 0..{n - 1}")


def matrice_adjacence(n: int, aretes: Iterable[Tuple[int, int]]) -> List[List[int]]:
    """Construit la matrice d'adjacence symétrique d'un graphe non orienté.

    Complexité : O(n² + E) en temps, O(n²) en espace.

    Exemple :
        >>> matrice_adjacence(2, [(0, 1)])
        [[0, 1], [1, 0]]
    """
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    matrice = [[0] * n for _ in range(n)]
    for u, v in aretes:
        _verifier_arete(u, v, n)
        matrice[u][v] = 1
        matrice[v][u] = 1
    return matrice


def liste_successeurs(n: int, aretes: Iterable[Tuple[int, int]]) -> Dict[int, List[int]]:
    """Construit les listes de successeurs d'un graphe non orienté.

    Tous les sommets ``0..n-1`` sont présents, même isolés.

    Complexité : O(n + E) en temps, O(n + E) en espace.

    Exemple :
        >>> liste_successeurs(2, [(0, 1)])
        {0: [1], 1: [0]}
    """
    if n < 0:
        raise ValueError("n doit être positif ou nul")
    successeurs: Dict[int, List[int]] = {sommet: [] for sommet in range(n)}
    for u, v in aretes:
        _verifier_arete(u, v, n)
        successeurs[u].append(v)
        successeurs[v].append(u)
    return successeurs
