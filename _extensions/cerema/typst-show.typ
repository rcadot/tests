#show: doc => cerema-rapport(
$if(title)$
  title: [$title$],
$endif$
$if(subtitle)$
  subtitle: [$subtitle$],
$endif$
$if(shorttitle)$
  shorttitle: [$shorttitle$],
$endif$
$if(by-author)$
  authors: (
$for(by-author)$
    "$it.name.literal$",
$endfor$
  ),
$endif$
$if(date)$
  date: [$date$],
$endif$
$if(abstract)$
  abstract: [$abstract$],
$endif$
$if(type-document)$
  type-document: [$type-document$],
$endif$
$if(img-couverture)$
  img-couverture: "$img-couverture$",
$endif$
$if(partenaires)$
  logo-partenaire: ($for(partenaires)$"$partenaires$", $endfor$),
$elseif(logo-partenaire)$
  logo-partenaire: "$logo-partenaire$",
$endif$
  toc: $if(toc)$true$else$false$endif$,
$if(toc-depth)$
  toc-depth: $toc-depth$,
$endif$
  doc,
)
