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
| (aucune, `##`) | Diapositive de contenu : barre, hachures, halo, pied de page | `cerema-after-body.html`, `cerema.scss` |
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

## Ressources

| Fichier | Origine | Rôle |
|---|---|---|
| `assets/cerema-logo.svg` | Design system Cerema, groupe Logos | Logo polychrome avec signature |
| `assets/cerema-rf.svg` | Design system Cerema, groupe Logos | Bloc-marque République française |
| `assets/cerema-halo.png` | Design system Cerema, groupe Motifs | Halo de points corail |
| `assets/cerema-hachures.svg`, `assets/cerema-trame.svg` | Design system Cerema, groupe Motifs | Fournis, non utilisés (motifs redessinés en CSS) |
| `fonts/Marianne-*.otf` | Design system Cerema | Light, Regular, Italic, Medium, Bold, BoldItalic, ExtraBold |
