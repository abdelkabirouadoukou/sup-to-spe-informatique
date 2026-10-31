"""Validation structurelle des banques de questions JSON."""

import json
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]
DOSSIER = RACINE / "quiz" / "questions"
FICHIERS = sorted(DOSSIER.glob("*.json"))
CHAMPS = {"id", "chapitre", "niveau", "question", "choix", "reponse", "explication"}


def _toutes_les_questions():
    questions = []
    for fichier in FICHIERS:
        questions.extend(json.loads(fichier.read_text(encoding="utf-8")))
    return questions


def test_sept_fichiers_de_questions():
    assert len(FICHIERS) == 7, [f.name for f in FICHIERS]


@pytest.mark.parametrize("fichier", FICHIERS, ids=lambda f: f.name)
def test_structure_du_fichier(fichier):
    contenu = json.loads(fichier.read_text(encoding="utf-8"))
    assert isinstance(contenu, list)
    assert len(contenu) >= 15

    for question in contenu:
        assert set(question) == CHAMPS
        assert isinstance(question["id"], str) and question["id"]
        assert isinstance(question["chapitre"], str) and question["chapitre"]
        assert isinstance(question["niveau"], int) and not isinstance(
            question["niveau"], bool
        )
        assert question["niveau"] in (1, 2, 3)
        assert isinstance(question["question"], str) and question["question"].strip()
        assert isinstance(question["explication"], str) and question["explication"].strip()

        choix = question["choix"]
        assert isinstance(choix, list) and len(choix) == 4
        assert all(isinstance(c, str) and c.strip() for c in choix)
        assert len(set(choix)) == 4

        assert isinstance(question["reponse"], int) and not isinstance(
            question["reponse"], bool
        )
        assert 0 <= question["reponse"] < len(choix)


def test_ids_uniques_globalement():
    ids = [question["id"] for question in _toutes_les_questions()]
    assert len(ids) == len(set(ids))


def test_questions_uniques_par_fichier():
    for fichier in FICHIERS:
        contenu = json.loads(fichier.read_text(encoding="utf-8"))
        enonces = [question["question"] for question in contenu]
        assert len(enonces) == len(set(enonces)), fichier.name


def test_bonne_reponse_repartie_sur_abcd():
    for fichier in FICHIERS:
        contenu = json.loads(fichier.read_text(encoding="utf-8"))
        positions = {question["reponse"] for question in contenu}
        assert positions == {0, 1, 2, 3}, fichier.name


def test_au_moins_15_questions_par_chapitre():
    for fichier in FICHIERS:
        contenu = json.loads(fichier.read_text(encoding="utf-8"))
        assert len(contenu) >= 15, fichier.name


def test_questions_de_code_contiennent_un_bloc_python():
    questions = _toutes_les_questions()
    code = [q for q in questions if "```python" in q["question"]]
    assert len(code) >= 20
    for question in code:
        assert question["question"].count("```") >= 2
