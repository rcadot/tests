# Modèles Quarto Cerema : présentations, rapports, documents et pages web

Ce dépôt fournit l'extension Quarto `cerema`, qui définit cinq formats : `cerema-revealjs` et `cerema-pptx` (présentations), `cerema-typst` (rapport d'étude en PDF, compilé par Typst), `cerema-docx` (document Word) et `cerema-html` (pages et sites HTML). Elle transpose le design system du Cerema, tel que le décrit le modèle PowerPoint « Diaporama Cerema 2026 » : couleurs indigo et corail, dégradé signature, police Marianne pour le texte courant, Arial gras pour les titres et Spectral italique pour le verbatim. La diapositive est au format 16:9, soit 1280 x 720 px ; l'échelle retenue fait correspondre 1 pt du modèle (960 x 540 pt) à 4/3 px.

## Prise en main : démarrer un nouveau document

Cet aide-mémoire s'adresse à l'auteur qui reprend un nouveau document avec l'extension, en version 1.3.0.

### Prérequis

- Quarto 1.6 ou supérieur (testé avec 1.7.32).
- Python et `uv`, seulement si le document contient du code Python (graphiques).
- Une connexion Internet pour le PDF dès qu'il y a un encadré (Quarto télécharge le paquet Typst `@preview/fontawesome`) et pour les graphiques Altair en HTML.

### Mettre en place

Deux situations se présentent.

- Depuis un clone du dépôt, les exemples `rapport.qmd` et `template.qmd` se trouvent à la racine. On clone le dépôt, on lance `uv sync` (seulement pour les documents qui contiennent du Python), puis on rend un exemple.
- Pour un autre projet, on copie le seul dossier `_extensions/cerema`. Le document doit se trouver dans le projet qui contient `_extensions/`, éventuellement dans un sous-dossier si un `_quarto.yml` est présent à la racine. Si le document contient du Python, voir « Environnement Python » pour rendre le module `cerema_altair` importable.

```sh
git clone https://github.com/rcadot/tests.git
cd <dossier du dépôt>
uv sync
quarto render rapport.qmd
```

### En-tête YAML type

À adapter au document.

```yaml
---
title: "Titre du document"                # titre
subtitle: "Sous-titre du document"        # sous-titre
shorttitle: "Titre court"                 # pied de page du PDF
author:                                   # liste d'auteurs
  - name: Prénom Nom
    affiliations:
      - name: Cerema
date: today                               # date du jour
abstract: "Résumé de l'étude."            # résumé (PDF et Word)
type-document: "Rapport d'étude"          # bandeau de couverture du PDF (« Rapport d'étude » par défaut)
img-couverture: images/couverture.jpg     # photo de couverture du PDF
partenaires:                              # logos (PDF et revealjs)
  - images/partenaire-1.png
toc: true                                 # sommaire
toc-depth: 3                              # profondeur du sommaire
format:                                   # formats voulus
  cerema-typst: default
  cerema-docx: default
  cerema-pptx: default
  cerema-html: default
  cerema-revealjs: default
---
```

### Générer

```sh
quarto render doc.qmd                          # tous les formats déclarés
quarto render doc.qmd --to cerema-typst        # un seul format
quarto preview doc.qmd --to cerema-html        # aperçu qui se recharge
```

Si le document contient du Python, on indique l'interpréteur de l'environnement : `QUARTO_PYTHON=.venv/bin/python quarto render doc.qmd --to cerema-typst` (sous Windows : `.venv\Scripts\python.exe`).

### Choisir le format

| Format | Usage | Produit |
|---|---|---|
| `cerema-typst` | rapport d'étude | PDF |
| `cerema-docx` | document à relire ou amender | Word |
| `cerema-pptx` | présentation à retoucher | PowerPoint |
| `cerema-revealjs` | présentation projetée | HTML |
| `cerema-html` | page ou site | HTML |

### Écrire pour plusieurs formats à la fois

- `#` ouvre une partie (diapositive de chapitre en pptx et revealjs) et `##` une section (une diapositive en pptx et revealjs). Un document pensé pour le PDF et le Word produit donc beaucoup de diapositives.
- Tableaux : s'écrivent en Markdown. La légende et la numérotation se posent sous le tableau par `: Légende {#tbl-nom}`, et le renvoi s'écrit `@tbl-nom`. Le modèle de tableau (en-tête indigo, lignes alternées) s'applique automatiquement en PDF, Word et HTML. En PowerPoint, c'est le style de tableau du modèle.
- Encadrés : `::: {.callout-note}` (ainsi que tip, warning, important et caution), avec un titre facultatif donné par `## Titre` en première ligne. Un encadré numéroté s'écrit `::: {#nte-nom .callout-note}` et se cite par `@nte-nom`. En PowerPoint, Quarto ne prend pas en charge les encadrés numérotés. En Word, ils gardent le rendu de Quarto.
- Graphiques Altair : `import cerema_altair` en tête de cellule. Ils sont interactifs en HTML et revealjs, et rendus en image PNG en PDF, Word et PowerPoint.
- Un `@` qui n'est pas un renvoi (un compte de réseau social, par exemple) s'écrit `\@`. Sinon, Pandoc y voit une citation et le PDF ne compile pas.
- Les classes propres à revealjs (`.chapitre`, `.fin`, fonds teintés, `.chapo`…) sont ignorées dans les autres formats.
- Le sommaire du Word est un champ à mettre à jour à l'ouverture (Word le propose).

### Ce qui se change où

| Je veux changer… | Fichier |
|---|---|
| les couleurs | `_extensions/cerema/outils/sources/tokens.json`, puis `uv run python _extensions/cerema/outils/generer_jetons.py` (régénère `cerema-jetons.scss`, `jetons.json` et le bloc de couleurs du gabarit Typst) |
| la mise en page du PDF | `_extensions/cerema/typst/typst-template.typ` |
| les styles du Word | `_extensions/cerema/outils/construire_reference_docx.py`, puis régénérer `reference.docx` (voir « Outils de maintenance ») |
| les dispositions PowerPoint | `_extensions/cerema/outils/construire_reference_pptx.py`, puis régénérer `reference.pptx` (voir « Outils de maintenance ») |
| les polices ou les logos des formats HTML et revealjs | `_extensions/cerema/commun/polices` ou `_extensions/cerema/commun/images`, puis `uv run python _extensions/cerema/outils/generer_ressources_web.py` |
| l'aspect des pages HTML | `_extensions/cerema/html/cerema-html.scss` |
| la présentation revealjs | `_extensions/cerema/revealjs/cerema.scss` |
| les options par défaut d'un format (sommaire, langue, largeur de page HTML…) | `_extensions/cerema/_extension.yml` |

Une option posée dans l'en-tête YAML du document l'emporte sur celle de l'extension.

### Vérifier

À chaque envoi, le dépôt exécute le workflow `.github/workflows/rendu.yml`. Il rend les cinq formats de `rapport.qmd` et de `template.qmd`, vérifie que les fichiers générés sont à jour et met les fichiers produits à disposition (artefact « rendus »).

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

Python n'est nécessaire que pour les graphiques et pour les outils de maintenance. Les dépendances (`altair`, `polars`, `jupyter`, `pyarrow`, `vl-convert-python`) sont déclarées dans `pyproject.toml`, qui exige Python 3.10 ou supérieur. Les paquets `python-docx`, `python-pptx`, `fonttools[woff]` et `pillow` sont des dépendances de développement (groupe `dev`), utiles uniquement aux outils de maintenance et installées elles aussi par `uv sync`. Les dépendances s'installent avec `uv` :

```sh
uv sync
QUARTO_PYTHON=.venv/bin/python quarto render template.qmd
```

Le module `cerema_altair` se trouve dans `_extensions/cerema/python/cerema_altair/` et il est déclaré comme paquet dans `pyproject.toml`. `uv sync` l'installe donc dans l'environnement, et `import cerema_altair` fonctionne depuis n'importe quel document du projet.

Un autre projet, qui n'a pas ce `pyproject.toml`, a deux possibilités. La première consiste à ajouter le paquet à son environnement, par `uv pip install -e chemin/vers/le/clone` ou par une dépendance de chemin. La seconde, plus simple, consiste à ajouter ces lignes en tête de la cellule :

```python
import sys; sys.path.insert(0, "_extensions/cerema/python")
import cerema_altair
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

Le module `cerema_altair` (`_extensions/cerema/python/cerema_altair/`) enregistre le thème Altair « cerema » et l'active dès son import. Il définit la police Marianne, des axes sans grille verticale, des filets gris clair et une palette catégorielle dans l'ordre indigo-profond, corail, jaune, olive, vert, bleu. Les barres sont en indigo-profond par défaut.

```python
import altair as alt
import cerema_altair  # noqa: F401
```

Dans un autre projet que ce dépôt, l'import suppose les réglages décrits dans « Environnement Python ». Les graphiques Altair chargent Vega depuis un CDN : une connexion est donc nécessaire lors de la projection.

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

Le texte courant est en Marianne, fournie par l'extension (option `font-paths`), et les titres sont en Arial gras. Sur un poste sans Arial, Typst le signale et utilise Marianne. La pagination commence après la couverture.

Le format présente trois limites.

- Quarto 1.7 télécharge le paquet Typst `@preview/fontawesome` dès qu'un document contient un encadré : sans connexion, la compilation échoue.
- Le type d'encadré est reconnu par sa couleur par défaut. Une palette `brand` modifiée le rend méconnaissable, et l'encadré prend alors la couleur indigo de la note.
- Les images de la charte sont appelées par le chemin absolu Typst `/_extensions/cerema/commun/images/`, résolu depuis la racine du projet Quarto. Le document doit donc se trouver dans le projet qui contient `_extensions/`.

## Présentation PowerPoint (format cerema-pptx)

Le fichier de référence `_extensions/cerema/pptx/reference.pptx` est construit à partir du modèle « Diaporama Cerema 2026 » (`_extensions/cerema/outils/sources/Modele_Diaporama_Cerema_2026.potx`) par le script `_extensions/cerema/outils/construire_reference_pptx.py`. Le script retire les 26 diapositives d'exemple, puis renomme sept des 40 dispositions avec les noms anglais que Pandoc attend et retype leurs zones réservées. Le modèle emploie en effet des zones de texte génériques pour les titres, alors que Pandoc exige des zones de type titre.

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

La disposition « Content with Caption » place le texte en haut et l'objet (image, tableau) dessous, sur toute la largeur. Quarto supprimait les tableaux numérotés en PowerPoint. Le filtre `cerema-pptx.lua` les rend : il pose la légende « Tableau n : … » au-dessus du tableau et remplace les renvois `@tbl-…` par « Tableau n ».

La commande qui régénère le fichier de référence est donnée dans « Outils de maintenance ».

## Document Word (format cerema-docx)

Le fichier de référence `_extensions/cerema/docx/reference.docx` est construit à partir du fichier de référence par défaut de Pandoc par `_extensions/cerema/outils/construire_reference_docx.py`. Le texte courant est en Marianne 11 pt noir et les titres sont en Arial gras indigo. Les titres suivent ceux du PDF : le niveau 1 est en capitales, le niveau 4 en italique corail et le niveau 5 en italique gris. Aucun filet corail ne figure sous le titre du document ni devant les titres de niveau 1. L'en-tête de la première page porte les logos République française et Cerema, celui des pages suivantes un petit logo Cerema. Le pied de page affiche la pagination « n / N ». Le sommaire (`toc`) est intitulé « Sommaire ».

Les tableaux reçoivent le style Word « Tableau Cerema », au même modèle que le PDF : en-tête indigo à texte blanc gras, filets gris, une ligne sur deux teintée, sans filet vertical. Le filtre `cerema-docx.lua` attribue ce style aux seuls tableaux écrits dans le document. Quarto emploie aussi des tableaux invisibles pour les légendes et les encadrés, qui gardent le style neutre « Table ».

Le même filtre rend les encadrés non numérotés comme dans le PDF : filet coloré à gauche, fond pâle et titre en couleur (styles Word « Encadré note », « Encadré note titre », etc.). Les encadrés numérotés gardent le rendu de Quarto.

Le format présente deux limites.

- Marianne n'est pas incorporée au fichier Word : un poste sans Marianne affiche une police de remplacement.
- Le sommaire est un champ Word, à mettre à jour à l'ouverture (Word le propose).

Les commandes qui régénèrent le fichier de référence sont données dans « Outils de maintenance ».

## Pages et sites HTML (format cerema-html)

Le thème est un thème Bootstrap, `cerema-html.scss`, fondé sur cosmo. Les polices Marianne sont intégrées à la feuille de style (voir ci-dessous), et `cerema-html-bandeau.html` place les logos République française et Cerema dans le pied de page.

- Titres : Arial gras indigo-profond, sans barre corail devant les titres ni filet sous le titre du document. La colonne de contenu est élargie à 1050 px (`grid: body-width` dans `_extension.yml`).
- Tableaux : au modèle commun, avec en-tête indigo, texte blanc, filets gris et une ligne sur deux teintée.
- Encadrés : aux couleurs Cerema, soit l'indigo pour `note`, le vert pour `tip`, le jaune foncé pour `warning`, le corail pour `important` et le corail foncé pour `caution`.
- Citations : Spectral italique indigo.
- Barre de navigation : blanche, soulignée de corail. Le pied de page est blanc, séparé du contenu par un filet gris clair, avec un texte indigo.

Pour un site, il suffit de déclarer le format dans `_quarto.yml`.

```yaml
project:
  type: website
format: cerema-html
```

Les polices et les logos sont intégrés à la feuille de style (WOFF2 et images encodés en URI `data:`, fichier généré `commun/cerema-ressources.scss`). Quarto ne copie donc aucun fichier de police ou de logo à côté des pages rendues, et la racine du projet reste propre. En contrepartie, la feuille de style des pages HTML pèse environ 600 Ko de plus, chargée une fois puis mise en cache. Les logos sont affichés comme des éléments `role="img"` portant un libellé accessible.

Le script de `cerema-html-bandeau.html` place les logos à gauche du pied de page, sur une page isolée comme sur un site. Si la page ne déclare pas de pied de page, l'extension en crée un, de même structure que celui de Quarto. Sans JavaScript, les logos restent en tête de page.

## Accessibilité

Le modèle comporte des paires de couleurs à faible contraste, qu'il convient de connaître.

- Le corail sur blanc offre un rapport de 2,82:1. Il doit être réservé aux titres d'au moins 28 pt en gras.
- Le blanc sur la partie corail du dégradé est peu contrasté.
- La page de fin est rendue à 73 % d'opacité : le texte blanc y est peu contrasté du côté gauche, où domine le corail.

Par ailleurs, dans le format revealjs, l'extension met en noir le texte des en-têtes de tableau, ce qui donne un rapport de 7,4:1 sur le corail.

## Fonctionnement technique

- `cerema.lua` est un filtre Lua. Il traduit les classes de titre en attributs `background-*`, que Pandoc convertit en attributs `data-background-*` de la section reveal.js : dégradés pour les chapitres et la page de fin, couleurs unies pour les fonds teintés. Un titre de niveau 1 reçoit la classe `.chapitre` s'il n'a ni `.chapitre-sommaire` ni `.fin`.
- `title-slide.html` est un partial de gabarit qui remplace la diapositive de titre de Quarto.
- `cerema-after-body.html` contient un script exécuté à l'initialisation de reveal.js. Il ajoute aux diapositives de contenu la classe `cerema-contenu` (barre, hachures, halo) et le pied de page. Sont exclues la couverture et les diapositives portant `.chapitre`, `.chapitre-sommaire`, `.fin` ou `.sans-pied`.
- `cerema-header.html` charge Spectral depuis Google Fonts. Les polices Marianne et l'image du halo n'y figurent plus : elles sont intégrées à la feuille de style par `commun/cerema-ressources.scss`, sans fichier copié à côté du HTML rendu.
- `cerema.scss` rassemble l'échelle typographique et les règles de chaque disposition. Les jetons de couleur viennent de `cerema-jetons.scss`.
- `typst-template.typ` définit la fonction `cerema-rapport()`, les couleurs, les fonctions de tableau et remplace la fonction `callout()` de Quarto ; `typst-show.typ` transmet les métadonnées YAML à `cerema-rapport()`.
- Pour un encadré référencé, une règle `show figure` du gabarit affiche directement le corps de la figure et transmet le préfixe « Note 1 » par un `state` Typst, au lieu de laisser Quarto démonter les blocs de l'encadré.

### Jetons de couleur

La source unique des couleurs est `_extensions/cerema/outils/sources/tokens.json`, copie du `tokens.json` du design system Cerema. Le générateur `_extensions/cerema/outils/generer_jetons.py` en produit trois sorties.

- `_extensions/cerema/commun/cerema-jetons.scss`, placé en dernier dans `theme:` des formats revealjs et html, car Quarto place en tête les valeurs par défaut des derniers fichiers.
- `_extensions/cerema/commun/jetons.json`, lu par `cerema_altair` et par `_extensions/cerema/outils/construire_reference_docx.py`.
- Le bloc compris entre `// <jetons>` et `// </jetons>` de `typst-template.typ`.

Les anciens noms de couleurs du gabarit Typst (`bleucerema`, `orangecerema`…) restent disponibles et pointent vers ces jetons.

La commande de génération est donnée dans « Outils de maintenance ».

## Outils de maintenance

Les scripts de `_extensions/cerema/outils/` ne servent pas à utiliser l'extension, seulement à la maintenir. Les fichiers qu'ils produisent sont versionnés : un utilisateur n'a donc jamais besoin de les lancer, et le workflow GitHub vérifie que ces fichiers sont à jour. Les scripts demandent les dépendances de développement (`python-docx`, `python-pptx`, `fonttools[woff]`, `pillow`), installées par `uv sync`.

| Script | À lancer après | Fichiers régénérés |
|---|---|---|
| `generer_jetons.py` | une modification des couleurs dans `outils/sources/tokens.json` | `commun/cerema-jetons.scss`, `commun/jetons.json` et le bloc de couleurs du gabarit Typst |
| `generer_ressources_web.py` | un changement de police ou de logo dans `commun/polices` ou `commun/images` | `commun/cerema-ressources.scss` |
| `construire_reference_docx.py` | une modification des styles Word | `docx/reference.docx` |
| `construire_reference_pptx.py` | une modification du modèle PowerPoint ou des dispositions | `pptx/reference.pptx`, depuis `outils/sources/Modele_Diaporama_Cerema_2026.potx` |

Les commandes se lancent depuis la racine du dépôt, après `uv sync`.

```sh
uv run python _extensions/cerema/outils/generer_jetons.py
uv run python _extensions/cerema/outils/generer_ressources_web.py
uv run python _extensions/cerema/outils/construire_reference_docx.py pandoc-reference.docx _extensions/cerema/docx/reference.docx
uv run python _extensions/cerema/outils/construire_reference_pptx.py _extensions/cerema/outils/sources/Modele_Diaporama_Cerema_2026.potx _extensions/cerema/pptx/reference.pptx
```

Pour le Word, `pandoc-reference.docx` s'obtient par `quarto pandoc -o pandoc-reference.docx --print-default-data-file reference.docx`.

## Arborescence

```text
.
├── .github/workflows/rendu.yml                     workflow de rendu des cinq formats
├── .gitignore
├── README.md
├── rapport.qmd                                     exemple de rapport (cinq formats)
├── template.qmd                                    exemple complet
├── pyproject.toml                                  environnement Python des exemples et des outils
├── uv.lock
└── _extensions/cerema/
    ├── _extension.yml                              définition des cinq formats
    ├── commun/                                     ressources partagées
    │   ├── polices/                                Marianne (.otf), lues par le PDF
    │   ├── images/                                 logos, bloc-marque RF, halo, motifs,
    │   │                                           couverture et page de fin du rapport
    │   ├── cerema-jetons.scss                      jetons de couleur SCSS (généré)
    │   ├── cerema-ressources.scss                  polices et logos intégrés aux thèmes HTML et revealjs (généré)
    │   └── jetons.json                             jetons de couleur (généré)
    ├── typst/                                      rapport PDF
    │   ├── typst-template.typ                      gabarit du rapport
    │   └── typst-show.typ                          passage des métadonnées au gabarit
    ├── docx/                                       document Word
    │   ├── reference.docx                          fichier de référence (généré)
    │   └── cerema-docx.lua                         filtre : tableaux et encadrés
    ├── pptx/                                       présentation PowerPoint
    │   ├── reference.pptx                          fichier de référence (généré)
    │   └── cerema-pptx.lua                         filtre : tableaux numérotés
    ├── html/                                       pages et sites HTML
    │   ├── cerema-html.scss                        thème
    │   ├── cerema-html-header.html                 en-tête HTML
    │   └── cerema-html-bandeau.html                logos du pied de page
    ├── revealjs/                                   présentation HTML
    │   ├── cerema.scss                             thème
    │   ├── cerema.lua                              filtre (fonds)
    │   ├── title-slide.html                        partial de couverture
    │   ├── cerema-header.html                      en-tête de la présentation
    │   └── cerema-after-body.html                  habillage et pied de page
    ├── python/cerema_altair/                       thème Altair (module Python)
    ├── outils/                                     scripts de maintenance
    │   ├── generer_jetons.py                       jetons de couleur
    │   ├── generer_ressources_web.py               polices et logos des thèmes HTML et revealjs
    │   ├── construire_reference_docx.py            fichier de référence Word
    │   ├── construire_reference_pptx.py            fichier de référence PowerPoint
    │   └── sources/                                sources des outils
    │       ├── Modele_Diaporama_Cerema_2026.potx   modèle PowerPoint du design system
    │       └── tokens.json                         jetons du design system (source unique)
    └── doc/                                        documentation du dépôt
        ├── CHANGELOG.md                            journal des modifications
        ├── dictionnaire_donnees.md
        └── memory.md
```

Le rendu de `template.qmd` produit en outre `template.html` et le dossier `template_files/`.

## Origine des ressources

Les logos, les motifs et les polices Marianne proviennent du design system du Cerema. Les logos ne doivent être ni recolorés ni redessinés.
