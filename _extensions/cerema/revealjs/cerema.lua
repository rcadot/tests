--[[
Filtre Cerema pour revealjs.

Traduit les classes de diapositive du design system en fonds reveal.js :
  - titre de niveau 1 ou classe .chapitre : dégradé corail vers indigo-profond ;
  - .chapitre-sommaire : dégradé sur la moitié gauche, fond blanc à droite ;
  - .fin : dégradé à 73 % d'opacité (page de fin) ;
  - .fond-lavande, .fond-jaune, .fond-corail, .fond-olive, .fond-vert,
    .fond-bleu : fonds teintés.
Pandoc convertit les attributs background-* d'un titre de diapositive en
attributs data-background-* de la section.
]]

local DEGRADE = "linear-gradient(90deg, #EF7757 0%, #262069 100%)"
local DEGRADE_SOMMAIRE = "linear-gradient(90deg, #EF7757 0%, #262069 50%, #FFFFFF 50%)"
local DEGRADE_FIN = "linear-gradient(90deg, rgba(239,119,87,0.73) 0%, rgba(38,32,105,0.73) 100%)"

local FONDS = {
  ["fond-lavande"] = "#E7E4EF",
  ["fond-jaune"] = "#FDF6DE",
  ["fond-corail"] = "#FCEAE5",
  ["fond-olive"] = "#ECF3DA",
  ["fond-vert"] = "#D6EBDE",
  ["fond-bleu"] = "#E4E8F2",
}

--- Indique si la liste de classes contient la classe donnée.
-- @param classes pandoc.List des classes du titre
-- @param nom nom de la classe recherchée
-- @return booléen
local function a_classe(classes, nom)
  return classes:includes(nom)
end

--- Pose les attributs de fond sur un titre de diapositive.
-- @param el pandoc.Header
-- @return pandoc.Header modifié, ou nil si rien à faire
function Header(el)
  if not quarto.doc.is_format("revealjs") then
    return nil
  end
  if el.level > 2 then
    return nil
  end

  local cls = el.classes
  if el.level == 1 and not a_classe(cls, "chapitre-sommaire") and not a_classe(cls, "fin") then
    if not a_classe(cls, "chapitre") then
      cls:insert("chapitre")
    end
  end

  if a_classe(cls, "chapitre") then
    el.attributes["background-gradient"] = DEGRADE
    return el
  end
  if a_classe(cls, "chapitre-sommaire") then
    el.attributes["background-gradient"] = DEGRADE_SOMMAIRE
    return el
  end
  if a_classe(cls, "fin") then
    el.attributes["background-color"] = "#FFFFFF"
    el.attributes["background-gradient"] = DEGRADE_FIN
    return el
  end
  for nom, couleur in pairs(FONDS) do
    if a_classe(cls, nom) then
      el.attributes["background-color"] = couleur
      return el
    end
  end
  return nil
end

--- Sépare le contenu qui suit directement un titre de chapitre.
-- Un « # Titre » suivi de texte sans « ## » intermédiaire mettait ce texte sur
-- la diapositive de chapitre (dégradé), par-dessus le titre. Un saut de
-- diapositive (règle horizontale) le reporte sur une diapositive de contenu.
-- .chapitre-sommaire et .fin portent volontairement du contenu : non concernés.
-- @param doc pandoc.Pandoc
-- @return pandoc.Pandoc modifié
function Pandoc(doc)
  if not quarto.doc.is_format("revealjs") then
    return nil
  end
  local blocs = pandoc.Blocks({})
  local n = #doc.blocks
  for i, bloc in ipairs(doc.blocks) do
    blocs:insert(bloc)
    local suivant = i < n and doc.blocks[i + 1] or nil
    if bloc.t == "Header" and bloc.level == 1 and a_classe(bloc.classes, "chapitre")
      and suivant ~= nil
      and not (suivant.t == "Header" and suivant.level <= 2)
      and suivant.t ~= "HorizontalRule" then
      blocs:insert(pandoc.HorizontalRule())
    end
  end
  doc.blocks = blocs
  return doc
end
