# Révision d'informatique CPGE — Sup → Spé

> Dépôt de révision d'informatique pour la CPGE scientifique (MPSI / PCSI / PSI,
> Maroc) : notebooks Jupyter, bibliothèque Python réutilisable, quiz interactif
> et exécutable distribué via GitHub Releases.

*(README provisoire — version complète à l'étape 7.)*

## Contenu

- `notebooks/` — chapitres pédagogiques (bases Python, structures de données,
  récursivité, algorithmique, NumPy/Matplotlib, SQL, exercices).
- `src/revision/` — fonctions réutilisables (tris, dichotomie, piles/files,
  exponentiation rapide, Horner, mémoïsation, graphes…).
- `quiz/` — quiz QCM par chapitre avec mode examen chronométré.
- `docs/guide_revision_cpge_info.pdf` — guide de révision imprimable.
- `tests/` — tests pytest du code et de la banque de questions.

## Démarrage rapide

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab notebooks/
```

## Licence

MIT — voir [LICENSE](LICENSE).
