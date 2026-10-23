// Extension Cerema — Rapport d'étude
// Contient : palette, état footer, fonctions tableaux, fonction principale cerema-rapport()
// Pas d'#import externe : tout est inline. Les images de la charte sont appelées
// par chemin absolu Typst (voir dossier-fig), résolu depuis la racine du projet.

// ── Jetons couleur du design system Cerema ───────────────────────────────────
// <jetons>
// Généré par outils/generer_jetons.py depuis sources/tokens.json : ne pas modifier.
#let indigo         = rgb("#282474")
#let indigo-profond = rgb("#262069")
#let indigo-texte   = rgb("#2F2B74")
#let corail         = rgb("#EF7757")
#let corail-pale    = rgb("#F6B5A4")
#let jaune          = rgb("#F7D05C")
#let olive          = rgb("#96AB5B")
#let vert           = rgb("#448D60")
#let bleu           = rgb("#5971B3")
#let fond-lavande   = rgb("#E7E4EF")
#let fond-jaune     = rgb("#FDF6DE")
#let fond-corail    = rgb("#FCEAE5")
#let fond-olive     = rgb("#ECF3DA")
#let fond-vert      = rgb("#D6EBDE")
#let fond-bleu      = rgb("#E4E8F2")
#let gris-clair     = rgb("#E7E6E6")
#let gris-tableau   = rgb("#F2F2F2")
#let blanc          = rgb("#FFFFFF")
#let noir           = rgb("#000000")
// </jetons>

// ── Palette historique du rapport ─────────────────────────────────────────────
// Anciens noms, conservés pour les documents qui les emploient : ils pointent
// désormais vers les jetons du design system.
#let bleucerema         = indigo
#let orangecerema       = corail
#let bleuexpertise      = indigo-profond
#let jaunebatiment      = jaune
#let orangemobilite     = corail
#let vertinfratransport = olive
#let vertenvrisque      = vert
#let bleumerlittoral    = bleu
// Gris des titres de niveau 5 et des mentions : absent du design system.
#let gris               = rgb(135, 136, 138)

// ── Polices ───────────────────────────────────────────────────────────────────
// Marianne (texte courant) est fournie par l'extension : font-paths dans
// _extension.yml. Les titres sont en Arial gras ; sur un poste sans Arial
// (Linux), Typst le signale et retombe sur Marianne.
#let police = "Marianne"
#let police-titre = ("Arial", "Marianne")

// ── Ressources graphiques ─────────────────────────────────────────────────────
// Chemins absolus Typst : résolus depuis la racine du projet Quarto (--root),
// ils restent valides pour un .qmd rangé dans un sous-dossier.
#let dossier-fig = "/_extensions/cerema/commun/images/"

// Pandoc échappe les métadonnées comme du balisage Typst : « mon_logo.png »
// arrive sous la forme « mon\_logo.png ». On retire ces barres obliques.
#let chemin(p) = p.replace(regex("\\\\(.)"), m => m.captures.at(0))

// ── État du pied de page ────────────────────────────────────────────────────
#let footer-style = state("footer-style", "default")

// ── Fonctions tableaux Cerema ─────────────────────────────────────────────────

#let tableau_cerema(titres, data, col_sizes: none) = {
  set text(size: 9pt)
  show table.cell.where(y: 0): set text(size: 10pt, fill: white, weight: "bold")
  let config_col = if col_sizes != none { col_sizes } else { titres.len() }
  table(
    columns: config_col,
    inset: (x: 7pt, y: 7pt),
    stroke: 0.5pt + black,
    fill: (x, y) => if y == 0 { bleucerema } else { white },
    ..titres.flatten(),
    ..data.flatten(),
  )
}

#let tableau_simple(data, col_sizes: none) = {
  set text(size: 11pt)
  show table.cell: it => {
    if it.x == 0 or it.y == 0 { set text(fill: bleucerema); strong(it) }
    else { it }
  }
  let config_col = if col_sizes != none { col_sizes } else { data.at(0).len() }
  table(
    columns: config_col,
    stroke: (x, y) => if (x, y) == (0, 0) { none } else { 0.05em },
    // Annule le fond d'en-tête posé par défaut sur les tableaux Quarto.
    fill: none,
    inset: (x: 7pt, y: 7pt),
    ..data.flatten(),
  )
}

#let tableau_cerema_color(data, color: none, col_sizes: none) = {
  if color == none {
    tableau_simple(data, col_sizes: col_sizes)
  } else {
    set text(size: 11pt)
    show table.cell: it => {
      if it.x == 0 or it.y == 0 { set text(fill: white); strong(it) }
      else { it }
    }
    let config_col = if col_sizes != none { col_sizes } else { data.at(0).len() }
    table(
      columns: config_col,
      stroke: none,
      gutter: .1em,
      inset: (x: 7pt, y: 7pt),
      fill: (x, y) => if y == 0 { color }
                      else if x == 0 { color }
                      else { color.lighten(80%) },
      ..data.flatten(),
    )
  }
}

#let tableau_scientifique(data, col_sizes: none, hline: none, vline: none) = {
  // Annule le style d'en-tête posé par défaut sur les tableaux Quarto.
  show table.cell.where(y: 0): set text(fill: black)
  show table.cell.where(y: 0): strong
  set table(
    fill: none,
    stroke: (x, y) => {
      let styles = (:)
      if hline != none {
        if (type(hline) == int and y == hline) or (type(hline) == array and y in hline) {
          styles.insert("bottom", 0.7pt + black)
        }
      }
      if vline != none {
        if (type(vline) == int and x == vline) or (type(vline) == array and x in vline) {
          styles.insert("right", 0.7pt + black)
        }
      }
      if styles.len() > 0 { styles } else { none }
    },
    align: (x, y) => if x > 0 { center } else { left },
  )
  let config_col = if col_sizes != none { col_sizes } else { data.at(0).len() }
  table(
    columns: config_col,
    inset: (x: 7pt, y: 7pt),
    ..data.flatten(),
  )
}

// ── Encadrés (callouts Quarto) ────────────────────────────────────────────────
// Remplace la fonction callout() de definitions.typ. Quarto ne transmet pas le
// type d'encadré, seulement sa couleur : on retrouve le type par celle-ci.
// Pour un encadré référencé (#nte-..., #tip-...), la règle `show figure` de
// cerema-rapport() dépose « Note 1 » dans prefixe-callout, lu par le titre.
#let prefixe-callout = state("prefixe-callout", none)

#let styles-callout = (
  "#0758e5": (couleur: bleucerema,                 pictogramme: "i"), // note
  "#00a047": (couleur: vertenvrisque,              pictogramme: "+"), // tip
  "#eb9113": (couleur: jaunebatiment.darken(25%),  pictogramme: "!"), // warning
  "#cc1914": (couleur: orangecerema,               pictogramme: "!"), // important
  "#fc5300": (couleur: orangecerema.darken(25%),   pictogramme: "!"), // caution
)

#let callout(body: [], title: "Callout", background_color: none, icon: none, icon_color: black, body_background_color: white) = {
  let style = styles-callout.at(
    icon_color.to-hex(),
    default: (couleur: icon_color, pictogramme: "i"),
  )
  let couleur = style.couleur
  let pastille = box(
    baseline: 0.2em,
    circle(radius: 0.55em, fill: couleur, stroke: none,
      align(center + horizon,
        text(fill: white, size: 0.8em, weight: "bold", style.pictogramme))),
  )
  let titre = context {
    let prefixe = prefixe-callout.get()
    if prefixe == none { title }
    else if title == [] { prefixe }
    else [#prefixe : #title]
  }
  block(
    breakable: true,
    fill: couleur.lighten(92%),
    stroke: (left: 3pt + couleur),
    width: 100%,
    above: 1.2em,
    below: 1.2em,
    inset: (x: 10pt, y: 8pt),
    {
      set par(justify: false)
      block(above: 0pt, below: 0.6em, sticky: true,
        text(fill: couleur, weight: "bold")[#pastille #h(0.3em) #titre])
      if body != [] {
        set par(justify: true)
        block(above: 0pt, below: 0pt, width: 100%, body)
      }
    },
  )
}

// ── Fonction principale ───────────────────────────────────────────────────────

#let cerema-rapport(
  title: none,
  subtitle: none,
  // Titre court pour le pied de page ; à défaut, le titre complet.
  shorttitle: none,
  authors: (),
  date: none,
  abstract: none,
  // Libellé du bandeau orange de la couverture.
  type-document: [Rapport d'étude],
  img-couverture: none,
  logo-partenaire: none,
  toc: true,
  toc-depth: 3,
  doc,
) = {

  // ── Métadonnées PDF ─────────────────────────────────────────────────────────
  set document(title: title, author: authors)

  // ── Styles globaux ──────────────────────────────────────────────────────────
  set text(font: police, size: 11pt, lang: "fr", region: "FR")

  // Page de base sans footer — le footer est ajouté après la couverture
  set page(
    paper: "a4",
    margin: (top: 1.7cm, bottom: 1.7cm, left: 1.7cm, right: 1.7cm),
  )

  set par(justify: true, leading: 0.5em, spacing: 1.0em, first-line-indent: 0pt)
  set heading(numbering: "1.1")

  // ── Styles titres ──────────────────────────────────────────────────────────
  // Le bloc « sticky » reste attaché au paragraphe suivant : un titre n'est
  // jamais laissé seul en bas de page.
  show heading: it => {
    set text(fill: bleucerema, font: police-titre, hyphenate: false)
    // Un titre justifié s'étire sur toute la largeur, lettres capitales espacées.
    set par(justify: false)
    let corps = if it.level == 1 {
      text(size: 19pt, weight: "bold", upper(it))
    } else if it.level == 2 {
      text(size: 16pt, weight: "bold", it)
    } else if it.level == 3 {
      text(size: 12pt, weight: "bold", it)
    } else if it.level == 4 {
      text(size: 11pt, weight: "regular", style: "italic", fill: orangecerema, it)
    } else {
      text(size: 11pt, weight: "regular", style: "italic", fill: gris, it)
    }
    block(
      above: if it.level == 1 { 1em } else { 2em },
      below: 1em,
      sticky: true,
      corps,
    )
  }

  // ── Styles sommaire ────────────────────────────────────────────────────────
  set outline(depth: toc-depth)
  show outline.entry: it => {
    let level    = it.level
    let indents  = (0pt, 0.39cm, 0.39cm)
    let spacings = (5pt, 5pt, 5pt)
    let sizes    = (14pt, 12pt, 11pt)
    v(spacings.at(level - 1, default: 0pt))
    pad(left: indents.at(level - 1, default: 3cm))[
      #text(
        fill: bleucerema,
        size: sizes.at(level - 1, default: 10pt),
        weight: if level < 3 { "bold" } else { "regular" },
      )[#it]
    ]
  }

  // ── Styles légendes ────────────────────────────────────────────────────────
  show figure.caption: set text(size: 9pt, style: "italic")
  show figure.caption: it => {
    strong(it.supplement + " n°")
    if it.numbering != none { strong([#context it.counter.display(it.numbering)]) }
    strong([ : ])
    it.body
  }
  show figure.where(kind: image): set figure(supplement: [Figure])
  show figure.where(kind: table): set figure(supplement: [Tableau])
  show figure.where(kind: table): set figure.caption(position: top)
  show figure: set block(spacing: 2em)

  // Encadré référencé : Quarto l'emballe dans une figure, que sa propre règle
  // démonte selon l'imbrication de ses blocs. On affiche ici le corps tel quel
  // et le titre de l'encadré lit le préfixe « Note 1 » depuis prefixe-callout.
  show figure: it => {
    if type(it.kind) == str and it.kind.starts-with("quarto-callout-") {
      // Annule le centrage et l'espacement de 2em hérités de la figure.
      set align(left)
      set block(spacing: 1.2em)
      prefixe-callout.update(
        context [#it.supplement #it.counter.display(it.numbering)])
      it.body
      prefixe-callout.update(none)
    } else {
      it
    }
  }

  // ── Page de couverture (sans footer) ───────────────────────────────────────
  {
    set page(
      margin: (top: 0.8cm, bottom: 0.8cm, left: 1.7cm, right: 1.7cm),
      header: none,
      footer: none,
    )
    // Titre replié dans un cadre de 16 cm : justifié, il s'étirerait.
    set par(justify: false)

    // Une photo fournie est recadrée au format du fond par défaut (17,6 x 22,4 cm),
    // quelle que soit son orientation, pour que la mise en page reste identique.
    place(center, dy: 3.5cm)[
      #if img-couverture != none {
        image(chemin(img-couverture), width: 100%, height: 22.4cm, fit: "cover")
      } else {
        image(dossier-fig + "fond.jpg", width: 100%, height: auto)
      }
    ]

    place(top + left)[
      #image(dossier-fig + "marianne.png", height: 2.7cm)
    ]
    place(top + right)[
      #image(dossier-fig + "cerema.png", height: 2.5cm)
    ]

    if title != none {
      place(top + left, dx: 0.68cm, dy: 5.42cm)[
        #stack(
          dir: ttb,
          spacing: 0pt,
          layout(size => {
            let style = (font: police-titre, size: 24pt, weight: "bold")
            let mesure = measure(text(..style, title))
            let w = if mesure.width > 16cm { 16cm } else { auto }
            box(
              fill: white, width: w, inset: (x: 6pt, y: 8pt), radius: 0pt,
              text(..style, fill: bleucerema, hyphenate: false, title),
            )
          }),
          if subtitle != none {
            layout(size => {
              let style = (font: police-titre, size: 18pt, weight: "bold")
              let mesure = measure(text(..style, subtitle))
              let w = if mesure.width > 16cm { 16cm } else { auto }
              block(
                fill: bleucerema, width: w, inset: (x: 6pt, y: 6pt), radius: 0pt,
                text(..style, fill: white, hyphenate: false, subtitle),
              )
            })
          },
        )
      ]
    }

    place(bottom + center, dx: +6cm, dy: -4.0cm)[
      #stack(
        spacing: -10pt,
        dir: ttb,
        block(
          fill: orangecerema, width: auto,
          inset: (x: 12pt, top: 6pt, bottom: 15pt), radius: 5pt,
          text(fill: white, size: 16pt, weight: "bold", type-document),
        ),
        block(
          fill: white, width: auto, inset: (x: 6pt, y: 6pt), radius: 5pt,
          text(fill: orangecerema, size: 12pt, weight: "bold",
            if date != none { date } else { [] }),
        ),
      )
    ]

    place(bottom + left)[
      #text(fill: black, size: 8pt)[
        Produit conçu avec le système de management de la qualité certifié AFAQ ISO 9001
      ]
    ]

    // Un chemin seul (logo-partenaire) ou une liste (partenaires, clé partagée
    // avec le format revealjs) : les logos s'alignent de droite à gauche.
    if logo-partenaire != none {
      let logos = if type(logo-partenaire) == str { (logo-partenaire,) } else { logo-partenaire }
      place(bottom + right)[
        #stack(dir: ltr, spacing: 0.5cm, ..logos.map(l => image(chemin(l), height: 1.5cm)))
      ]
    }

    pagebreak()
  }

  // La couverture n'est pas comptée : la page suivante porte le numéro 1.
  counter(page).update(1)

  // ── Activation du footer pour toutes les pages suivantes ───────────────────
  set page(footer: context {
    set text(fill: bleucerema, size: 10pt, font: police)
    set par(justify: false)
    let titre-pied = if shorttitle != none { shorttitle } else { title }
    let current-style = footer-style.get()
    if current-style == "default" {
      grid(
        columns: (1fr, auto),
        column-gutter: 1cm,
        rows: auto,
        align(left)[
          *#if titre-pied != none { titre-pied }* \
          #if subtitle != none { subtitle }
        ],
        align(bottom + right)[
          *#counter(page).display() / #counter(page).final().at(0)*
        ],
      )
    } else {
      align(bottom + right)[
        *#counter(page).display() / #counter(page).final().at(0)*
      ]
    }
  })

  // ── Page copyright ─────────────────────────────────────────────────────────
  footer-style.update("simple")
  block[
    #set text(size: 12pt)
    #set par(leading: 0.25em)
    #v(18.5cm)

    *Le Cerema#footnote[Le Cerema est un établissement public relevant des ministères chargés de l'Aménagement du territoire et de la Transition écologique], référent public en aménagement, accompagne l'État, les collectivités et les entreprises pour adapter les territoires au changement climatique.*

    Il joue un rôle clé dans l'élaboration et la mise en œuvre de politiques publiques nationales et de projets territoriaux adaptés au climat de demain dans 6 domaines d'activité : aménagement et stratégies territoriales, bâtiment, mobilités, infrastructures de transport, environnement et risques, mer et littoral.

    Avec des équipes multidisciplinaires et 27 implantations sur les territoires de l'Hexagone et des Outre-mer, le Cerema dispose d'une approche globale pour conseiller, innover et fédérer.

    #v(1em)
    *www.cerema.fr*
  ]
  pagebreak()
  footer-style.update("default")

  // ── Résumé (depuis abstract: dans le YAML) ────────────────────────────────
  if abstract != none {
    text(fill: bleucerema)[*Résumé de l'étude*]
    v(0.5em)
    abstract
    pagebreak()
  }

  // ── Sommaire stylisé (désactivable par toc: false) ────────────────────────
  if toc {
    box(
      text(
        fill: gradient.linear(bleucerema, orangecerema),
        size: 28pt,
        weight: "bold",
      )[SOMMAIRE],
    )
    rect(
      width: 100%, height: 0.03cm,
      fill: gradient.linear(bleucerema, orangecerema),
      stroke: none,
    )
    v(0.5cm)
    outline(title: none)
    pagebreak()
  }

  // ── Contenu principal ──────────────────────────────────────────────────────
  // Les figures matplotlib arrivent à leur taille native (jusqu'à 25 x 30 cm) :
  // chaque image du corps est réduite, proportions conservées, pour tenir dans
  // la largeur disponible et sous une hauteur qui laisse place à la légende.
  // Jamais agrandie. Posée ici pour ne pas toucher aux images de couverture.
  // Tableaux great_tables : Quarto les range en figures « quarto-float-tbl »,
  // insécables par défaut ; un tableau long déborde alors sur le pied de page.
  // Le texte des cellules n'est ni justifié ni coupé, et la police imposée par
  // great_tables (Segoe UI 12 pt) cède à celle du rapport.
  show figure.where(kind: "quarto-float-tbl"): set block(breakable: true)
  show table: set text(font: police, size: 9pt)
  show table.cell: set par(justify: false)
  show table.cell: set text(hyphenate: false)

  // Tableaux Markdown, modèle commun à tous les formats (docx, html) :
  // en-tête plein indigo à texte blanc gras, filets horizontaux gris, une
  // ligne sur deux teintée, aucun filet vertical. Les fonctions tableau_* et
  // les tableaux qui fixent fill/stroke conservent leur propre style.
  set table(
    inset: (x: 8pt, y: 5pt),
    stroke: (x, y) => (bottom: 0.4pt + gris.lighten(40%)),
    fill: (x, y) => if y == 0 { bleucerema }
                    else if calc.even(y) { bleucerema.lighten(94%) }
                    else { none },
  )
  set table.hline(stroke: none)
  show table.cell.where(y: 0): set text(fill: white, weight: "bold")

  let hauteur-max-image = 19cm
  // La mesure se fait sans contrainte : bornée à la largeur disponible, elle
  // réduirait l'image et masquerait le débordement des dimensions imposées par
  // Quarto (graphiques plotnine). Une largeur relative, mesurée dans un espace
  // infini, est laissée telle quelle.
  show image: it => layout(size => {
    let m = measure(it)
    if m.width == 0pt or m.height == 0pt or m.width > 1e5pt { return it }
    let f = calc.min(1.0, size.width / m.width, hauteur-max-image / m.height)
    if f < 1.0 { scale(f * 100%, reflow: true, it) } else { it }
  })

  doc

  // ── Page de fin ───────────────────────────────────────────────────────────
  {
    set page(
      margin: (top: 0.8cm, bottom: 0.8cm, left: 1.7cm, right: 1.7cm),
      footer: none,
    )
    place(
      bottom + center, dy: -4cm,
      image(dossier-fig + "fin_rapport.jpg", height: 5.5cm),
    )
    place(
      bottom + center, dy: -0.8cm,
      block(width: 100%)[
        #set text(fill: gris, size: 8pt)
        #set par(leading: 0.4em, justify: false)
        #align(center)[
          Siège social : 2 rue Antoine Charial - 69426 Lyon Cedex 03 \
          #underline[www.cerema.fr]
        ]
      ],
    )
  }
}
