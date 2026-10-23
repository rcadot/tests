"""Thème Altair aux couleurs du design system Cerema.

L'import du module enregistre le thème « cerema » et l'active.
Barres en indigo-profond, séries catégorielles dans l'ordre indigo-profond,
corail, jaune, olive, vert, bleu, comme le prescrit le livre de marque.
"""

import altair as alt

INDIGO = "#282474"
INDIGO_PROFOND = "#262069"
CORAIL = "#EF7757"
JAUNE = "#F7D05C"
OLIVE = "#96AB5B"
VERT = "#448D60"
BLEU = "#5971B3"
GRIS_CLAIR = "#E7E6E6"
NOIR = "#000000"

SERIES: list[str] = [INDIGO_PROFOND, CORAIL, JAUNE, OLIVE, VERT, BLEU]
"""Ordre des couleurs pour les séries catégorielles."""

POLICE: str = "Marianne, Arial, sans-serif"


@alt.theme.register("cerema", enable=True)
def theme_cerema() -> alt.theme.ThemeConfig:
    """Construit la configuration Altair du thème Cerema.

    Returns:
        Dictionnaire de configuration Vega-Lite : police Marianne, axes sans
        grille verticale, filets gris-clair, palette catégorielle Cerema.
    """
    return {
        "config": {
            "background": "transparent",
            "font": POLICE,
            "view": {"stroke": None},
            "mark": {"color": INDIGO_PROFOND},
            "bar": {"color": INDIGO_PROFOND},
            "arc": {"stroke": "#FFFFFF"},
            "range": {"category": SERIES},
            "axis": {
                "labelFont": POLICE,
                "titleFont": POLICE,
                "labelFontSize": 14,
                "titleFontSize": 14,
                "titleFontWeight": 700,
                "labelColor": NOIR,
                "titleColor": INDIGO,
                "domainColor": GRIS_CLAIR,
                "tickColor": GRIS_CLAIR,
                "gridColor": GRIS_CLAIR,
            },
            "axisX": {"grid": False},
            "legend": {
                "labelFont": POLICE,
                "titleFont": POLICE,
                "labelFontSize": 14,
                "titleFontSize": 14,
                "titleColor": INDIGO,
            },
            "title": {
                "font": POLICE,
                "fontSize": 18,
                "color": INDIGO,
                "anchor": "start",
            },
        }
    }
