"""Génère les jetons couleur de l'extension à partir du design system Cerema.

Source unique : ``sources/tokens.json``, copie du fichier ``project/tokens.json``
du design system Cerema. Le script écrit :

- ``_extensions/cerema/cerema-jetons.scss`` : variables SCSS, partagées par les
  thèmes revealjs et html (le fichier doit venir en dernier dans ``theme:``,
  car Quarto place en tête les valeurs par défaut des derniers fichiers) ;
- ``_extensions/cerema/jetons.json`` : nom -> couleur hexadécimale, lu par
  ``cerema_altair.py`` et ``outils/construire_reference_docx.py`` ;
- le bloc compris entre ``// <jetons>`` et ``// </jetons>`` de
  ``_extensions/cerema/typst-template.typ``.

Usage :
    uv run python outils/generer_jetons.py
"""

import json
import re
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "sources" / "tokens.json"
EXTENSION = RACINE / "_extensions" / "cerema"
SCSS = EXTENSION / "cerema-jetons.scss"
JSON = EXTENSION / "jetons.json"
TYPST = EXTENSION / "typst-template.typ"

EN_TETE = (
    "Généré par outils/generer_jetons.py depuis sources/tokens.json : ne pas modifier."
)
BLOC_TYPST = re.compile(r"(// <jetons>\n).*?(// </jetons>)", re.DOTALL)


def lire_couleurs(source: Path) -> dict[str, str]:
    """Extrait les couleurs du thème clair, dans l'ordre du design system.

    Args:
        source: Fichier tokens.json du design system.

    Returns:
        Dictionnaire nom du jeton -> couleur hexadécimale en majuscules.
    """
    jetons = json.loads(source.read_text(encoding="utf-8"))
    couleurs: dict[str, str] = {}
    for jeton in jetons["color"]["tokens"]:
        valeur = jeton["value"]
        if isinstance(valeur, dict):
            valeur = next(iter(valeur.values()))
        couleurs[jeton["name"]] = valeur.upper()
    return couleurs


def ecrire_scss(couleurs: dict[str, str]) -> None:
    """Écrit les variables SCSS des jetons couleur.

    Args:
        couleurs: Jetons nom -> couleur.
    """
    lignes = ["/*-- scss:defaults --*/", "", f"// {EN_TETE}"]
    lignes += [f"${nom}: {valeur};" for nom, valeur in couleurs.items()]
    SCSS.write_text("\n".join(lignes) + "\n", encoding="utf-8")


def ecrire_json(couleurs: dict[str, str]) -> None:
    """Écrit la table nom -> couleur lue par les scripts Python.

    Args:
        couleurs: Jetons nom -> couleur.
    """
    JSON.write_text(
        json.dumps(couleurs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def ecrire_typst(couleurs: dict[str, str]) -> None:
    """Remplace le bloc de jetons du gabarit Typst.

    Args:
        couleurs: Jetons nom -> couleur.

    Raises:
        ValueError: Si les balises du bloc sont absentes du gabarit.
    """
    gabarit = TYPST.read_text(encoding="utf-8")
    largeur = max(len(nom) for nom in couleurs)
    corps = f"// {EN_TETE}\n" + "".join(
        f'#let {nom.ljust(largeur)} = rgb("{valeur}")\n'
        for nom, valeur in couleurs.items()
    )
    nouveau, remplacements = BLOC_TYPST.subn(
        lambda m: m.group(1) + corps + m.group(2), gabarit
    )
    if remplacements != 1:
        raise ValueError(f"{TYPST} : balises // <jetons> et // </jetons> introuvables")
    TYPST.write_text(nouveau, encoding="utf-8")


def main() -> None:
    """Régénère les trois sorties à partir de sources/tokens.json."""
    couleurs = lire_couleurs(SOURCE)
    ecrire_scss(couleurs)
    ecrire_json(couleurs)
    ecrire_typst(couleurs)


if __name__ == "__main__":
    main()
