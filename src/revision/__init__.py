"""Bibliothèque de révision d'informatique CPGE (Sup → Spé).

Fonctions réutilisables, sans dépendance externe, utilisées par les notebooks
et les tests. Installation éditable :

    pip install -e .

Puis, depuis n'importe où :

    from revision import dichotomie, tri_fusion, puissance_iter

Version : 0.2.0
"""

from __future__ import annotations

from .arithmetique import crible, horner, pgcd, puissance_iter, puissance_rec
from .graphes import (
    bfs,
    composantes_connexes,
    dfs,
    est_connexe,
    liste_successeurs,
    matrice_adjacence,
)
from .recherche import dichotomie, recherche_lineaire
from .recursivite import (
    a_doublon,
    factorielle,
    fib_memo,
    fib_naif,
    hanoi_coups,
    maximum_dichotomie,
    renverse,
    somme_chiffres,
)
from .structures import File, Pile, bien_parenthese, compter_occurrences
from .tris import est_triee, fusion, tri_fusion, tri_insertion, tri_selection

__version__ = "0.2.0"

__all__ = [
    # arithmetique
    "crible",
    "horner",
    "pgcd",
    "puissance_iter",
    "puissance_rec",
    # graphes
    "bfs",
    "composantes_connexes",
    "dfs",
    "est_connexe",
    "liste_successeurs",
    "matrice_adjacence",
    # recherche
    "dichotomie",
    "recherche_lineaire",
    # recursivite
    "a_doublon",
    "factorielle",
    "fib_memo",
    "fib_naif",
    "hanoi_coups",
    "maximum_dichotomie",
    "renverse",
    "somme_chiffres",
    # structures
    "File",
    "Pile",
    "bien_parenthese",
    "compter_occurrences",
    # tris
    "est_triee",
    "fusion",
    "tri_fusion",
    "tri_insertion",
    "tri_selection",
    "__version__",
]
