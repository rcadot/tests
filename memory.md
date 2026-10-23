# Mémoire de travail : modèle Quarto revealjs Cerema

## Source
- Design system « Cerema » : artifact https://claude.ai/artifact/Fn3QqmPyJigAviFLdWWthH
  (README, tokens.json, composants TitreDiapo, Chapitre, Chapo, Verbatim, Tableau, PiedDePage, Cover).
- Ressources téléchargées depuis son magasin d'assets (identifiants dans `project/design-system.json`).
- Polices Marianne Thin, ThinItalic, ExtraBoldItalic, MediumItalic, LightItalic non reprises (inutiles ici).

## Choix
- Diapositive 1280 x 720, `margin: 0`, `center: false` ; conversion 1 pt = 4/3 px depuis les positions du modèle (960 x 540 pt).
- `format-resources` d'une extension est copié à plat à côté du HTML rendu : les URL d'images et de polices
  vivent donc dans `cerema-header.html` (relatives au document), jamais dans le SCSS
  (le CSS compilé est dans `<doc>_files/libs/revealjs/dist/theme/`).
- Fonds par attributs `background-*` posés par `cerema.lua` (Pandoc les traduit en `data-background-*`).
- Habillage des diapositives de contenu et pied de page ajoutés en JS (`cerema-after-body.html`)
  pour qu'ils suivent la mise à l'échelle de reveal.js.
- En-tête de tableau : texte noir par défaut (7,4:1) ; `.entete-blanc` restitue le blanc du modèle.
- Contenu des diapositives de texte aligné sur le titre (113 px du bord), 64 px sous le titre ;
  hachures réduites à 140 px de haut (271 px dans le modèle) pour ne plus chevaucher le contenu.
- Bouton du menu déplacé en bas à droite pour libérer les logos.

## Vérification
- Rendu testé avec Quarto 1.6.42 (binaire installé dans le scratchpad, absent du système).
- Captures Playwright des 18 diapositives : couverture, contenu, chapitres, fonds teintés et fin conformes.
- Le graphique Altair n'a pas pu s'afficher dans le bac à sable (CDN Vega bloqué) ; le code s'exécute.

## Pistes
- Pictogrammes LinkedIn et YouTube de la page de fin : absents du design system, à ajouter.
- Disposition « couverture photo » et « texte et photo(s) » non transposées.
