-- Filtre Word du format cerema-docx.
--
-- 1. Attribue le style « Tableau Cerema » aux tableaux écrits dans le document.
--    Le filtre s'exécute avant ceux de Quarto : les tableaux que Quarto ajoute
--    ensuite pour mettre en page légendes et encadrés gardent le style neutre
--    « Table » du fichier de référence.
-- 2. Remplace les encadrés (callouts) non référencés par des paragraphes aux
--    styles « Encadré <type> » du fichier de référence : filet coloré à gauche
--    et fond pâle, comme dans le rapport PDF. Les encadrés référencés
--    (#nte-..., #tip-...) gardent le rendu de Quarto, qui les numérote.

-- Titres par défaut : ceux de Quarto pour le français (_language-fr.yml).
local titres = {
  note = "Note",
  tip = "Astuce",
  warning = "Avertissement",
  important = "Important",
  caution = "Mise en garde",
}

function Table(tableau)
  if tableau.attr.attributes["custom-style"] == nil then
    -- Identifiant du style Word (sans espace), et non son nom affiché.
    tableau.attr.attributes["custom-style"] = "TableauCerema"
  end
  return tableau
end

function Callout(encadre)
  local identifiant = encadre.identifier
  if (identifiant == nil or identifiant == "") and encadre.attr ~= nil then
    identifiant = encadre.attr.identifier
  end
  if identifiant ~= nil and identifiant ~= "" then
    return nil
  end
  local type_encadre = titres[encadre.type] and encadre.type or "note"
  local style = "Encadré " .. type_encadre

  -- Le titre arrive en éléments en ligne ou en bloc (Plain, Para) selon les cas.
  local titre = encadre.title
  if titre ~= nil and (titre.t == "Plain" or titre.t == "Para") then
    titre = titre.content
  elseif titre ~= nil and titre.t ~= nil then
    titre = pandoc.Inlines(pandoc.utils.stringify(titre))
  end
  if titre == nil or #pandoc.utils.stringify(titre) == 0 then
    titre = pandoc.Inlines(titres[type_encadre])
  end

  local blocs = pandoc.Blocks({
    pandoc.Div(pandoc.Plain(titre), { ["custom-style"] = style .. " titre" }),
  })
  -- Quarto transmet le contenu soit comme une liste de blocs, soit comme un
  -- seul bloc (une Div) : on aplatit dans les deux cas.
  local contenu = encadre.content
  if contenu.t == "Div" then
    contenu = contenu.content
  elseif contenu.t ~= nil then
    contenu = pandoc.Blocks({ contenu })
  end
  blocs:extend(contenu)
  return pandoc.Blocks({
    pandoc.Div(blocs, { ["custom-style"] = style }),
    pandoc.Div(pandoc.Para({}), { ["custom-style"] = "Encadré fin" }),
  })
end
