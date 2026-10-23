# Modèle Quarto revealjs Cerema

Ce dépôt fournit l'extension Quarto `cerema`, qui définit le format `cerema-revealjs`. Elle transpose le design system du Cerema, tel que le décrit le modèle PowerPoint « Diaporama Cerema 2026 » : couleurs indigo et corail, dégradé signature, police Marianne pour le texte courant, Arial gras pour les titres et Spectral italique pour le verbatim. La diapositive est au format 16:9, soit 1280 x 720 px ; l'échelle retenue fait correspondre 1 pt du modèle (960 x 540 pt) à 4/3 px.

## Installation

Deux voies sont possibles.

- Copier le dossier `_extensions/cerema` dans le dossier `_extensions` du projet cible.
- Exécuter `quarto use template rcadot/tests` dans un dossier vide. Cette commande suppose que le dépôt soit publié sur GitHub sous ce nom ; elle n'est donc à utiliser que dans ce cas.

L'extension requiert Quarto 1.4 ou supérieur. L'en-tête YAML minimal d'une présentation est le suivant :

```yaml
---
title: "Titre de la présentation"
format: cerema-revealjs
---
```

Le fichier `template.qmd` présente l'ensemble des dispositions et des composants.

## Environnement Python

Python n'est nécessaire que pour les graphiques. Les dépendances (`altair`, `polars`, `jupyter`, `pyarrow`) sont déclarées dans `pyproject.toml`, qui exige Python 3.10 ou supérieur. Elles s'installent avec `uv` :

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

- `title` et `subtitle` : titre en capitales et sous-titre.
- `author` : pour chaque auteur, `name` et, le cas échéant, `affiliations` (liste d'objets portant un `name`), affichées à la suite du nom.
- `date` : l'extension règle le format d'affichage sur `MMMM YYYY` et la langue sur `fr` (par exemple « Octobre 2026 »).
- `partenaires` : liste de chemins d'images, affichées en bas de la couverture, avec une hauteur de 56 px.

## Dispositions

| Disposition | Syntaxe | Rendu |
|---|---|---|
| Couverture | automatique, d'après les métadonnées | Bloc-marque RF, logo Cerema, halo, titre, auteurs, date |
| Diapositive de contenu | `## Titre` | Barre corail, titre en capitales, hachures, halo, pied de page avec bloc-marque RF, logo Cerema et numéro de page |
| Chapitre | `# Titre` ou `## Titre {.chapitre}` | Dégradé corail vers indigo-profond, titre blanc centré verticalement |
| Chapitre avec sommaire | `# Titre {.chapitre-sommaire}` suivi d'une liste | Dégradé sur la moitié gauche, fond blanc à droite portant la liste |
| Sommaire | `## Sommaire / ordre du jour {.sommaire}` suivi d'une liste numérotée | Diapositive de contenu avec liste numérotée en grands caractères |
| Fonds teintés | `{.fond-lavande}`, `{.fond-jaune}`, `{.fond-corail}`, `{.fond-olive}`, `{.fond-vert}`, `{.fond-bleu}` sur un titre de niveau 2 | Fond pâle ; la couleur du titre et de la barre suit le fond |
| Page de fin | `## Merci pour votre attention {.fin}` | Dégradé à 73 % d'opacité, texte et liens blancs |
| Sans pied de page | `{.sans-pied}` | Retire de la diapositive le pied de page et l'habillage de contenu |

Les diapositives à fond teinté conservent l'habillage et le pied de page des diapositives de contenu. La classe `.sans-pied` s'ajoute au titre, par exemple `## Titre {.sans-pied}`.

## Composants

Les composants s'écrivent sous forme de divs Quarto.

- `.chapo` : encadré à filet indigo, destiné au message clé. Le premier mot en gras de la première ligne sert d'intitulé.
- `.verbatim` : citation en Spectral italique indigo, introduite par une citation Markdown (`>`). Une div `.attribution` imbriquée porte l'auteur, la fonction et l'organisme.
- `.source` et `.mention` : mentions en petits caractères, par exemple pour la source d'un chiffre.
- `.encadre` : bloc de mise en avant sur fond corail pâle.
- Tableaux Markdown : en-tête corail, lignes en gris clair et libellés de la première colonne en indigo. Le texte de l'en-tête est noir, car le blanc du modèle sur le corail n'atteint pas le contraste requis. La classe `.entete-blanc`, posée sur le tableau ou sur une div qui l'enveloppe, rétablit le texte blanc du modèle.
- Colonnes : les colonnes Quarto standard (`.columns` et `.column`) sont disposées en flex ; la gouttière se répartit automatiquement entre les colonnes.

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

Le module `cerema_altair.py` enregistre le thème Altair « cerema » et l'active dès son import. Il définit la police Marianne, des axes sans grille verticale, des filets gris clair et une palette catégorielle dans l'ordre indigo-profond, corail, jaune, olive, vert, bleu. Les barres sont en indigo-profond par défaut.

```python
import altair as alt
import cerema_altair  # noqa: F401
```

Les graphiques Altair chargent Vega depuis un CDN : une connexion est donc nécessaire lors de la projection, sauf si le document est rendu avec l'option `embed-resources`.

## Accessibilité

Le modèle comporte des paires de couleurs à faible contraste, qu'il convient de connaître.

- Le corail sur blanc offre un rapport de 2,82:1. Il doit être réservé aux titres d'au moins 28 pt en gras.
- Le blanc sur la partie corail du dégradé est peu contrasté.
- La page de fin est rendue à 73 % d'opacité : le texte blanc y est peu contrasté du côté gauche, où domine le corail.

Pour limiter ce défaut, l'extension passe le texte des en-têtes de tableau en noir (rapport de 7,4:1).

## Fonctionnement technique

- `cerema.lua` est un filtre Lua. Il traduit les classes de titre en attributs `background-*`, que Pandoc convertit en attributs `data-background-*` de la section reveal.js : dégradés pour les chapitres et la page de fin, couleurs unies pour les fonds teintés. Un titre de niveau 1 reçoit la classe `.chapitre` s'il n'a ni `.chapitre-sommaire` ni `.fin`.
- `title-slide.html` est un partial de gabarit qui remplace la diapositive de titre de Quarto.
- `cerema-after-body.html` contient un script exécuté à l'initialisation de reveal.js. Il ajoute aux diapositives de contenu la classe `cerema-contenu` (barre, hachures, halo) et le pied de page. Sont exclues la couverture et les diapositives portant `.chapitre`, `.chapitre-sommaire`, `.fin` ou `.sans-pied`.
- `cerema-header.html` déclare les `@font-face` de Marianne, applique l'image du halo et charge Spectral depuis Google Fonts. Les chemins y sont relatifs au document, car Quarto copie les fichiers déclarés dans `format-resources` à côté du HTML rendu.
- `cerema.scss` rassemble les jetons de couleur, l'échelle typographique et les règles de chaque disposition.

## Arborescence

```text
.
├── _extensions/cerema/
│   ├── _extension.yml          définition du format cerema-revealjs
│   ├── cerema.lua              filtre Lua (fonds)
│   ├── cerema.scss             thème
│   ├── title-slide.html        partial de couverture
│   ├── cerema-header.html      polices et halo
│   ├── cerema-after-body.html  habillage et pied de page
│   ├── assets/                 logos, bloc-marque RF, halo, motifs
│   └── fonts/                  Marianne (graisses 300 à 800)
├── template.qmd                exemple complet
├── cerema_altair.py            thème Altair
├── pyproject.toml              dépendances Python
└── uv.lock
```

Le rendu de `template.qmd` produit en outre `template.html`, le dossier `template_files/` et, à la racine, une copie des logos et des polices.

## Origine des ressources

Les logos, les motifs et les polices Marianne proviennent du design system du Cerema. Les logos ne doivent être ni recolorés ni redessinés.
