"""Construit le fichier de référence Word du format cerema-docx.

Le point de départ est le fichier de référence par défaut de Pandoc, qui porte
déjà tous les styles que Pandoc emploie (« Title », « Heading 1 », « Table »,
« Image Caption »…). Le script les habille selon le design system Cerema :

- texte courant en Marianne 11 pt noir ;
- titres comme ceux du rapport PDF (cerema-typst) : Arial gras indigo, niveau 1
  en capitales, niveau 4 en italique corail, niveau 5 en italique gris ;
- style de tableau « Tableau Cerema », modèle commun aux formats : en-tête
  indigo à texte blanc gras, filets horizontaux gris, une ligne sur deux
  teintée, aucun filet vertical ;
- styles des encadrés (« Encadré note », « Encadré note titre »…) : filet
  coloré à gauche et fond pâle, comme dans le rapport PDF ;
- en-tête de première page avec le bloc-marque République française et le
  logo Cerema, pied de page avec le titre court et la pagination « n / N ».

Usage :
    quarto pandoc -o pandoc-reference.docx --print-default-data-file reference.docx
    uv run python outils/construire_reference_docx.py \
        pandoc-reference.docx _extensions/cerema/reference.docx
"""

import json
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

JETONS: dict[str, str] = json.loads(
    (
        Path(__file__).resolve().parent.parent
        / "_extensions"
        / "cerema"
        / "jetons.json"
    ).read_text(encoding="utf-8")
)
"""Jetons couleur du design system, générés par outils/generer_jetons.py."""

INDIGO = RGBColor.from_string(JETONS["indigo"][1:])
NOIR = RGBColor.from_string(JETONS["noir"][1:])
CORAIL = RGBColor.from_string(JETONS["corail"][1:])
GRIS_HEX = "87888A"
"""Gris des titres de niveau 5 et des filets (gabarit Typst), hors design system."""


def eclaircir(couleur: str, proportion: float) -> str:
    """Mélange une couleur avec du blanc, comme ``lighten`` de Typst (approché).

    Args:
        couleur: Couleur hexadécimale sans dièse.
        proportion: Part de blanc, entre 0 et 1.

    Returns:
        La couleur éclaircie, hexadécimale sans dièse.
    """
    canaux = [int(couleur[i : i + 2], 16) for i in (0, 2, 4)]
    return "".join(f"{round(c + (255 - c) * proportion):02X}" for c in canaux)


INDIGO_HEX = JETONS["indigo"][1:]
LIGNE_TEINTEE_HEX = eclaircir(INDIGO_HEX, 0.94)
"""Ligne paire des tableaux (indigo éclairci à 94 %, comme le PDF)."""
FILET_HEX = eclaircir(GRIS_HEX, 0.40)
"""Filets horizontaux des tableaux (gris éclairci à 40 %, comme le PDF)."""

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

    texte(s["Title"], POLICE_TITRE, 26, INDIGO, gras=True)
    espacement(s["Title"], 0, 12)
    s["Title"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    texte(s["Subtitle"], POLICE_TEXTE, 16, INDIGO)
    s["Subtitle"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for nom in ("Author", "Date"):
        texte(s[nom], POLICE_TEXTE, 11, NOIR)
        s[nom].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    texte(s["Abstract Title"], POLICE_TITRE, 12, INDIGO, gras=True)
    texte(s["Abstract"], POLICE_TEXTE, 10, NOIR)

    # Corps des titres du gabarit Typst : 19, 16 et 12 pt.
    titres = {1: 19, 2: 16, 3: 12}
    for niveau, taille in titres.items():
        style = s[f"Heading {niveau}"]
        texte(style, POLICE_TITRE, taille, INDIGO, gras=True)
        espacement(style, 18 if niveau == 1 else 12, 6)
        style.paragraph_format.keep_with_next = True
    s["Heading 1"].font.all_caps = True
    texte(s["Heading 4"], POLICE_TITRE, 11, CORAIL, italique=True)
    for niveau in range(5, 10):
        texte(
            s[f"Heading {niveau}"],
            POLICE_TITRE,
            11,
            RGBColor.from_string(GRIS_HEX),
            italique=True,
        )
    for niveau in range(4, 10):
        s[f"Heading {niveau}"].paragraph_format.keep_with_next = True
    texte(s["TOC Heading"], POLICE_TITRE, 18, INDIGO, gras=True)

    texte(s["Block Text"], POLICE_TEXTE, 12, INDIGO, italique=True)
    filet(s["Block Text"], "left", JETONS["indigo"][1:], 12, 8)
    # « Caption » est un nom intégré que python-docx stocke en minuscules :
    # on compare donc les noms affichés plutôt que d'indexer.
    legendes = {"caption", "table caption", "image caption"}
    for style in s:
        if style.name and style.name.lower() in legendes:
            texte(style, POLICE_TEXTE, 9, NOIR, italique=True)
    texte(s["Footnote Text"], POLICE_TEXTE, 9, NOIR)
    s["Hyperlink"].font.color.rgb = INDIGO


def style_tableau(document: Document) -> None:
    """Crée le style « Tableau Cerema » aux couleurs du modèle Cerema.

    Le style « Table » de Pandoc reste neutre : Quarto l'emploie aussi pour les
    tableaux de mise en page (légendes, encadrés). Le filtre cerema-docx.lua
    n'attribue « Tableau Cerema » qu'aux tableaux écrits dans le document.

    En-tête indigo à texte blanc gras, filets horizontaux gris, une ligne sur
    deux teintée d'indigo pâle, aucun filet vertical : le modèle du rapport PDF.

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
        """Ajoute un bloc de bordures simples de 0,5 pt sur les côtés donnés."""
        bloc = OxmlElement(nom)
        for cote in cotes:
            trait = OxmlElement(f"w:{cote}")
            trait.set(qn("w:val"), "single")
            trait.set(qn("w:sz"), "4")
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
    bordures(tblpr, "w:tblBorders", FILET_HEX, ("bottom", "insideH"))
    marges = OxmlElement("w:tblCellMar")
    for cote, valeur in (("top", 40), ("left", 100), ("bottom", 40), ("right", 100)):
        marge = OxmlElement(f"w:{cote}")
        marge.set(qn("w:w"), str(valeur))
        marge.set(qn("w:type"), "dxa")
        marges.append(marge)
    tblpr.append(marges)
    element.append(tblpr)

    # Une ligne sur deux teintée : la deuxième bande suit la première ligne de
    # données, comme les lignes paires du gabarit Typst.
    paire = OxmlElement("w:tblStylePr")
    paire.set(qn("w:type"), "band2Horz")
    fond(paire, LIGNE_TEINTEE_HEX)
    element.append(paire)

    # Texte de l'en-tête, posé sur les cellules par cerema-docx.lua : la couleur
    # de la première ligne du style de tableau est ignorée par LibreOffice.
    caractere = document.styles.add_style("Tableau entête", WD_STYLE_TYPE.CHARACTER)
    caractere.font.bold = True
    caractere.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    entete = OxmlElement("w:tblStylePr")
    entete.set(qn("w:type"), "firstRow")
    rpr = OxmlElement("w:rPr")
    rpr.append(OxmlElement("w:b"))
    couleur = OxmlElement("w:color")
    couleur.set(qn("w:val"), "FFFFFF")
    rpr.append(couleur)
    entete.append(rpr)
    fond(entete, INDIGO_HEX)
    element.append(entete)


def assombrir(couleur: str, proportion: float) -> str:
    """Mélange une couleur avec du noir, comme ``darken`` de Typst (approché).

    Args:
        couleur: Couleur hexadécimale sans dièse.
        proportion: Part de noir, entre 0 et 1.

    Returns:
        La couleur assombrie, hexadécimale sans dièse.
    """
    canaux = [int(couleur[i : i + 2], 16) for i in (0, 2, 4)]
    return "".join(f"{round(c * (1 - proportion)):02X}" for c in canaux)


COULEURS_ENCADRES: dict[str, str] = {
    "note": JETONS["indigo"][1:],
    "tip": JETONS["vert"][1:],
    "warning": assombrir(JETONS["jaune"][1:], 0.25),
    "important": JETONS["corail"][1:],
    "caution": assombrir(JETONS["corail"][1:], 0.25),
}
"""Type d'encadré Quarto -> couleur, comme dans le gabarit Typst."""


def styles_encadres(document: Document) -> None:
    """Crée les styles de paragraphe des encadrés, repris par cerema-docx.lua.

    Pour chaque type : « Encadré <type> » (corps : filet coloré de 3 pt à
    gauche, fond éclairci à 92 %) et « Encadré <type> titre » (même cadre,
    texte gras de la couleur du type). « Encadré fin » ménage l'espace sous
    l'encadré.

    Args:
        document: Document de référence modifié sur place.
    """
    s = document.styles
    for type_encadre, couleur in COULEURS_ENCADRES.items():
        corps = s.add_style(f"Encadré {type_encadre}", WD_STYLE_TYPE.PARAGRAPH)
        corps.base_style = s["Body Text"]
        corps.quick_style = False
        texte(corps, POLICE_TEXTE, 10.5, NOIR)
        espacement(corps, 0, 0)
        corps.paragraph_format.left_indent = Cm(0.3)
        corps.paragraph_format.right_indent = Cm(0.1)
        filet(corps, "left", couleur, 24, 8)
        ppr = corps.element.get_or_add_pPr()
        trame = OxmlElement("w:shd")
        trame.set(qn("w:val"), "clear")
        trame.set(qn("w:color"), "auto")
        trame.set(qn("w:fill"), eclaircir(couleur, 0.92))
        ppr.append(trame)

        titre = s.add_style(f"Encadré {type_encadre} titre", WD_STYLE_TYPE.PARAGRAPH)
        titre.base_style = corps
        titre.quick_style = False
        titre.font.bold = True
        titre.font.color.rgb = RGBColor.from_string(couleur)
        titre.paragraph_format.space_before = Pt(10)
        titre.paragraph_format.keep_with_next = True

    fin = s.add_style("Encadré fin", WD_STYLE_TYPE.PARAGRAPH)
    fin.base_style = s["Body Text"]
    fin.quick_style = False
    fin.font.size = Pt(4)
    espacement(fin, 0, 4)


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
    styles_encadres(document)
    entetes_et_pieds(document)
    document.save(str(sortie))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    construire(Path(sys.argv[1]), Path(sys.argv[2]))
