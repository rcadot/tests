"""Intègre polices et images aux thèmes HTML et revealjs de l'extension.

Les formats html et revealjs déclaraient les polices Marianne et les logos dans
``format-resources`` : Quarto les copiait à plat à côté de chaque document
rendu, si bien que la racine du projet se remplissait de ``Marianne-*.otf`` et
de ``cerema-*.svg``. Le script les intègre dans une feuille SCSS, sous forme
d'URI ``data:``, et plus rien n'est copié.

Il écrit ``_extensions/cerema/commun/cerema-ressources.scss`` :

- valeurs par défaut : ``$cerema-img-<nom>`` (``url("data:…")``) et
  ``$cerema-ratio-<nom>`` (largeur / hauteur) pour chaque image ;
- règles : ``@font-face`` de Marianne (WOFF2, converti depuis les .otf de
  ``commun/polices``) et classes ``.cerema-img-<nom>``, qui affichent l'image
  en fond d'un élément ``role="img"``.

Le fichier se place en dernier dans ``theme:`` (Quarto met en tête les valeurs
par défaut des derniers fichiers). Les .otf restent la source : le PDF (Typst)
les lit directement.

Usage :
    uv run python _extensions/cerema/outils/generer_ressources_web.py
"""

import base64
import io
import re
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image

EXTENSION = Path(__file__).resolve().parent.parent
POLICES = EXTENSION / "commun" / "polices"
IMAGES = EXTENSION / "commun" / "images"
SORTIE = EXTENSION / "commun" / "cerema-ressources.scss"

EN_TETE = "Généré par outils/generer_ressources_web.py : ne pas modifier."

GRAISSES: dict[str, tuple[int, str]] = {
    "Light": (300, "normal"),
    "Regular": (400, "normal"),
    "RegularItalic": (400, "italic"),
    "Medium": (500, "normal"),
    "Bold": (700, "normal"),
    "BoldItalic": (700, "italic"),
    "ExtraBold": (800, "normal"),
}
"""Suffixe du fichier Marianne-<suffixe>.otf -> (graisse, style)."""

IMAGES_WEB: dict[str, str] = {
    "rf": "cerema-rf.svg",
    "logo": "cerema-logo.svg",
    "halo": "cerema-halo.png",
}
"""Nom court -> fichier de commun/images."""


def woff2_base64(otf: Path) -> str:
    """Convertit une police OpenType en WOFF2 encodé en base64.

    Args:
        otf: Fichier .otf.

    Returns:
        Le contenu WOFF2 en base64.
    """
    # Sans recalcTimestamp=False, fontTools réécrit la date de modification à
    # chaque enregistrement : la sortie changerait à chaque exécution.
    police = TTFont(otf, recalcTimestamp=False)
    police.flavor = "woff2"
    tampon = io.BytesIO()
    police.save(tampon)
    return base64.b64encode(tampon.getvalue()).decode("ascii")


def ratio(image: Path) -> float:
    """Calcule le rapport largeur / hauteur d'une image SVG ou PNG.

    Args:
        image: Fichier image.

    Returns:
        Le rapport largeur / hauteur, arrondi à quatre décimales.
    """
    if image.suffix == ".svg":
        boite = re.search(r'viewBox="([\d.\s-]+)"', image.read_text(encoding="utf-8"))
        _, _, largeur, hauteur = (float(v) for v in boite.group(1).split())
    else:
        largeur, hauteur = Image.open(image).size
    return round(largeur / hauteur, 4)


def uri_data(image: Path) -> str:
    """Encode une image en URI ``data:`` base64.

    Args:
        image: Fichier SVG ou PNG.

    Returns:
        L'URI ``data:`` de l'image.
    """
    type_mime = "image/svg+xml" if image.suffix == ".svg" else "image/png"
    contenu = base64.b64encode(image.read_bytes()).decode("ascii")
    return f"data:{type_mime};base64,{contenu}"


def main() -> None:
    """Écrit commun/cerema-ressources.scss."""
    lignes = ["/*-- scss:defaults --*/", "", f"// {EN_TETE}"]
    for nom, fichier in IMAGES_WEB.items():
        image = IMAGES / fichier
        lignes.append(f'$cerema-img-{nom}: url("{uri_data(image)}");')
        lignes.append(f"$cerema-ratio-{nom}: {ratio(image)};")

    lignes += ["", "/*-- scss:rules --*/", "", "// Marianne, police de l'État (WOFF2)"]
    for suffixe, (graisse, style) in GRAISSES.items():
        donnees = woff2_base64(POLICES / f"Marianne-{suffixe}.otf")
        lignes.append(
            '@font-face { font-family: "Marianne"; '
            f'src: url("data:font/woff2;base64,{donnees}") format("woff2"); '
            f"font-weight: {graisse}; font-style: {style}; font-display: swap; }}"
        )

    lignes += [
        "",
        '// Images portées par un élément role="img" (largeur fixée par le thème)',
    ]
    for nom in IMAGES_WEB:
        lignes.append(
            f".cerema-img-{nom} {{ display: block; "
            f"background: $cerema-img-{nom} center / contain no-repeat; "
            f"aspect-ratio: $cerema-ratio-{nom}; }}"
        )
    SORTIE.write_text("\n".join(lignes) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
