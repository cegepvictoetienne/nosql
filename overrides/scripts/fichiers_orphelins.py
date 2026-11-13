"""Liste les fichiers du wiki (pages, images, etc.) qui ne sont référencés nulle part.

Un fichier est considéré comme référencé s'il apparaît :
  - dans un lien ou une image Markdown : [texte](chemin), ![alt](chemin), [id]: chemin
  - dans un attribut HTML src="..." ou href="..." d'un fichier Markdown
  - dans zensical.toml (nav, logo, favicon, extra_css...)

Utilisation :
    python overrides/scripts/fichiers_orphelins.py

Code de sortie : 0 si aucun fichier orphelin, 1 sinon.
N'utilise que la bibliothèque standard.
"""

import re
import sys
import urllib.parse
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
WIKI = RACINE / "wiki"
CONFIG = RACINE / "zensical.toml"

FICHIERS_IGNORES = {".DS_Store", "Thumbs.db"}

# Liens Markdown inline : ](chemin) ou ](chemin "titre") ou ](<chemin avec espaces>)
MD_LINK_RE = re.compile(r"\]\(\s*<?([^)\s>]+)")
# Définitions de référence : [id]: chemin
MD_REF_RE = re.compile(r"^\s*\[[^\]]+\]:\s*<?(\S+?)>?(?:\s|$)", re.MULTILINE)
# Attributs HTML
HTML_ATTR_RE = re.compile(r"""(?:src|href|data-src|poster)\s*=\s*["']([^"']+)["']""", re.IGNORECASE)
# Chaînes entre guillemets dans le fichier de configuration
TOML_STR_RE = re.compile(r"""["']([^"'\s]+\.[A-Za-z0-9]+)["']""")


def normaliser(cible: str, base: Path):
    """Transforme une cible de lien en chemin absolu, ou None si c'est un lien externe."""
    if re.match(r"^[a-z][a-z0-9+.-]*:", cible, re.IGNORECASE) or cible.startswith("#"):
        return None  # http:, https:, mailto:, data:, ancre interne...
    cible = urllib.parse.unquote(cible.split("#", 1)[0].split("?", 1)[0])
    if not cible:
        return None
    chemin = WIKI / cible.lstrip("/") if cible.startswith("/") else base / cible
    return chemin.resolve()


def main():
    tous = {
        f.resolve()
        for f in WIKI.rglob("*")
        if f.is_file() and f.name not in FICHIERS_IGNORES
    }

    references = set()
    for page in WIKI.rglob("*.md"):
        texte = page.read_text(encoding="utf-8")
        for regex in (MD_LINK_RE, MD_REF_RE, HTML_ATTR_RE):
            for cible in regex.findall(texte):
                chemin = normaliser(cible, page.parent)
                if chemin is None:
                    continue
                references.add(chemin)
                # Avec use_directory_urls, un lien vers « page/ » pointe vers page.md ou page/index.md.
                if chemin.suffix == "":
                    references.update({chemin.with_suffix(".md"), chemin / "index.md"})

    if CONFIG.exists():
        for cible in TOML_STR_RE.findall(CONFIG.read_text(encoding="utf-8")):
            chemin = normaliser(cible, WIKI)
            if chemin is not None:
                references.add(chemin)

    # La page d'accueil est toujours accessible.
    references.add((WIKI / "index.md").resolve())

    orphelins = sorted(tous - references)
    if orphelins:
        print(f"=== {len(orphelins)} fichier(s) non référencé(s) sur {len(tous)} ===")
        for f in orphelins:
            print(f"  {f.relative_to(RACINE)}")
    else:
        print(f"Tous les {len(tous)} fichiers sont référencés.")

    sys.exit(1 if orphelins else 0)


if __name__ == "__main__":
    main()
