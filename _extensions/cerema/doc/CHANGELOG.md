# Journal des modifications

## 1.3.1

- revealjs : la présentation est écrite dans `doc.diapo.html` (option `output-ext`), elle n'écrase plus `doc.html` du format `cerema-html`.
- revealjs : le contenu placé directement sous un titre de chapitre (`#` sans `##`) passe sur une diapositive de contenu au lieu de recouvrir le dégradé.
- revealjs : légendes et renvois en français (« Tableau 1 »).

## 1.3.0

- Tout ce qui concerne l'extension est rangé dans `_extensions/cerema/` : outils de maintenance (`outils/`) et leurs sources (`outils/sources/`), module Altair (`python/cerema_altair/`), documentation (`doc/`). À la racine du dépôt ne restent que le README, les exemples, l'environnement Python et le workflow.
- Polices et logos des formats HTML et revealjs intégrés à la feuille de style (`commun/cerema-ressources.scss`, généré par `outils/generer_ressources_web.py`) : Quarto ne copie plus `Marianne-*.otf` ni les logos à côté des documents rendus.
- Module `cerema_altair` installé par `uv sync` (paquet déclaré dans `pyproject.toml`) : importable depuis tout document du projet.

## 1.2.1

- Extension rangée par format : `commun/` (polices, images, jetons), `typst/`, `docx/`, `pptx/`, `html/`, `revealjs/`. Les noms de format et les en-têtes YAML des documents ne changent pas.

## 1.2.0

- Jetons de couleur générés depuis le design system (source unique).
- PDF : texte en Marianne (fournie par l'extension), titres en Arial, pagination après la couverture.
- Word : titres comme le PDF (indigo, sans filet corail), tableaux au modèle du PDF, encadrés au style du PDF.
- Word, correction : les titres n'avaient pas de couleur.
- HTML : sans barre ni filet corail sur les titres, contenu élargi, tableaux au modèle du PDF.
- PowerPoint : tableaux numérotés rendus avec leur légende et leurs renvois, disposition texte puis objet en pleine largeur, renvois en français.
- Workflow GitHub de rendu des cinq formats.
- Logos dans le pied de page des pages et sites HTML, pied de page clair.

## 1.1.0

- Formats `cerema-docx`, `cerema-pptx` et `cerema-html`.
- Graphiques Altair en PNG pour PDF, Word et PowerPoint.
- Format `cerema-typst` (rapport d'étude en PDF) ajouté à l'extension.

## 1.0.0

- Format `cerema-revealjs`.
