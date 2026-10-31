#!/usr/bin/env python3
"""Quiz de révision d'informatique CPGE — interface terminal.

Bibliothèque standard uniquement.

Compatibilité PyInstaller : les questions sont lues dans
``sys._MEIPASS/questions`` lorsque l'application est figée ; l'historique est
écrit à côté de l'exécutable. En développement, l'historique est
``quiz/historique.json`` (gitignoré).
"""

from __future__ import annotations

import json
import random
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Callable, Iterable, Optional

LETTRES = "ABCD"
DUREE_EXAMEN_SECONDES = 300
NOMBRE_ALEATOIRE = 10
NOMBRE_EXAMEN = 20


# ---------------------------------------------------------------------------
# Chemins (compatibles PyInstaller)
# ---------------------------------------------------------------------------
def dossier_ressources() -> Path:
    """Dossier des ressources : ``sys._MEIPASS`` si figé, sinon le dossier du script."""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    return Path(__file__).resolve().parent


def dossier_questions() -> Path:
    """Dossier contenant les fichiers ``*.json`` de questions."""
    return dossier_ressources() / "questions"


def chemin_historique() -> Path:
    """Emplacement de l'historique des erreurs."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent / "historique.json"
    return Path(__file__).resolve().parent / "historique.json"


# ---------------------------------------------------------------------------
# Chargement des questions
# ---------------------------------------------------------------------------
def charger_questions(dossier: Optional[Path] = None) -> list[dict]:
    """Charge toutes les questions des fichiers JSON triés du dossier.

    Les fichiers illisibles ou mal formés sont ignorés silencieusement.
    """
    dossier = Path(dossier) if dossier is not None else dossier_questions()
    questions: list[dict] = []
    for fichier in sorted(dossier.glob("*.json")):
        try:
            contenu = json.loads(fichier.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(contenu, list):
            questions.extend(contenu)
    return questions


def lister_chapitres(questions: Iterable[dict]) -> list[str]:
    """Renvoie les chapitres dans l'ordre d'apparition, sans doublon."""
    chapitres: list[str] = []
    for question in questions:
        nom = question.get("chapitre")
        if nom and nom not in chapitres:
            chapitres.append(nom)
    return chapitres


# ---------------------------------------------------------------------------
# Historique des erreurs
# ---------------------------------------------------------------------------
def assurer_historique(chemin: Optional[Path] = None) -> Path:
    """Crée ``historique.json`` (liste vide) s'il n'existe pas encore."""
    fichier = Path(chemin) if chemin is not None else chemin_historique()
    if not fichier.exists():
        fichier.parent.mkdir(parents=True, exist_ok=True)
        fichier.write_text("[]\n", encoding="utf-8")
    return fichier


def charger_historique(chemin: Optional[Path] = None) -> list[dict]:
    """Lit l'historique ; renvoie ``[]`` si absent ou corrompu."""
    fichier = Path(chemin) if chemin is not None else chemin_historique()
    if not fichier.exists():
        return []
    try:
        contenu = json.loads(fichier.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return contenu if isinstance(contenu, list) else []


def _ecrire_historique(erreurs: list[dict], chemin: Optional[Path]) -> None:
    fichier = Path(chemin) if chemin is not None else chemin_historique()
    fichier.parent.mkdir(parents=True, exist_ok=True)
    fichier.write_text(
        json.dumps(erreurs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def enregistrer_erreur(question: dict, chemin: Optional[Path] = None) -> None:
    """Enregistre (ou remplace) une question ratée dans l'historique."""
    erreurs = [e for e in charger_historique(chemin) if e.get("id") != question.get("id")]
    erreurs.append(
        {
            "id": question.get("id"),
            "chapitre": question.get("chapitre"),
            "niveau": question.get("niveau"),
            "question": question.get("question"),
            "choix": question.get("choix"),
            "reponse": question.get("reponse"),
            "explication": question.get("explication"),
            "date": datetime.now().isoformat(timespec="seconds"),
        }
    )
    _ecrire_historique(erreurs, chemin)


def retirer_erreur(question_id: str, chemin: Optional[Path] = None) -> None:
    """Retire une question de l'historique (réussie lors d'une révision)."""
    fichier = Path(chemin) if chemin is not None else chemin_historique()
    if not fichier.exists():
        return
    erreurs = [e for e in charger_historique(chemin) if e.get("id") != question_id]
    _ecrire_historique(erreurs, chemin)


def questions_a_reviser(chemin: Optional[Path] = None) -> list[dict]:
    """Renvoie les questions ratées, dédoublonnées (dernière version gardée)."""
    derniere: dict[str, dict] = {}
    for entree in charger_historique(chemin):
        if not isinstance(entree, dict) or "id" not in entree:
            continue
        if not {"question", "choix", "reponse", "explication"} <= set(entree):
            continue
        derniere[entree["id"]] = entree
    return list(derniere.values())


# ---------------------------------------------------------------------------
# Logique du quiz
# ---------------------------------------------------------------------------
def normaliser_reponse(saisie: str, nb_choix: int = 4) -> Optional[int]:
    """Convertit ``"b"``, ``" B "``… en indice 0-3 ; ``None`` si invalide."""
    texte = saisie.strip().upper()
    if not texte:
        return None
    lettres = LETTRES[:nb_choix]
    if len(texte) == 1 and texte in lettres:
        return lettres.index(texte)
    return None


def calculer_score(resultats: Iterable[dict]) -> tuple[int, int]:
    """Renvoie ``(bonnes_réponses, total)``."""
    liste = list(resultats)
    return sum(1 for r in liste if r.get("correct")), len(liste)


def afficher_question(
    question: dict,
    numero: Optional[int] = None,
    total: Optional[int] = None,
    sortie: Optional[Callable[[str], None]] = None,
) -> None:
    """Affiche l'énoncé et les choix A/B/C/D."""
    sortie = sortie or print
    if numero is not None and total is not None:
        niveau = question.get("niveau", "?")
        sortie(f"\nQuestion {numero}/{total}  (niveau {niveau})")
    sortie(question["question"])
    for indice, choix in enumerate(question["choix"]):
        sortie(f"  {LETTRES[indice]}. {choix}")


def poser_question(
    question: dict,
    numero: Optional[int] = None,
    total: Optional[int] = None,
    entree: Optional[Callable[[str], str]] = None,
    sortie: Optional[Callable[[str], None]] = None,
    historique: Optional[Path] = None,
) -> bool:
    """Pose une question, affiche l'explication et renvoie si la réponse est juste.

    Les entrées vides ou invalides sont redemandées. ``EOFError`` est converti
    en ``KeyboardInterrupt`` pour être géré par le menu.
    """
    entree = entree or input
    sortie = sortie or print
    afficher_question(question, numero, total, sortie)

    index: Optional[int] = None
    while index is None:
        try:
            saisie = entree("Votre réponse (A-D) : ")
        except EOFError as exc:
            raise KeyboardInterrupt from exc
        index = normaliser_reponse(saisie, len(question["choix"]))
        if index is None:
            sortie("Réponse invalide : tapez A, B, C ou D.")

    correct = index == question["reponse"]
    if correct:
        sortie("✅ Correct !")
        retirer_erreur(question["id"], historique)
    else:
        sortie(f"❌ Incorrect. La bonne réponse était {LETTRES[question['reponse']]}.")
        enregistrer_erreur(question, historique)
    sortie(f"💡 {question['explication']}")
    return correct


def jouer_questions(
    questions: Iterable[dict],
    entree: Optional[Callable[[str], str]] = None,
    sortie: Optional[Callable[[str], None]] = None,
    historique: Optional[Path] = None,
    budget: Optional[float] = None,
    horloge: Callable[[], float] = time.monotonic,
) -> list[dict]:
    """Joue une série de questions et renvoie les résultats.

    Si ``budget`` (secondes) est fourni, la série s'arrête entre deux questions
    dès que le temps est écoulé.
    """
    entree = entree or input
    sortie = sortie or print
    liste = list(questions)
    resultats: list[dict] = []
    debut = horloge()
    for numero, question in enumerate(liste, start=1):
        if budget is not None:
            ecoule = horloge() - debut
            if ecoule >= budget:
                sortie("\n⏰ Temps écoulé !")
                break
            sortie(f"⏳ Temps restant : {max(0, int(budget - ecoule))} s")
        correct = poser_question(
            question, numero, len(liste), entree, sortie, historique
        )
        resultats.append({"question": question, "correct": correct})
    return resultats


def afficher_bilan(
    resultats: Iterable[dict], sortie: Optional[Callable[[str], None]] = None
) -> None:
    """Affiche le score final et un commentaire."""
    sortie = sortie or print
    bonnes, total = calculer_score(resultats)
    if total == 0:
        sortie("\nAucune question jouée.")
        return
    pourcentage = 100 * bonnes / total
    sortie(f"\n📊 Score final : {bonnes}/{total} ({pourcentage:.1f} %)")
    if pourcentage == 100:
        sortie("🏆 Excellent, tout est juste !")
    elif pourcentage >= 60:
        sortie("👍 Bien, continue à réviser.")
    else:
        sortie("📚 À revoir : essaie le mode « réviser mes erreurs ».")


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------
def menu_principal(
    entree: Optional[Callable[[str], str]] = None,
    sortie: Optional[Callable[[str], None]] = None,
    historique: Optional[Path] = None,
    graine: Optional[int] = None,
) -> None:
    """Boucle du menu jusqu'à ce que l'utilisateur quitte."""
    entree = entree or input
    sortie = sortie or print
    if graine is not None:
        random.seed(graine)

    questions = charger_questions()
    if not questions:
        sortie("Aucune question trouvée dans quiz/questions/.")
        return

    while True:
        sortie(
            "\n=== Quiz de révision CPGE — Informatique ===\n"
            "1. Réviser par chapitre\n"
            "2. Quiz aléatoire\n"
            "3. Mode examen chronométré\n"
            "4. Réviser mes erreurs\n"
            "5. Quitter"
        )
        choix = entree("Votre choix : ").strip()

        if choix == "1":
            chapitres = lister_chapitres(questions)
            sortie("\nChapitres disponibles :")
            for numero, chapitre in enumerate(chapitres, start=1):
                nombre = sum(1 for q in questions if q.get("chapitre") == chapitre)
                sortie(f"  {numero}. {chapitre} ({nombre} questions)")
            reponse = entree("Numéro du chapitre : ").strip()
            if not reponse.isdigit() or not 1 <= int(reponse) <= len(chapitres):
                sortie("Choix de chapitre invalide.")
                continue
            chapitre = chapitres[int(reponse) - 1]
            selection = [q for q in questions if q.get("chapitre") == chapitre]
            resultats = jouer_questions(
                selection, entree=entree, sortie=sortie, historique=historique
            )
            afficher_bilan(resultats, sortie)

        elif choix == "2":
            tirage = random.sample(questions, min(NOMBRE_ALEATOIRE, len(questions)))
            sortie(f"\n{len(tirage)} questions tirées au hasard.")
            resultats = jouer_questions(
                tirage, entree=entree, sortie=sortie, historique=historique
            )
            afficher_bilan(resultats, sortie)

        elif choix == "3":
            tirage = random.sample(questions, min(NOMBRE_EXAMEN, len(questions)))
            sortie(
                f"\nMode examen : {len(tirage)} questions, "
                f"{DUREE_EXAMEN_SECONDES // 60} minutes."
            )
            resultats = jouer_questions(
                tirage,
                entree=entree,
                sortie=sortie,
                historique=historique,
                budget=DUREE_EXAMEN_SECONDES,
            )
            afficher_bilan(resultats, sortie)

        elif choix == "4":
            a_reviser = questions_a_reviser(historique)
            if not a_reviser:
                sortie("\nAucune erreur enregistrée. Bravo !")
                continue
            sortie(f"\n{len(a_reviser)} question(s) à réviser.")
            resultats = jouer_questions(
                a_reviser, entree=entree, sortie=sortie, historique=historique
            )
            afficher_bilan(resultats, sortie)

        elif choix == "5":
            sortie("\nÀ bientôt !")
            return

        else:
            sortie("Choix invalide : tape un numéro entre 1 et 5.")


def main(argv: Optional[list[str]] = None, historique: Optional[Path] = None) -> int:
    """Point d'entrée : crée l'historique puis lance le menu."""
    assurer_historique(historique)
    try:
        menu_principal(historique=historique)
    except (KeyboardInterrupt, EOFError):
        print("\n\nÀ bientôt !")
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
