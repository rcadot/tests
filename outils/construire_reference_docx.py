"""Construit le fichier de référence Word du format cerema-docx.

Le point de départ est le fichier de référence par défaut de Pandoc, qui porte
déjà tous les styles que Pandoc emploie (« Title », « Heading 1 », « Table »,
« Image Caption »…). Le script les habille selon le design system Cerema :

- texte courant en Marianne 11 pt noir, titres en Arial gras indigo ;
- titre de niveau 1 en capitales, précédé d'un filet corail à gauche ;
- style de tableau « Tableau Cerema » : en-tête corail (texte noir gras,
  7,4:1), lignes gris-tableau ;
- en-tête de première page avec le bloc-marque République française et le
  logo Cerema, pied de page avec le titre court et la pagination « n / N ».

Usage :
    quarto pandoc -o pandoc-reference.docx --print-default-data-file reference.docx
    uv run python outils/construire_reference_docx.py \
        pandoc-reference.docx _extensions/cerema/reference.docx
"""

import sys
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from docx.styles.style import BaseStyle
from docx.text.paragraph import Paragraph

INDIGO = RGBColor(0x28, 0x24, 0x74)
INDIGO_PROFOND = RGBColor(0x26, 0x20, 0x69)
NOIR = RGBColor(0x00, 0x00, 0x00)
CORAIL_HEX = "EF7757"
GRIS_TABLEAU_HEX = "F2F2F2"
GRIS_CLAIR_HEX = "E7E6E6"

NOM_STYLE_TABLEAU = "Tableau Cerema"
"""Style de tableau, repris par le filtre _extensions/cerema/cerema-docx.lua."""

POLICE_TEXTE = "Marianne"
POLICE_TITRE = "Arial"

DOSSIER_FIG = (
    Path(__file__).resolve().parent.parent / "_extensions" / "cerema" / "fig" / "cerema"
)
"""Logos partagés avec le format cerema-typst."""


def police(style: BaseStyle, nom: str) -> None:
    """Applique une police à toutes les écritures d'un style (latin, complexe).

    Args:
        style: Style Word modifié sur place.
        nom: Nom de la police.
    """
    style.font.name = nom
    rfonts = style.element.get_or_add_rPr().get_or_add_rFonts()
    for attribut in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attribut), nom)
    for theme in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        rfonts.attrib.pop(qn(theme), None)


def texte(
    style: BaseStyle,
    nom_police: str,
    taille: float,
    couleur: RGBColor,
    gras: bool = False,
    italique: bool = False,
) -> None:
    """Règle la police, le corps, la couleur et la graisse d'un style.

    Args:
        style: Style Word modifié sur place.
        nom_police: Police à appliquer.
        taille: Corps en points.
        couleur: Couleur du texte.
        gras: Graisse.
        italique: Style italique.
    """
    police(style, nom_police)
    style.font.size = Pt(taille)
    style.font.color.rgb = couleur
    style.font.color.theme_color = None
    style.font.bold = gras
    style.font.italic = italique


def espacement(style: BaseStyle, avant: float, apres: float) -> None:
    """Fixe l'espace avant et après un paragraphe, en points.

    Args:
        style: Style de paragraphe modifié sur place.
        avant: Espace avant.
        apres: Espace après.
    """
    style.paragraph_format.space_before = Pt(avant)
    style.paragraph_format.space_after = Pt(apres)


def filet(
    style: BaseStyle, cote: str, couleur: str, epaisseur_huitiemes: int, marge: int
) -> None:
    """Ajoute un filet de paragraphe à un style.

    Args:
        style: Style de paragraphe modifié sur place.
        cote: « left », « bottom »…
        couleur: Couleur hexadécimale sans dièse.
        epaisseur_huitiemes: Épaisseur en huitièmes de point.
        marge: Écart entre le filet et le texte, en points.
    """
    ppr = style.element.get_or_add_pPr()
    bordures = ppr.find(qn("w:pBdr"))
    if bordures is None:
        bordures = OxmlElement("w:pBdr")
        ppr.append(bordures)
    trait = OxmlElement(f"w:{cote}")
    trait.set(qn("w:val"), "single")
    trait.set(qn("w:sz"), str(epaisseur_huitiemes))
    trait.set(qn("w:space"), str(marge))
    trait.set(qn("w:color"), couleur)
    bordures.append(trait)


def styles_texte(document: Document) -> None:
    """Habille les styles de paragraphe et de caractère employés par Pandoc.

    Args:
        document: Document de référence modifié sur place.
    """
    s = document.styles
    for nom in ("Normal", "Body Text", "First Paragraph", "Compact", "Definition"):
        texte(s[nom], POLICE_TEXTE, 11, NOIR)
    espacement(s["Body Text"], 0, 8)
    espacement(s["First Paragraph"], 0, 8)
    s["Body Text"].paragraph_format.line_spacing = 1.15

    texte(s["Title"], POLICE_TITRE, 26, INDIGO_PROFOND, gras=True)
    espacement(s["Title"], 0, 12)
    filet(s["Title"], "bottom", CORAIL_HEX, 24, 8)
    s["Title"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    texte(s["Subtitle"], POLICE_TEXTE, 16, INDIGO)
    s["Subtitle"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for nom in ("Author", "Date"):
        texte(s[nom], POLICE_TEXTE, 11, NOIR)
        s[nom].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    texte(s["Abstract Title"], POLICE_TITRE, 12, INDIGO, gras=True)
    texte(s["Abstract"], POLICE_TEXTE, 10, NOIR)

    titres = {1: 18, 2: 14, 3: 12}
    for niveau, taille in titres.items():
        style = s[f"Heading {niveau}"]
        texte(style, POLICE_TITRE, taille, INDIGO, gras=True)
        espacement(style, 18 if niveau == 1 else 12, 6)
        style.paragraph_format.keep_with_next = True
    s["Heading 1"].font.all_caps = True
    filet(s["Heading 1"], "left", CORAIL_HEX, 48, 8)
    for niveau in range(4, 10):
        style = s[f"Heading {niveau}"]
        texte(style, POLICE_TEXTE, 11, INDIGO, gras=True, italique=niveau > 4)
        style.paragraph_format.keep_with_next = True
    texte(s["TOC Heading"], POLICE_TITRE, 18, INDIGO, gras=True)

    texte(s["Block Text"], POLICE_TEXTE, 12, INDIGO, italique=True)
    filet(s["Block Text"], "left", "282474", 12, 8)
    # « Caption » est un nom intégré que python-docx stocke en minuscules :
    # on compare donc les noms affichés plutôt que d'indexer.
    legendes = {"caption", "table caption", "image caption"}
    for style in s:
        if style.name and style.name.lower() in legendes:
            texte(style, POLICE_TEXTE, 9, NOIR, italique=True)
    texte(s["Footnote Text"], POLICE_TEXTE, 9, NOIR)
    s["Hyperlink"].font.color.rgb = INDIGO
    s["Hyperlink"].font.color.theme_color = None


def style_tableau(document: Document) -> None:
    """Crée le style « Tableau Cerema » aux couleurs du modèle Cerema.

    Le style « Table » de Pandoc reste neutre : Quarto l'emploie aussi pour les
    tableaux de mise en page (légendes, encadrés). Le filtre cerema-docx.lua
    n'attribue « Tableau Cerema » qu'aux tableaux écrits dans le document.

    En-tête corail à texte noir gras (le blanc du modèle n'atteint que 2,82:1),
    cellules gris-tableau séparées par des filets blancs, comme dans le modèle
    PowerPoint.

    Args:
        document: Document de référence modifié sur place.
    """
    style = document.styles.add_style(NOM_STYLE_TABLEAU, WD_STYLE_TYPE.TABLE)
    style.base_style = document.styles["Table"]
    style.quick_style = True
    element = style.element

    def bordures(
        parent: OxmlElement, nom: str, couleur: str, cotes: tuple[str, ...]
    ) -> None:
        """Ajoute un bloc de bordures blanches ou grises."""
        bloc = OxmlElement(nom)
        for cote in cotes:
            trait = OxmlElement(f"w:{cote}")
            trait.set(qn("w:val"), "single")
            trait.set(qn("w:sz"), "8")
            trait.set(qn("w:space"), "0")
            trait.set(qn("w:color"), couleur)
            bloc.append(trait)
        parent.append(bloc)

    def fond(parent: OxmlElement, couleur: str) -> None:
        """Ajoute une trame de cellule."""
        tcpr = OxmlElement("w:tcPr")
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), couleur)
        tcpr.append(shd)
        parent.append(tcpr)

    rpr_tableau = OxmlElement("w:rPr")
    taille = OxmlElement("w:sz")
    taille.set(qn("w:val"), "18")
    rpr_tableau.append(taille)
    element.append(rpr_tableau)

    tblpr = OxmlElement("w:tblPr")
    bande = OxmlElement("w:tblStyleRowBandSize")
    bande.set(qn("w:val"), "1")
    tblpr.append(bande)
    bordures(
        tblpr,
        "w:tblBorders",
        "FFFFFF",
        ("top", "left", "bottom", "right", "insideH", "insideV"),
    )
    marges = OxmlElement("w:tblCellMar")
    for cote, valeur in (("top", 40), ("left", 100), ("bottom", 40), ("right", 100)):
        marge = OxmlElement(f"w:{cote}")
        marge.set(qn("w:w"), str(valeur))
        marge.set(qn("w:type"), "dxa")
        marges.append(marge)
    tblpr.append(marges)
    element.append(tblpr)

    # Trame grise posée sur les deux bandes de lignes : LibreOffice ignore la
    # trame « wholeTable », Word et LibreOffice appliquent celle des bandes.
    for bande_lignes in ("band1Horz", "band2Horz"):
        ensemble = OxmlElement("w:tblStylePr")
        ensemble.set(qn("w:type"), bande_lignes)
        fond(ensemble, GRIS_TABLEAU_HEX)
        element.append(ensemble)

    entete = OxmlElement("w:tblStylePr")
    entete.set(qn("w:type"), "firstRow")
    rpr = OxmlElement("w:rPr")
    rpr.append(OxmlElement("w:b"))
    couleur = OxmlElement("w:color")
    couleur.set(qn("w:val"), "000000")
    rpr.append(couleur)
    entete.append(rpr)
    fond(entete, CORAIL_HEX)
    element.append(entete)


def champ(paragraphe: Paragraph, instruction: str) -> None:
    """Insère un champ Word (PAGE, NUMPAGES…) à la fin d'un paragraphe.

    Args:
        paragraphe: Paragraphe d'en-tête ou de pied de page.
        instruction: Code du champ.
    """
    simple = OxmlElement("w:fldSimple")
    simple.set(qn("w:instr"), instruction)
    run = OxmlElement("w:r")
    texte_run = OxmlElement("w:t")
    texte_run.text = "1"
    run.append(texte_run)
    simple.append(run)
    paragraphe._p.append(simple)


def entetes_et_pieds(document: Document) -> None:
    """Pose les logos en première page et la pagination sur les suivantes.

    Args:
        document: Document de référence modifié sur place.
    """
    section = document.sections[-1]
    section.start_type = WD_SECTION_START.NEW_PAGE
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    for cote in ("left_margin", "right_margin"):
        setattr(section, cote, Cm(2))
    section.top_margin, section.bottom_margin = Cm(2.5), Cm(2)
    section.different_first_page_header_footer = True
    largeur_utile = section.page_width - section.left_margin - section.right_margin

    premiere = section.first_page_header.paragraphs[0]
    premiere.paragraph_format.tab_stops.add_tab_stop(
        largeur_utile, WD_TAB_ALIGNMENT.RIGHT
    )
    premiere.add_run().add_picture(str(DOSSIER_FIG / "marianne.png"), height=Cm(2))
    premiere.add_run("\t").add_picture(str(DOSSIER_FIG / "cerema.png"), height=Cm(1.6))

    entete = section.header.paragraphs[0]
    entete.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    entete.add_run().add_picture(str(DOSSIER_FIG / "cerema.png"), height=Cm(0.9))

    for pied in (section.footer, section.first_page_footer):
        paragraphe = pied.paragraphs[0]
        paragraphe.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        run = paragraphe.add_run()
        run.font.name = POLICE_TITRE
        run.font.size = Pt(9)
        champ(paragraphe, "PAGE")
        paragraphe.add_run(" / ")
        champ(paragraphe, "NUMPAGES")


def construire(source: Path, sortie: Path) -> None:
    """Produit le fichier de référence Cerema à partir de celui de Pandoc.

    Args:
        source: Fichier de référence par défaut de Pandoc.
        sortie: Fichier .docx à écrire.
    """
    document = Document(str(source))
    styles_texte(document)
    style_tableau(document)
    entetes_et_pieds(document)
    document.save(str(sortie))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    construire(Path(sys.argv[1]), Path(sys.argv[2]))
