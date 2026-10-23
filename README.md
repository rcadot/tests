# Modèles Quarto Cerema : présentations, rapports, documents et pages web

Ce dépôt fournit l'extension Quarto `cerema`, qui définit cinq formats : `cerema-revealjs` et `cerema-pptx` (présentations), `cerema-typst` (rapport d'étude en PDF, compilé par Typst), `cerema-docx` (document Word) et `cerema-html` (pages et sites HTML). Elle transpose le design system du Cerema, tel que le décrit le modèle PowerPoint « Diaporama Cerema 2026 » : couleurs indigo et corail, dégradé signature, police Marianne pour le texte courant, Arial gras pour les titres et Spectral italique pour le verbatim. La diapositive est au format 16:9, soit 1280 x 720 px ; l'échelle retenue fait correspondre 1 pt du modèle (960 x 540 pt) à 4/3 px.

## Installation

Deux voies sont possibles.

- Copier le dossier `_extensions/cerema` dans le dossier `_extensions` du projet cible.
- Exécuter `quarto use template rcadot/tests` dans un dossier vide. Cette commande suppose que le dépôt soit publié sur GitHub sous ce nom ; elle n'est donc à utiliser que dans ce cas.

L'extension requiert Quarto 1.6 ou supérieur, car le format Typst exige Typst 0.12, fourni à partir de cette version. Le rendu a été testé avec Quarto 1.7.32. L'en-tête YAML minimal d'une présentation est le suivant :

```yaml
---
title: "Titre de la présentation"
format: cerema-revealjs
---
```

Le fichier `template.qmd` présente l'ensemble des dispositions et des composants.

## Environnement Python

Python n'est nécessaire que pour les graphiques et pour la régénération des fichiers de référence. Les dépendances (`altair`, `polars`, `jupyter`, `pyarrow`, `vl-convert-python`) sont déclarées dans `pyproject.toml`, qui exige Python 3.10 ou supérieur. Les paquets `python-pptx` et `python-docx` sont des dépendances de développement (groupe `dev`), utiles uniquement pour régénérer les fichiers de référence. Les dépendances s'installent avec `uv` :

```sh
uv sync
QUARTO_PYTHON=.venv/bin/python quarto render template.qmd
```

## Métadonnées de couverture

La couverture est produite automatiquement à partir de l'en-tête YAML.

```yaml
title: "Titre de la présentation"
subtitle: "Sous-titre de la présentation"
author:
  - name: Prénom Nom
    affiliations:
      - name: Cerema
date: today
partenaires:
  - images/partenaire-1.png
```

- `title` et `subtitle` : titre en capitales et sous-titre.
- `author` : pour chaque auteur, `name` et, le cas échéant, `affiliations` (liste d'objets portant un `name`), affichées à la suite du nom.
- `date` : l'extension règle le format d'affichage sur `MMMM YYYY` et la langue sur `fr` (par exemple « Octobre 2026 »).
- `partenaires` : liste de chemins d'images, affichées en bas de la couverture, avec une hauteur de 56 px.

## Dispositions

| Disposition | Syntaxe | Rendu |
|---|---|---|
| Couverture | automatique, d'après les métadonnées | Bloc-marque RF, logo Cerema, halo, titre, auteurs, date |
| Diapositive de contenu | `## Titre` | Barre corail, titre en capitales, hachures, halo, pied de page avec bloc-marque RF, logo Cerema et numéro de page |
| Chapitre | `# Titre` ou `## Titre {.chapitre}` | Dégradé corail vers indigo-profond, titre blanc centré verticalement |
| Chapitre avec sommaire | `# Titre {.chapitre-sommaire}` suivi d'une liste | Dégradé sur la moitié gauche, fond blanc à droite portant la liste |
| Sommaire | `## Sommaire / ordre du jour {.sommaire}` suivi d'une liste numérotée | Diapositive de contenu avec liste numérotée en grands caractères |
| Fonds teintés | `{.fond-lavande}`, `{.fond-jaune}`, `{.fond-corail}`, `{.fond-olive}`, `{.fond-vert}`, `{.fond-bleu}` sur un titre de niveau 2 | Fond pâle ; la couleur du titre et de la barre suit le fond |
| Page de fin | `## Merci pour votre attention {.fin}` | Dégradé à 73 % d'opacité, texte et liens blancs |
| Sans pied de page | `{.sans-pied}` | Retire de la diapositive le pied de page et l'habillage de contenu |

Les diapositives à fond teinté conservent l'habillage et le pied de page des diapositives de contenu. La classe `.sans-pied` s'ajoute au titre, par exemple `## Titre {.sans-pied}`.

## Composants

Les composants s'écrivent sous forme de divs Quarto.

- `.chapo` : encadré à filet indigo, destiné au message clé. Un premier segment en gras sert d'intitulé.
- `.verbatim` : citation en Spectral italique indigo, introduite par une citation Markdown (`>`). Une div `.attribution` imbriquée porte l'auteur, la fonction et l'organisme.
- `.source` et `.mention` : mentions en petits caractères, par exemple pour la source d'un chiffre.
- `.encadre` : bloc de mise en avant sur fond corail pâle.
- Tableaux Markdown : en-tête corail, lignes en gris clair et libellés de la première colonne en indigo. Le texte de l'en-tête est noir, car le blanc du modèle sur le corail n'atteint pas le contraste requis. La classe `.entete-blanc`, posée sur le tableau ou sur une div qui l'enveloppe, rétablit le texte blanc du modèle.
- Colonnes : les colonnes Quarto standard (`.columns` et `.column`) sont disposées en flex ; la gouttière se répartit automatiquement entre les colonnes.

```markdown
:::: {.columns}

::: {.column width="38%"}
::: {.chapo}
**Chapô**

Message clé de la diapositive.
:::
:::

::: {.column width="58%"}
Texte de développement.
:::

::::
```

## Graphiques

Le module `cerema_altair.py` enregistre le thème Altair « cerema » et l'active dès son import. Il définit la police Marianne, des axes sans grille verticale, des filets gris clair et une palette catégorielle dans l'ordre indigo-profond, corail, jaune, olive, vert, bleu. Les barres sont en indigo-profond par défaut.

```python
import altair as alt
import cerema_altair  # noqa: F401
```

Les graphiques Altair chargent Vega depuis un CDN : une connexion est donc nécessaire lors de la projection.

Le module active aussi un moteur de rendu « cerema » qui joint une image PNG au graphique interactif. Quarto garde le graphique interactif pour les formats HTML (html, revealjs) et prend l'image pour les autres (typst, docx, pptx). L'image est produite par le paquet `vl-convert-python`, avec les polices Marianne de l'extension. Sans ce paquet, seule la version interactive est produite.

## Choix du format

Un même document peut déclarer plusieurs formats, la sortie se choisissant au rendu. Le fichier `rapport.qmd` sert d'exemple : il déclare les cinq formats.

```yaml
format:
  cerema-typst: default
  cerema-revealjs: default
  cerema-pptx: default
  cerema-docx: default
  cerema-html: default
```

```sh
quarto render rapport.qmd --to cerema-typst
quarto render rapport.qmd --to cerema-revealjs
quarto render rapport.qmd --to cerema-pptx
quarto render rapport.qmd --to cerema-docx
quarto render rapport.qmd --to cerema-html
```

Sans `--to`, Quarto produit tous les formats déclarés.

## Rapport d'étude (format cerema-typst)

Le PDF produit comporte, dans l'ordre : la couverture (bloc-marque République française, logo Cerema, photo, titre sur fond blanc, sous-titre sur fond indigo, bandeau corail portant le type de document et la date, mention de certification ISO 9001, logos partenaires), une page de présentation du Cerema, le résumé (si `abstract` est renseigné), le sommaire, le contenu et une page de fin.

| Clé | Effet |
|---|---|
| `title`, `subtitle` | Titre et sous-titre de la couverture et du pied de page |
| `shorttitle` | Titre court du pied de page (à défaut, le titre complet) |
| `author` | Auteurs, repris dans les propriétés du PDF |
| `date` | Date de la couverture, au format « octobre 2026 » |
| `abstract` | Résumé de l'étude, sur une page dédiée |
| `type-document` | Libellé du bandeau corail, « Rapport d'étude » par défaut |
| `img-couverture` | Photo de couverture, recadrée à 17,6 x 22,4 cm |
| `partenaires` | Liste de logos partenaires (clé commune avec le format revealjs) ; `logo-partenaire` accepte un chemin unique |
| `toc`, `toc-depth` | Affichage et profondeur du sommaire (`true` et 3 par défaut) |

Le rendu des éléments suit les règles ci-dessous.

- Titres : numérotés en indigo, le niveau 1 en capitales, et jamais isolés en bas de page.
- Tableaux Markdown : en-tête indigo à texte blanc, filets gris horizontaux, une ligne sur deux teintée, sans filet vertical. Les légendes, de la forme « Tableau n°1 : », se placent au-dessus des tableaux.
- Images : réduites pour tenir dans la largeur et sous 19 cm de haut.
- Encadrés Quarto (callouts) : filet gauche, fond pâle et pastille de la couleur du type, soit l'indigo pour `note`, le vert pour `tip`, le jaune foncé pour `warning`, le corail pour `important` et le corail foncé pour `caution`. Les encadrés référencés (`#nte-...`) affichent « Note 1 : » suivi de leur titre.

Les fonctions Typst `tableau_cerema`, `tableau_simple`, `tableau_cerema_color` et `tableau_scientifique` sont disponibles dans un bloc ` ```{=typst} `. Elles conservent leur propre style.

La police est Arial, remplacée par Liberation Sans (mêmes métriques) lorsqu'Arial est absente, notamment sous Linux.

Le format présente trois limites.

- Quarto 1.7 télécharge le paquet Typst `@preview/fontawesome` dès qu'un document contient un encadré : sans connexion, la compilation échoue.
- Le type d'encadré est reconnu par sa couleur par défaut. Une palette `brand` modifiée le rend méconnaissable, et l'encadré prend alors la couleur indigo de la note.
- Les images de la charte sont appelées par le chemin absolu Typst `/_extensions/cerema/fig/cerema/`, résolu depuis la racine du projet Quarto. Le document doit donc se trouver dans le projet qui contient `_extensions/`.

## Présentation PowerPoint (format cerema-pptx)

Le fichier de référence `_extensions/cerema/reference.pptx` est construit à partir du modèle « Diaporama Cerema 2026 » (`sources/Modele_Diaporama_Cerema_2026.potx`) par le script `outils/construire_reference_pptx.py`. Le script retire les 26 diapositives d'exemple, puis renomme sept des 40 dispositions avec les noms anglais que Pandoc attend et retype leurs zones réservées. Le modèle emploie en effet des zones de texte génériques pour les titres, alors que Pandoc exige des zones de type titre.

| Disposition du modèle | Nom attendu par Pandoc |
|---|---|
| Slide couv | Title Slide |
| Slide texte seulement | Title and Content |
| Slide fond dégradé | Section Header |
| Slide texte 2 colonnes | Two Content |
| Slide texte + graphiques | Comparison |
| Page avec 1 photo + texte | Content with Caption |
| Derniere page | Blank |

Les 33 autres dispositions restent disponibles dans PowerPoint pour une retouche manuelle.

Le réglage `slide-level: 2` fait produire une diapositive de chapitre sur dégradé par `#` et une diapositive de contenu par `##`. Les titres de diapositive sont forcés en capitales. Quarto ne prend pas en charge les encadrés référencés (`#nte-...`) en PowerPoint et émet un avertissement.

Le fichier de référence se régénère avec la commande suivante.

```sh
uv run python outils/construire_reference_pptx.py sources/Modele_Diaporama_Cerema_2026.potx _extensions/cerema/reference.pptx
```

## Document Word (format cerema-docx)

Le fichier de référence `_extensions/cerema/reference.docx` est construit à partir du fichier de référence par défaut de Pandoc par `outils/construire_reference_docx.py`. Le texte courant est en Marianne 11 pt noir et les titres sont en Arial gras indigo. Le titre de niveau 1 est en capitales, précédé d'un filet corail, et le titre du document est souligné d'un filet corail. L'en-tête de la première page porte les logos République française et Cerema, celui des pages suivantes un petit logo Cerema. Le pied de page affiche la pagination « n / N ». Le sommaire (`toc`) est intitulé « Sommaire ».

Les tableaux reçoivent le style Word « Tableau Cerema » : en-tête corail à texte noir gras, lignes gris-tableau et filets blancs. Le filtre `cerema-docx.lua` attribue ce style aux seuls tableaux écrits dans le document. Quarto emploie aussi des tableaux invisibles pour les légendes et les encadrés, qui gardent le style neutre « Table ».

Le format présente deux limites.

- Marianne n'est pas incorporée au fichier Word : un poste sans Marianne affiche une police de remplacement.
- Le sommaire est un champ Word, à mettre à jour à l'ouverture (Word le propose).

Le fichier de référence se régénère avec les commandes suivantes.

```sh
quarto pandoc -o pandoc-reference.docx --print-default-data-file reference.docx
uv run python outils/construire_reference_docx.py pandoc-reference.docx _extensions/cerema/reference.docx
```

## Pages et sites HTML (format cerema-html)

Le thème est un thème Bootstrap, `cerema-html.scss`, fondé sur cosmo. Les polices Marianne sont déclarées dans `cerema-html-header.html`, et `cerema-html-bandeau.html` place les logos République française et Cerema dans le pied de page.

- Titre : Arial gras indigo-profond, souligné de corail. Les titres de niveau 2 sont précédés d'une barre corail.
- Tableaux : en-tête corail et lignes gris-tableau.
- Encadrés : aux couleurs Cerema, soit l'indigo pour `note`, le vert pour `tip`, le jaune foncé pour `warning`, le corail pour `important` et le corail foncé pour `caution`.
- Citations : Spectral italique indigo.
- Barre de navigation : blanche, soulignée de corail. Le pied de page est blanc, séparé du contenu par un filet gris clair, avec un texte indigo.

Pour un site, il suffit de déclarer le format dans `_quarto.yml`.

```yaml
project:
  type: website
format: cerema-html
```

Les polices et les logos sont copiés à côté de chaque page rendue, y compris dans les sous-dossiers.

Le script de `cerema-html-bandeau.html` place les logos à gauche du pied de page, sur une page isolée comme sur un site. Si la page ne déclare pas de pied de page, l'extension en crée un, de même structure que celui de Quarto. Sans JavaScript, les logos restent en tête de page.

## Accessibilité

Le modèle comporte des paires de couleurs à faible contraste, qu'il convient de connaître.

- Le corail sur blanc offre un rapport de 2,82:1. Il doit être réservé aux titres d'au moins 28 pt en gras.
- Le blanc sur la partie corail du dégradé est peu contrasté.
- La page de fin est rendue à 73 % d'opacité : le texte blanc y est peu contrasté du côté gauche, où domine le corail.

Par ailleurs, l'extension met en noir le texte des en-têtes de tableau, ce qui donne un rapport de 7,4:1 sur le corail.

## Fonctionnement technique

- `cerema.lua` est un filtre Lua. Il traduit les classes de titre en attributs `background-*`, que Pandoc convertit en attributs `data-background-*` de la section reveal.js : dégradés pour les chapitres et la page de fin, couleurs unies pour les fonds teintés. Un titre de niveau 1 reçoit la classe `.chapitre` s'il n'a ni `.chapitre-sommaire` ni `.fin`.
- `title-slide.html` est un partial de gabarit qui remplace la diapositive de titre de Quarto.
- `cerema-after-body.html` contient un script exécuté à l'initialisation de reveal.js. Il ajoute aux diapositives de contenu la classe `cerema-contenu` (barre, hachures, halo) et le pied de page. Sont exclues la couverture et les diapositives portant `.chapitre`, `.chapitre-sommaire`, `.fin` ou `.sans-pied`.
- `cerema-header.html` déclare les `@font-face` de Marianne, applique l'image du halo et charge Spectral depuis Google Fonts. Les chemins y sont relatifs au document, car Quarto copie les fichiers déclarés dans `format-resources` à côté du HTML rendu.
- `cerema.scss` rassemble les jetons de couleur, l'échelle typographique et les règles de chaque disposition.
- `typst-template.typ` définit la fonction `cerema-rapport()`, les couleurs, les fonctions de tableau et remplace la fonction `callout()` de Quarto ; `typst-show.typ` transmet les métadonnées YAML à `cerema-rapport()`.
- Pour un encadré référencé, une règle `show figure` du gabarit affiche directement le corps de la figure et transmet le préfixe « Note 1 » par un `state` Typst, au lieu de laisser Quarto démonter les blocs de l'encadré.

## Arborescence

```text
.
├── _extensions/cerema/
│   ├── _extension.yml            définition des cinq formats
│   ├── cerema.lua                filtre Lua (fonds)
│   ├── cerema.scss               thème
│   ├── title-slide.html          partial de couverture
│   ├── cerema-header.html        polices et halo
│   ├── cerema-after-body.html    habillage et pied de page
│   ├── typst-template.typ        gabarit du rapport (Typst)
│   ├── typst-show.typ            passage des métadonnées au gabarit
│   ├── cerema-docx.lua           filtre Word (style des tableaux)
│   ├── cerema-html.scss          thème des pages HTML
│   ├── cerema-html-header.html   polices des pages HTML
│   ├── cerema-html-bandeau.html  logos du pied de page (HTML)
│   ├── reference.pptx            référence PowerPoint (générée)
│   ├── reference.docx            référence Word (générée)
│   ├── assets/                   logos, bloc-marque RF, halo, motifs
│   ├── fonts/                    Marianne (graisses 300 à 800)
│   └── fig/cerema/               images du rapport (couverture, logos, page de fin)
├── template.qmd                  exemple complet
├── rapport.qmd                   exemple de rapport (cinq formats)
├── cerema_altair.py              thème Altair
├── outils/                       scripts de construction des fichiers de référence
├── sources/                      modèle PowerPoint d'origine (.potx)
├── pyproject.toml                dépendances Python
└── uv.lock
```

Le rendu de `template.qmd` produit en outre `template.html`, le dossier `template_files/` et, à la racine, une copie des logos et des polices.

## Origine des ressources

Les logos, les motifs et les polices Marianne proviennent du design system du Cerema. Les logos ne doivent être ni recolorés ni redessinés.
