"""Structures de données élémentaires : pile, file et utilitaires."""

from __future__ import annotations

from collections import deque
from typing import Deque, Dict, Generic, Iterable, List, TypeVar

T = TypeVar("T")


class Pile(Generic[T]):
    """Pile LIFO (dernier entré, premier sorti).

    Implémentée sur une liste Python : ``empiler`` et ``depiler`` sont en O(1)
    amorti.

    Exemple :
        >>> p = Pile()
        >>> p.empiler(1)
        >>> p.empiler(2)
        >>> p.depiler()
        2
    """

    def __init__(self) -> None:
        self._elements: List[T] = []

    def empiler(self, valeur: T) -> None:
        """Ajoute ``valeur`` au sommet (O(1) amorti)."""
        self._elements.append(valeur)

    def depiler(self) -> T:
        """Retire et renvoie le sommet (O(1)).

        Lève ``IndexError`` si la pile est vide.
        """
        if not self._elements:
            raise IndexError("dépiler une pile vide")
        return self._elements.pop()

    def sommet(self) -> T:
        """Renvoie le sommet sans le retirer (O(1)).

        Lève ``IndexError`` si la pile est vide.
        """
        if not self._elements:
            raise IndexError("sommet d'une pile vide")
        return self._elements[-1]

    def est_vide(self) -> bool:
        """Indique si la pile ne contient aucun élément (O(1))."""
        return not self._elements

    def __len__(self) -> int:
        return len(self._elements)

    def __repr__(self) -> str:
        return f"Pile({self._elements!r})"


class File(Generic[T]):
    """File FIFO (premier entré, premier sorti).

    Implémentée sur ``collections.deque`` : ``enfiler`` et ``defiler`` sont en
    O(1) aux deux extrémités.

    Exemple :
        >>> f = File()
        >>> f.enfiler(1)
        >>> f.enfiler(2)
        >>> f.defiler()
        1
    """

    def __init__(self) -> None:
        self._elements: Deque[T] = deque()

    def enfiler(self, valeur: T) -> None:
        """Ajoute ``valeur`` en queue (O(1))."""
        self._elements.append(valeur)

    def defiler(self) -> T:
        """Retire et renvoie la tête (O(1)).

        Lève ``IndexError`` si la file est vide.
        """
        if not self._elements:
            raise IndexError("défiler une file vide")
        return self._elements.popleft()

    def tete(self) -> T:
        """Renvoie la tête sans la retirer (O(1)).

        Lève ``IndexError`` si la file est vide.
        """
        if not self._elements:
            raise IndexError("tête d'une file vide")
        return self._elements[0]

    def est_vide(self) -> bool:
        """Indique si la file ne contient aucun élément (O(1))."""
        return not self._elements

    def __len__(self) -> int:
        return len(self._elements)

    def __repr__(self) -> str:
        return f"File({list(self._elements)!r})"


def bien_parenthese(texte: str) -> bool:
    """Vérifie que les parenthèses, crochets et accolades sont équilibrés.

    Complexité : O(len(texte)) en temps, O(len(texte)) en espace.

    Exemple :
        >>> bien_parenthese("([]{})")
        True
        >>> bien_parenthese("([)]")
        False
    """
    appariement = {")": "(", "]": "[", "}": "{"}
    pile: List[str] = []
    for caractere in texte:
        if caractere in "([{":
            pile.append(caractere)
        elif caractere in appariement:
            if not pile or pile.pop() != appariement[caractere]:
                return False
    return not pile


def compter_occurrences(elements: Iterable[T]) -> Dict[T, int]:
    """Compte le nombre d'occurrences de chaque élément.

    Complexité : O(n) en temps, O(k) en espace (k éléments distincts).

    Exemple :
        >>> compter_occurrences("abca")
        {'a': 2, 'b': 1, 'c': 1}
    """
    compteur: Dict[T, int] = {}
    for element in elements:
        compteur[element] = compteur.get(element, 0) + 1
    return compteur
