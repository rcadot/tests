"""Thème Altair aux couleurs du design system Cerema.

L'import du module enregistre le thème « cerema » et l'active.
Barres en indigo-profond, séries catégorielles dans l'ordre indigo-profond,
corail, jaune, olive, vert, bleu, comme le prescrit le livre de marque.

Il active aussi le moteur de rendu « cerema », qui joint une image PNG au
graphique interactif : Quarto garde le HTML pour les formats web (html,
revealjs) et prend le PNG pour les autres (typst, docx, pptx).
"""

import json
from pathlib import Path
from typing import Any

import altair as alt
from altair.vegalite.v6.display import html_renderer, png_renderer

JETONS: dict[str, str] = json.loads(
    (Path(__file__).parent / "_extensions" / "cerema" / "jetons.json").read_text(
        encoding="utf-8"
    )
)
"""Jetons couleur du design system, générés par outils/generer_jetons.py."""

INDIGO = JETONS["indigo"]
INDIGO_PROFOND = JETONS["indigo-profond"]
CORAIL = JETONS["corail"]
JAUNE = JETONS["jaune"]
OLIVE = JETONS["olive"]
VERT = JETONS["vert"]
BLEU = JETONS["bleu"]
GRIS_CLAIR = JETONS["gris-clair"]
NOIR = JETONS["noir"]

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


DOSSIER_POLICES: Path = Path(__file__).parent / "_extensions" / "cerema" / "fonts"
"""Polices Marianne de l'extension, enregistrées auprès de vl-convert."""

ECHELLE_PNG: float = 2.0
"""Facteur d'échelle des images PNG (2 : netteté à l'impression)."""


def _enregistrer_polices() -> None:
    """Rend Marianne disponible pour l'export PNG.

    vl-convert ne voit que les polices du système ; sans Marianne installée,
    les PNG retomberaient sur Arial. Sans vl-convert, ne fait rien.
    """
    try:
        import vl_convert as vlc
    except ImportError:
        return
    if DOSSIER_POLICES.is_dir():
        vlc.register_font_directory(str(DOSSIER_POLICES))


def rendu_html_et_png(spec: dict, **metadata: Any) -> tuple[dict, dict]:
    """Produit le graphique en HTML interactif et en image PNG.

    Args:
        spec: Spécification Vega-Lite transmise par Altair.
        **metadata: Options d'intégration transmises au rendu HTML.

    Returns:
        Le paquet MIME (``text/html`` et ``image/png``) et ses métadonnées.
        Sans vl-convert, le paquet ne contient que le HTML.
    """
    paquet = dict(html_renderer(spec, **metadata))
    try:
        image, meta = png_renderer(spec, scale_factor=ECHELLE_PNG)
    except (ImportError, ValueError):
        return paquet, {}
    paquet.update(image)
    return paquet, meta


_enregistrer_polices()
alt.renderers.register("cerema", rendu_html_et_png)
alt.renderers.enable("cerema")
