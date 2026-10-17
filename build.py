"""Build the static pages of the Schola Sainte-Odile site.

Each page body lives in pages/<name>.html; this script wraps it with the
shared head, navigation and footer, and writes <name>.html at the root.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
SITE_URL = "https://scholasainteodile.github.io"
# Keep search engines away until the placeholders are filled in.
NOINDEX = True
CHORISTERS_URL = "https://scholasainteodile.github.io/espace-choristes/"

PAGES = [
    # (file, nav label, <title>, meta description)
    ("index", "Accueil", "Schola Sainte-Odile – Chant grégorien à Paris 17e",
     "La Schola Sainte-Odile chante le grégorien à la liturgie de l'église Sainte-Odile, Paris 17e. "
     "Offices, répertoire, enregistrements, nous rejoindre."),
    ("offices", "Prochains offices", "Prochains offices chantés en grégorien – Sainte-Odile, Paris 17e",
     "Programme des messes et offices chantés en grégorien par la Schola Sainte-Odile : propre, ordinaire et pièces de chaque dimanche."),
    ("partitions", "Partitions", "Partitions grégoriennes – Schola Sainte-Odile",
     "Partitions grégoriennes libres de droits chantées par la Schola Sainte-Odile, Paris 17e."),
    ("ecouter", "Écouter", "Écouter la Schola Sainte-Odile – chant grégorien, Paris 17e",
     "Enregistrements de la Schola Sainte-Odile : introïts, graduels, hymnes et antiennes grégoriennes."),
    ("rejoindre", "Nous rejoindre", "Rejoindre la Schola Sainte-Odile – chœur grégorien à Paris 17e",
     "Chanter le grégorien à Sainte-Odile, Paris 17e : répétitions, voix recherchées, contact."),
]

# Pages kept in pages/ but not published for now.
HIDDEN = {"ecouter"}

SCHEMA = {
    "@context": "https://schema.org",
    "@type": "MusicGroup",
    "name": "Schola Sainte-Odile",
    "url": SITE_URL + "/",
    "genre": "Chant grégorien",
    "description": "Chœur grégorien de l'église Sainte-Odile, Paris 17e, au service de la liturgie traditionnelle.",
    "location": {
        "@type": "Church",
        "name": "Église Sainte-Odile",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "2, avenue Stéphane-Mallarmé",
            "postalCode": "75017",
            "addressLocality": "Paris",
            "addressCountry": "FR",
        },
    },
}

TEMPLATE = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{description}">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alegreya:ital,wght@0,400;0,600;1,400&family=Alegreya+SC:wght@500&display=swap">
<link rel="stylesheet" href="style.css">
{schema}
</head>
<body>
<header class="site-head">
  <a class="brand" href="index.html">Schola Sainte-Odile</a>
  <nav aria-label="Menu principal"><ul>
{nav}
    <li><a class="choristes" href="{choristers}">Espace choristes</a></li>
  </ul></nav>
</header>
<main>
{body}
</main>
<footer class="site-foot">
  <span>Schola Sainte-Odile · Église Sainte-Odile, 2, avenue Stéphane-Mallarmé, 75017 Paris · Métro ligne 3 et tram T3b, Porte de Champerret</span>
  <span>En lien avec l'<a href="https://www.orguesainteodileparis.fr/">Association musicale de Sainte-Odile</a> et la <a href="https://sainteodile.fr/">paroisse Sainte-Odile</a>.</span>
</footer>
</body>
</html>
"""


def build():
    published = [page for page in PAGES if page[0] not in HIDDEN]
    for name in HIDDEN:
        (ROOT / f"{name}.html").unlink(missing_ok=True)
    for name, label, title, description in published:
        nav = "\n".join(
            f'    <li><a href="{p}.html"{" aria-current=\"page\"" if p == name else ""}>{l}</a></li>'
            for p, l, _, _ in published
        )
        canonical = SITE_URL + "/" + ("" if name == "index" else f"{name}.html")
        schema = ""
        if name == "index":
            schema = '<script type="application/ld+json">' + json.dumps(SCHEMA, ensure_ascii=False) + "</script>"
        body = (ROOT / "pages" / f"{name}.html").read_text(encoding="utf-8")
        html = TEMPLATE.format(title=title, description=description, canonical=canonical,
                               schema=schema, nav=nav,
                               robots='<meta name="robots" content="noindex">' if NOINDEX else "", body=body.strip(), choristers=CHORISTERS_URL)
        (ROOT / f"{name}.html").write_text(html, encoding="utf-8")
        print("built", name)


if __name__ == "__main__":
    build()
