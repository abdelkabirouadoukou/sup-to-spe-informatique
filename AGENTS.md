# AGENTS.md — Guide pour les agents IA

Ce fichier décrit les conventions du dépôt **sup-to-spe-informatique** afin que
tout agent (ou contributeur) puisse intervenir sans casser la cohérence.

## Mission

Dépôt de révision d'informatique CPGE scientifique (passage Sup → Spé,
filières MPSI / PCSI / PSI, Maroc). Contenu : notebooks Jupyter pédagogiques,
bibliothèque `src/revision/`, quiz QCM interactif et exécutable distribué via
GitHub Releases.

## Structure

| Chemin | Rôle |
|---|---|
| `notebooks/00_notebook_original.ipynb` | Source d'origine, **ne jamais modifier** |
| `notebooks/01..07_*.ipynb` | Chapitres pédagogiques (définition, usage, code testé, pièges, astuce) |
| `src/revision/` | Fonctions réutilisables, docstrings + annotations de type |
| `quiz/questions/*.json` | Banque de questions, un fichier par chapitre |
| `quiz/quiz_app.py` | Application quiz (bibliothèque standard uniquement) |
| `tests/` | Tests pytest (code + validation des JSON) |
| `scripts/` | Scripts de build (`build_exe.bat` Windows, `build_exe.sh` macOS/Linux) |
| `docs/` | PDF source du guide de révision |
| `.github/workflows/build.yml` | CI : build Windows + release sur tag `v*` |

## Règles de contenu

- Chaque notion d'un notebook suit le schéma :
  **définition (2 lignes) → quand l'utiliser → code commenté avec `assert` → pièges → astuce**.
- Tout code de notebook doit s'exécuter sans erreur (`pytest --nbmake notebooks`).
- Le quiz utilise **uniquement la bibliothèque standard**.
- `quiz/historique.json` contient des données personnelles : il est **gitignoré**
  et doit être créé automatiquement par `quiz_app.py` s'il est absent.

## Règles de code

- Python ≥ 3.11, annotations de type systématiques dans `src/revision/`.
- Pas de dépendance externe dans `src/revision/` ni dans `quiz/`.
- Pas de commentaires inutiles ; les commentaires expliquent le *pourquoi*.
- Chemins compatibles PyInstaller via `sys._MEIPASS` pour les ressources.

## Commandes utiles

```bash
python3 -m venv .venv && source .venv/bin/activate   # Windows : .venv\Scripts\activate
pip install -r requirements.txt
pytest -q                                            # tests unitaires + JSON
pytest --nbmake notebooks -q                         # exécution des notebooks
python quiz/quiz_app.py                              # lancer le quiz
bash scripts/build_exe.sh                            # build local macOS/Linux
scripts\build_exe.bat                                # build Windows (local)
```

## Git

- Un commit par étape fonctionnelle, message en français.
- Ne jamais committer `dist/`, `build/`, `.venv/`, `*.spec`, `quiz/historique.json`.
- Ne jamais modifier ni déplacer les fichiers sources de l'utilisateur
  (`~/Downloads`).

## Système de développement

Le poste principal est **macOS** : le `.exe` Windows n'est produit que par la CI
(`windows-latest`) sur tag `v*`. En local on teste `scripts/build_exe.sh`.
