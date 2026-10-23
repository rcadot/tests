# Dictionnaire de données du modèle Cerema

## Jetons couleur (`cerema.scss`, variables `--cerema-*`, `cerema_altair.py`)

| Jeton | Valeur | Usage |
|---|---|---|
| `indigo` | #282474 | Texte d'accent, liens, chapô, verbatim, libellés de première colonne |
| `indigo-profond` | #262069 | Fin du dégradé, première série des graphiques |
| `indigo-texte` | #2F2B74 | Titre sur `fond-lavande` et `fond-jaune` |
| `corail` | #EF7757 | Titres de diapositive, barre-repère, en-têtes de tableau, puces |
| `corail-pale` | #F6B5A4 | Décoration, classe `.encadre` |
| `jaune` | #F7D05C | Séries de graphiques |
| `olive` | #96AB5B | Titre sur `fond-olive`, séries |
| `vert` | #448D60 | Titre sur `fond-vert`, séries |
| `bleu` | #5971B3 | Titre sur `fond-bleu`, séries |
| `fond-lavande` | #E7E4EF | Fond teinté |
| `fond-jaune` | #FDF6DE | Fond teinté |
| `fond-corail` | #FCEAE5 | Fond teinté |
| `fond-olive` | #ECF3DA | Fond teinté |
| `fond-vert` | #D6EBDE | Fond teinté |
| `fond-bleu` | #E4E8F2 | Fond teinté |
| `gris-clair` | #E7E6E6 | Filets, axes des graphiques |
| `gris-tableau` | #F2F2F2 | Cellules de tableau |
| `blanc` | #FFFFFF | Fond par défaut |
| `noir` | #000000 | Texte courant |

## Styles de texte (1 pt du modèle = 4/3 px)

| Style | Modèle | Rendu | Police |
|---|---|---|---|
| display (chapitre, fin) | 40 pt | 53 px | Arial gras |
| titre de couverture | 32,6 pt | 43 px | Arial gras, capitales, dégradé |
| titre-diapo (`##`) | 28 pt | 37 px | Arial gras, capitales |
| sous-titre (`###`) | 20 pt | 27 px | Marianne gras |
| corps | 18 pt | 24 px | Marianne |
| corps-petit (chapô, tableau) | 14 pt | 19 px | Marianne |
| mention (`.source`, `.mention`) | 12 pt | 16 px | Marianne |
| numéro de page | 10 pt | 13 px | Arial |
| verbatim | 20 pt | 27 px | Spectral italique |

## Classes de diapositive (titre `#` ou `##`)

| Classe | Effet | Fichier |
|---|---|---|
| (aucune, `##`) | Diapositive de contenu : barre, hachures (140 px de haut), halo, pied de page ; contenu aligné sur le titre à 113 px | `cerema-after-body.html`, `cerema.scss` |
| (aucune, `#`) ou `.chapitre` | Dégradé corail vers indigo-profond, titre blanc | `cerema.lua` |
| `.chapitre-sommaire` | Dégradé sur la moitié gauche, liste à droite | `cerema.lua` |
| `.fin` | Dégradé à 73 % d'opacité, texte blanc | `cerema.lua` |
| `.fond-*` | Fond teinté, titre de la couleur assortie | `cerema.lua`, `cerema.scss` |
| `.sommaire` | Liste numérotée en 27 px | `cerema.scss` |
| `.sans-pied` | Supprime habillage et pied de page | `cerema-after-body.html` |

## Classes de bloc (divs `:::`)

| Classe | Effet |
|---|---|
| `.chapo` | Cadre filet indigo 1 px, texte indigo 19 px |
| `.verbatim` / `.attribution` | Citation Spectral italique indigo, attribution 16 px |
| `.source`, `.mention` | Texte 16 px |
| `.encadre` | Aplat `corail-pale` |
| `.entete-blanc` | En-têtes de tableau en blanc (choix du modèle, contraste 2,82:1) |

## Métadonnées YAML

| Clé | Type | Rôle |
|---|---|---|
| `title` | texte | Titre de couverture |
| `subtitle` | texte | Sous-titre de couverture |
| `author` | liste `{name, affiliations}` | Auteurs et organismes |
| `date` | date ou `today` | Pavé corail en bas à droite, format « MMMM YYYY » |
| `partenaires` | liste de chemins | Logos partenaires en bas de couverture |

## Métadonnées YAML propres au format `cerema-typst`

| Clé | Type | Rôle |
|---|---|---|
| `shorttitle` | texte | Titre du pied de page (défaut : `title`) |
| `abstract` | texte | Page « Résumé de l'étude » |
| `type-document` | texte | Libellé du bandeau corail (défaut : « Rapport d'étude ») |
| `img-couverture` | chemin | Photo de couverture, recadrée à 17,6 x 22,4 cm |
| `logo-partenaire` | chemin | Logo partenaire unique (ignoré si `partenaires` est renseigné) |
| `toc` | booléen | Page Sommaire (défaut : `true`) |
| `toc-depth` | entier | Niveaux de titres du sommaire (défaut : 3) |

## Objets Typst (`typst-template.typ`)

| Nom | Type | Rôle |
|---|---|---|
| `bleucerema` … `bleumerlittoral` | couleur | Palette du rapport (`bleucerema` #292574, `orangecerema` #EF7757, `gris` #87888A, `jaunebatiment` #F7D05C, `vertinfratransport` #96AB5B, `vertenvrisque` #448D60, `bleumerlittoral` #5A71B4) |
| `police` | liste | `("Arial", "Liberation Sans")` |
| `dossier-fig` | texte | `/_extensions/cerema/commun/images/`, chemin absolu Typst depuis la racine du projet |
| `chemin(p)` | fonction | Retire les échappements Pandoc (`\_`) d'un chemin de métadonnée |
| `styles-callout` | dictionnaire | Couleur Quarto de l'encadré (hex) vers `(couleur, pictogramme)` Cerema |
| `prefixe-callout` | state | « Note 1 » transmis au titre d'un encadré référencé |
| `footer-style` | state | `"default"` (titre + pagination) ou `"simple"` (pagination seule) |
| `cerema-rapport(...)` | fonction | Mise en page complète, appelée par `typst-show.typ` |
| `tableau_cerema`, `tableau_simple`, `tableau_cerema_color`, `tableau_scientifique` | fonctions | Tableaux stylés à appeler depuis un bloc `{=typst}` |

## Ressources

| Fichier | Origine | Rôle |
|---|---|---|
| `commun/images/cerema-logo.svg` | Design system Cerema, groupe Logos | Logo polychrome avec signature |
| `commun/images/cerema-rf.svg` | Design system Cerema, groupe Logos | Bloc-marque République française |
| `commun/images/cerema-halo.png` | Design system Cerema, groupe Motifs | Halo de points corail |
| `commun/images/cerema-hachures.svg`, `commun/images/cerema-trame.svg` | Design system Cerema, groupe Motifs | Fournis, non utilisés (motifs redessinés en CSS) |
| `commun/polices/Marianne-*.otf` | Design system Cerema | Light, Regular, Italic, Medium, Bold, BoldItalic, ExtraBold |
| `commun/images/marianne.png`, `commun/images/cerema.png` | Fournis par l'utilisateur | Logos de couverture du rapport Typst |
| `commun/images/fond.jpg` | Fourni par l'utilisateur | Photo de couverture par défaut (« photo à remplacer ») |
| `commun/images/fin_rapport.jpg` | Fourni par l'utilisateur | Bloc-marque de la page de fin du rapport |

## Dispositions PowerPoint (`pptx/reference.pptx`)

| Nom Pandoc | Disposition du modèle | Zones (type, index) |
|---|---|---|
| Title Slide | Slide couv | `ctrTitle` ; `subTitle` 1 (sous-titre et auteur) ; `dt` 10 (date) |
| Title and Content | Slide texte seulement | `title` ; contenu 1 |
| Section Header | Slide fond dégradé | `title` |
| Two Content | Slide texte 2 colonnes | `title` ; contenus 1 et 2 |
| Comparison | Slide texte + graphiques | `title` ; intertitres `body` 1 et 3 ; contenus 2 et 4 |
| Content with Caption | Page avec 1 photo + texte | `title` ; contenu 1 (image) ; `body` 2 (texte) |
| Blank | Derniere page | inchangée |

## Styles Word (`docx/reference.docx`)

| Style | Rendu |
|---|---|
| Normal, Body Text, First Paragraph, Compact | Marianne 11 pt noir |
| Title | Arial gras 26 pt `indigo` |
| Subtitle | Marianne 16 pt `indigo` |
| Heading 1 | Arial gras 19 pt `indigo`, capitales |
| Heading 2, Heading 3 | Arial gras 16 et 12 pt `indigo` |
| Heading 4 | Arial italique 11 pt `corail` |
| Heading 5 à 9 | Arial italique 11 pt gris #87888A |
| Block Text | Marianne italique 12 pt `indigo`, filet `indigo` à gauche |
| Caption, Table Caption, Image Caption | Marianne italique 9 pt noir |
| Tableau Cerema (`TableauCerema`) | En-tête `indigo`, texte blanc gras ; filets horizontaux #B7B8B9 ; ligne paire #F2F2F7 ; 9 pt |
| Encadré `<type>` (note, tip, warning, important, caution) | Marianne 10,5 pt ; filet gauche 3 pt de la couleur du type ; fond éclairci à 92 % |
| Encadré `<type>` titre | Idem, gras, couleur du type |
| Encadré fin | Espace de 4 pt sous l'encadré |
| Table | Style neutre de Pandoc, laissé aux tableaux de mise en page de Quarto |

## Graphiques (`cerema_altair.py`)

| Nom | Type | Rôle |
|---|---|---|
| `rendu_html_et_png` | fonction | Moteur de rendu « cerema » : paquet MIME `text/html` + `image/png` |
| `ECHELLE_PNG` | float | Facteur d'échelle des PNG (2) |
| `DOSSIER_POLICES` | Path | `_extensions/cerema/commun/polices`, enregistré auprès de vl-convert |

## Jetons couleur générés (`outils/generer_jetons.py`)

| Fichier | Contenu | Lu par |
|---|---|---|
| `sources/tokens.json` | Copie du `tokens.json` du design system (source unique) | `outils/generer_jetons.py` |
| `_extensions/cerema/commun/cerema-jetons.scss` | Variables `$indigo`, `$corail`… | Thèmes revealjs et html (dernier fichier de `theme:`) |
| `_extensions/cerema/commun/jetons.json` | Nom -> couleur hexadécimale | `cerema_altair.py`, `outils/construire_reference_docx.py` |
| `typst-template.typ`, bloc `// <jetons>` | `#let indigo = rgb("#282474")`… | Gabarit Typst (alias `bleucerema`, `orangecerema`… conservés) |

## Couleurs des encadrés (tous formats)

| Type | Couleur |
|---|---|
| note | `indigo` |
| tip | `vert` |
| warning | `jaune` assombri de 25 % |
| important | `corail` |
| caution | `corail` assombri (25 % en Typst et Word, 15 % en HTML) |
