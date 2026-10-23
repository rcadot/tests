-- Filtre PowerPoint du format cerema-pptx.
--
-- Quarto n'accepte qu'une image dans un tableau numéroté (#tbl-...) en
-- PowerPoint : le tableau disparaissait avec un simple avertissement. Le filtre
-- le sort de son conteneur, pose la légende au-dessus (« Tableau n : légende »)
-- et remplace les renvois @tbl-... par « Tableau n ». Deux passages : le
-- premier numérote, le second convertit, car un renvoi peut précéder son tableau.

local numeros = {}

local function numeroter()
  local compte = 0
  return {
    FloatRefTarget = function(flottant)
      if flottant.type == "Table" then
        compte = compte + 1
        numeros[flottant.identifier] = compte
      end
      return nil
    end,
  }
end

local function convertir()
  return {
    FloatRefTarget = function(flottant)
      local numero = numeros[flottant.identifier]
      if numero == nil then
        return nil
      end
      local legende = pandoc.Inlines({ pandoc.Str("Tableau " .. numero .. " :"), pandoc.Space() })
      if flottant.caption_long ~= nil then
        legende:extend(pandoc.utils.blocks_to_inlines({ flottant.caption_long }))
      end
      local contenu = flottant.content
      if contenu.t ~= nil then
        contenu = pandoc.Blocks({ contenu })
      end
      local blocs = pandoc.Blocks({ pandoc.Para({ pandoc.Emph(legende) }) })
      blocs:extend(contenu)
      return blocs
    end,
    Cite = function(renvoi)
      local numero = numeros[renvoi.citations[1].id]
      if #renvoi.citations ~= 1 or numero == nil then
        return nil
      end
      return pandoc.Str("Tableau " .. numero)
    end,
  }
end

return { numeroter(), convertir() }
