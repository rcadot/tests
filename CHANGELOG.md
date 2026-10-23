# Journal des modifications

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
