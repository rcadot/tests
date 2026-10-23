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
| `dossier-fig` | texte | `/_extensions/cerema/fig/cerema/`, chemin absolu Typst depuis la racine du projet |
| `chemin(p)` | fonction | Retire les échappements Pandoc (`\_`) d'un chemin de métadonnée |
| `styles-callout` | dictionnaire | Couleur Quarto de l'encadré (hex) vers `(couleur, pictogramme)` Cerema |
| `prefixe-callout` | state | « Note 1 » transmis au titre d'un encadré référencé |
| `footer-style` | state | `"default"` (titre + pagination) ou `"simple"` (pagination seule) |
| `cerema-rapport(...)` | fonction | Mise en page complète, appelée par `typst-show.typ` |
| `tableau_cerema`, `tableau_simple`, `tableau_cerema_color`, `tableau_scientifique` | fonctions | Tableaux stylés à appeler depuis un bloc `{=typst}` |

## Ressources

| Fichier | Origine | Rôle |
|---|---|---|
| `assets/cerema-logo.svg` | Design system Cerema, groupe Logos | Logo polychrome avec signature |
| `assets/cerema-rf.svg` | Design system Cerema, groupe Logos | Bloc-marque République française |
| `assets/cerema-halo.png` | Design system Cerema, groupe Motifs | Halo de points corail |
| `assets/cerema-hachures.svg`, `assets/cerema-trame.svg` | Design system Cerema, groupe Motifs | Fournis, non utilisés (motifs redessinés en CSS) |
| `fonts/Marianne-*.otf` | Design system Cerema | Light, Regular, Italic, Medium, Bold, BoldItalic, ExtraBold |
| `fig/cerema/marianne.png`, `fig/cerema/cerema.png` | Fournis par l'utilisateur | Logos de couverture du rapport Typst |
| `fig/cerema/fond.jpg` | Fourni par l'utilisateur | Photo de couverture par défaut (« photo à remplacer ») |
| `fig/cerema/fin_rapport.jpg` | Fourni par l'utilisateur | Bloc-marque de la page de fin du rapport |
