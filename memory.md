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

## Format cerema-typst (rapport d'étude PDF)
- Ajouté dans la même extension (`contributes.formats.typst`) : `--to cerema-typst` ou `--to cerema-revealjs`.
- Images : chemin absolu Typst `/_extensions/cerema/fig/cerema/` (Quarto passe `--root` = projet).
  `format-resources` écarté pour Typst : copie à plat à côté du document.
- Pandoc échappe les métadonnées (`mon\_logo.png`) : la fonction `chemin()` retire les barres obliques.
- Callouts : `callout()` de Quarto redéfinie ; type retrouvé par `icon_color` (0758E5, 00A047, EB9113,
  CC1914, FC5300) ; encadrés référencés rendus par une règle `show figure` + `state("prefixe-callout")`.
- Tableaux Markdown : `set table` global ; `tableau_simple` et `tableau_scientifique` posent `fill: none`.
- Correspondance des images fournies supposée : marianne.png (bloc-marque seul), cerema.png (logo
  horizontal), fond.jpg (photo), fin_rapport.jpg (RF + Cerema). marianne.png converti depuis un .webp.
- Testé avec Quarto 1.7.32 / Typst 0.13.0 ; fontawesome remplacé par un paquet factice hors ligne.
- Pistes : numérotation des pages à partir du contenu ; polices Marianne pour le rapport (charte = Arial).

## Formats cerema-pptx, cerema-docx, cerema-html et graphiques Altair
- Une seule extension, cinq formats ; choix au rendu par `--to`. `rapport.qmd` déclare les cinq.
- pptx : `reference.pptx` généré par `outils/construire_reference_pptx.py` depuis
  `sources/Modele_Diaporama_Cerema_2026.potx` (type de contenu .potx -> .pptx, 26 diapositives retirées).
  Le modèle emploie des zones `body` pour les titres : Pandoc exige `title`/`ctrTitle` pour le titre et une
  zone sans type (`obj`) pour le contenu. 7 dispositions renommées (Title Slide, Title and Content,
  Section Header, Two Content, Comparison, Content with Caption, Blank).
  Pièges : « Slide texte 2 colonnes » a `numCol="2"` (à retirer après découpage en deux zones) ;
  une zone `dt` hérite d'une police à empattements (Marianne fixée).
- docx : `reference.docx` généré par `outils/construire_reference_docx.py` depuis la référence Pandoc.
  Quarto met légendes et encadrés dans des tableaux au style « Table » : le style Cerema est un style à part
  (« Tableau Cerema », identifiant `TableauCerema`), posé par `cerema-docx.lua` (attribut `custom-style`,
  qui doit valoir l'identifiant sans espace). LibreOffice ignore la trame `wholeTable` : trame sur les bandes.
- html : thème `cerema-html.scss` (cosmo), polices via `cerema-html-header.html` (chemins relatifs,
  `format-resources` copiés à côté de chaque page, sous-dossiers compris), bandeau de logos en
  `include-before-body`. Testé sur un site avec une page en sous-dossier.
- Altair : moteur « cerema » = `text/html` + `image/png` (vl-convert-python, polices Marianne enregistrées).
  Quarto prend le HTML pour html/revealjs, le PNG pour typst/docx/pptx. Le format d'image de Quarto
  (`QUARTO_FIG_FORMAT`) vaut png aussi en HTML : il ne permet pas de distinguer les sorties.
- Vérifications : rendus des 5 formats sur `rapport.qmd` et `template.qmd` ; pptx et docx contrôlés via
  LibreOffice (conversion PDF), html via Chromium. Non vérifié dans Word ni PowerPoint eux-mêmes.
- Limites : encadré référencé non pris en charge en pptx (avertissement Quarto) ; encadrés docx = rendu
  Quarto par défaut ; sommaire docx à mettre à jour à l'ouverture.
