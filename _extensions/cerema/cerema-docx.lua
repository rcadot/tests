-- Attribue le style Word « Tableau Cerema » aux tableaux écrits dans le document.
-- Le filtre s'exécute avant ceux de Quarto : les tableaux que Quarto ajoute
-- ensuite pour mettre en page légendes et encadrés gardent le style neutre
-- « Table » du fichier de référence.

function Table(tableau)
  if tableau.attr.attributes["custom-style"] == nil then
    tableau.attr.attributes["custom-style"] = "TableauCerema"
  end
  return tableau
end
