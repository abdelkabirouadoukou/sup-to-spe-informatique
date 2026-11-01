"""Tests de la logique du quiz, sans interaction réelle."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("quiz_app", RACINE / "quiz" / "quiz_app.py")
quiz_app = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(quiz_app)


def question(reponse=0, qid="test-1"):
    return {
        "id": qid,
        "chapitre": "Test",
        "niveau": 1,
        "question": "Question de test ?",
        "choix": ["A", "B", "C", "D"],
        "reponse": reponse,
        "explication": "Explication de test.",
    }


def entree_depuis(valeurs):
    it = iter(valeurs)

    def _entree(_prompt):
        return next(it)

    return _entree


def collecteur():
    messages = []

    def _sortie(message):
        messages.append(str(message))

    return messages, _sortie


@pytest.mark.parametrize(
    "saisie,attendu",
    [
        ("a", 0),
        ("A", 0),
        (" B ", 1),
        ("c", 2),
        ("d", 3),
        ("", None),
        ("   ", None),
        ("z", None),
        ("AB", None),
        ("1", None),
    ],
)
def test_normaliser_reponse(saisie, attendu):
    assert quiz_app.normaliser_reponse(saisie, 4) == attendu


def test_calculer_score():
    assert quiz_app.calculer_score([]) == (0, 0)
    resultats = [{"correct": True}, {"correct": False}, {"correct": True}]
    assert quiz_app.calculer_score(resultats) == (2, 3)


def test_charger_questions(tmp_path):
    (tmp_path / "a.json").write_text(
        json.dumps([question(qid="a-1")]), encoding="utf-8"
    )
    (tmp_path / "b.json").write_text(
        json.dumps([question(qid="b-1"), question(qid="b-2")]), encoding="utf-8"
    )
    (tmp_path / "casse.json").write_text("{ pas du json", encoding="utf-8")
    (tmp_path / "objet.json").write_text(json.dumps({"x": 1}), encoding="utf-8")

    questions = quiz_app.charger_questions(tmp_path)
    assert [q["id"] for q in questions] == ["a-1", "b-1", "b-2"]


def test_lister_chapitres():
    questions = [question(qid="1"), question(qid="2")]
    questions[1]["chapitre"] = "Autre"
    assert quiz_app.lister_chapitres(questions) == ["Test", "Autre"]


def test_assurer_historique_cree_un_fichier(tmp_path):
    chemin = tmp_path / "sous" / "historique.json"
    assert not chemin.exists()
    quiz_app.assurer_historique(chemin)
    assert chemin.exists()
    assert json.loads(chemin.read_text(encoding="utf-8")) == []


def test_historique_absent_ou_corrompu(tmp_path):
    assert quiz_app.charger_historique(tmp_path / "absent.json") == []
    casse = tmp_path / "casse.json"
    casse.write_text("{ pas du json", encoding="utf-8")
    assert quiz_app.charger_historique(casse) == []


def test_enregistrer_et_charger_erreur(tmp_path):
    chemin = tmp_path / "historique.json"
    quiz_app.enregistrer_erreur(question(qid="x"), chemin)

    erreurs = quiz_app.charger_historique(chemin)
    assert len(erreurs) == 1
    entree = erreurs[0]
    assert entree["id"] == "x"
    assert entree["question"] == "Question de test ?"
    assert entree["reponse"] == 0
    assert "date" in entree


def test_enregistrer_deux_fois_remplace(tmp_path):
    chemin = tmp_path / "historique.json"
    quiz_app.enregistrer_erreur(question(qid="x"), chemin)
    quiz_app.enregistrer_erreur(question(qid="x"), chemin)
    assert len(quiz_app.charger_historique(chemin)) == 1


def test_retirer_erreur(tmp_path):
    chemin = tmp_path / "historique.json"
    quiz_app.enregistrer_erreur(question(qid="x"), chemin)
    quiz_app.enregistrer_erreur(question(qid="y"), chemin)
    quiz_app.retirer_erreur("x", chemin)
    assert [e["id"] for e in quiz_app.charger_historique(chemin)] == ["y"]


def test_questions_a_reviser_dedoublonne(tmp_path):
    chemin = tmp_path / "historique.json"
    quiz_app.enregistrer_erreur(question(qid="x"), chemin)
    quiz_app.enregistrer_erreur(question(qid="y"), chemin)
    # entrée invalide ignorée
    erreurs = quiz_app.charger_historique(chemin)
    erreurs.append({"id": "invalide"})
    chemin.write_text(json.dumps(erreurs), encoding="utf-8")

    a_reviser = quiz_app.questions_a_reviser(chemin)
    assert {q["id"] for q in a_reviser} == {"x", "y"}


def test_poser_question_entrees_invalides_puis_valide(tmp_path):
    messages, sortie = collecteur()
    correct = quiz_app.poser_question(
        question(reponse=1),
        entree=entree_depuis(["", "z", "b"]),
        sortie=sortie,
        historique=tmp_path / "historique.json",
    )
    assert correct is True
    assert sum("Réponse invalide" in m for m in messages) == 2
    assert any("Correct" in m for m in messages)
    assert any("Explication de test." in m for m in messages)


def test_mauvaise_reponse_enregistre_erreur(tmp_path):
    chemin = tmp_path / "historique.json"
    messages, sortie = collecteur()
    correct = quiz_app.poser_question(
        question(reponse=0),
        entree=entree_depuis(["B"]),
        sortie=sortie,
        historique=chemin,
    )
    assert correct is False
    assert any("Incorrect" in m for m in messages)
    assert len(quiz_app.charger_historique(chemin)) == 1


def test_bonne_reponse_retire_erreur(tmp_path):
    chemin = tmp_path / "historique.json"
    quiz_app.enregistrer_erreur(question(reponse=0), chemin)
    _, sortie = collecteur()
    correct = quiz_app.poser_question(
        question(reponse=0),
        entree=entree_depuis(["A"]),
        sortie=sortie,
        historique=chemin,
    )
    assert correct is True
    assert quiz_app.charger_historique(chemin) == []


def test_jouer_questions_budget(tmp_path):
    messages, sortie = collecteur()
    questions = [question(qid=f"q{i}") for i in range(3)]
    horloge = iter([0.0, 5.0, 20.0, 30.0])

    resultats = quiz_app.jouer_questions(
        questions,
        entree=entree_depuis(["A", "A", "A"]),
        sortie=sortie,
        historique=tmp_path / "historique.json",
        budget=15.0,
        horloge=lambda: next(horloge),
    )
    assert len(resultats) == 1
    assert any("Temps écoulé" in m for m in messages)


def test_jouer_questions_sans_budget(tmp_path):
    _, sortie = collecteur()
    questions = [question(qid=f"q{i}") for i in range(3)]
    resultats = quiz_app.jouer_questions(
        questions,
        entree=entree_depuis(["A", "A", "A"]),
        sortie=sortie,
        historique=tmp_path / "historique.json",
    )
    assert len(resultats) == 3
    assert quiz_app.calculer_score(resultats) == (3, 3)


def test_afficher_bilan():
    messages, sortie = collecteur()
    quiz_app.afficher_bilan([{"correct": True}, {"correct": False}], sortie)
    texte = "\n".join(messages)
    assert "1/2" in texte
    assert "50.0 %" in texte


def test_menu_choix_invalide_puis_quitter(tmp_path):
    messages, sortie = collecteur()
    quiz_app.menu_principal(
        entree=entree_depuis(["9", "5"]),
        sortie=sortie,
        historique=tmp_path / "historique.json",
    )
    texte = "\n".join(messages)
    assert "Choix invalide" in texte
    assert "À bientôt" in texte


def test_chemins_pyinstaller(monkeypatch, tmp_path):
    executable = tmp_path / "dist" / "quiz_revision.exe"
    monkeypatch.setattr(quiz_app.sys, "frozen", True, raising=False)
    monkeypatch.setattr(quiz_app.sys, "_MEIPASS", str(tmp_path / "meipass"), raising=False)
    monkeypatch.setattr(quiz_app.sys, "executable", str(executable), raising=False)

    assert quiz_app.dossier_ressources() == tmp_path / "meipass"
    assert quiz_app.dossier_questions() == tmp_path / "meipass" / "questions"
    assert quiz_app.chemin_historique() == executable.resolve().parent / "historique.json"


def test_self_test_ok(monkeypatch, capsys):
    monkeypatch.setattr(
        quiz_app,
        "charger_questions",
        lambda: [question(qid=f"q{i}") for i in range(quiz_app.NOMBRE_QUESTIONS_ATTENDU)],
    )
    assert quiz_app.main(["--self-test"]) == 0
    assert capsys.readouterr().out.strip() == "OK"


def test_self_test_mauvais_nombre(monkeypatch, capsys):
    monkeypatch.setattr(quiz_app, "charger_questions", lambda: [question()])
    assert quiz_app.main(["--self-test"]) == 1
    assert "ÉCHEC" in capsys.readouterr().out


def test_self_test_index_invalide(monkeypatch, capsys):
    questions = [question(qid=f"q{i}") for i in range(quiz_app.NOMBRE_QUESTIONS_ATTENDU)]
    questions[0]["reponse"] = 9
    monkeypatch.setattr(quiz_app, "charger_questions", lambda: questions)
    assert quiz_app.main(["--self-test"]) == 1
    assert "index invalide" in capsys.readouterr().out


def test_self_test_en_sous_processus():
    resultat = subprocess.run(
        [sys.executable, str(RACINE / "quiz" / "quiz_app.py"), "--self-test"],
        capture_output=True,
        text=True,
        cwd=str(RACINE),
    )
    assert resultat.returncode == 0, resultat.stderr
    assert resultat.stdout.strip() == "OK"
