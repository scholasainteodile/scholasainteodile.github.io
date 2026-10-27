"""Build the static pages of the Schola Sainte-Odile site.

Each page body lives in pages/<name>.html; this script wraps it with the
shared head, navigation and footer, and writes <name>.html at the root.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
SITE_URL = "https://scholasainteodile.fr"
# Keep search engines away until the placeholders are filled in.
NOINDEX = False
CHORISTERS_URL = "https://scholasainteodile.fr/espace-choristes/"

PAGES = [
    # (file, nav label, <title>, meta description)
    ("index", "Accueil", "Schola Sainte-Odile – Chœur liturgique à Paris 17e : grégorien, motets, cantiques",
     "Chœur de l'église Sainte-Odile (Paris 17e) : chant grégorien, polyphonie, motets et cantiques au service de la liturgie traditionnelle."),
    ("offices", "Prochains offices", "Prochains offices chantés en grégorien – Sainte-Odile, Paris 17e",
     "Programme des messes chantées par la Schola Sainte-Odile : propre grégorien et ordinaire de chaque dimanche et fête."),
    ("partitions", "Partitions", "Partitions grégoriennes – Schola Sainte-Odile",
     "Partitions grégoriennes chantées par la Schola Sainte-Odile, Paris 17e."),
    ("ecouter", "Écouter", "Écouter la Schola Sainte-Odile – chant grégorien, Paris 17e",
     "Enregistrements de la Schola Sainte-Odile : introïts, graduels, hymnes et antiennes grégoriennes."),
    ("rejoindre", "Nous rejoindre", "Rejoindre la Schola Sainte-Odile – chœur grégorien à Paris 17e",
     "Rejoindre la Schola Sainte-Odile : répétitions le vendredi soir à l'église Sainte-Odile, Paris 17e. Toutes les voix sont recherchées."),
    ("divers", "Divers", "Divers – Schola Sainte-Odile",
     "Documents utiles de la Schola Sainte-Odile, Paris 17e : calendrier propre de Paris."),
]

# Pages kept in pages/ but not published for now.
HIDDEN = {"ecouter"}

SCHEMA = {
    "@context": "https://schema.org",
    "@type": "MusicGroup",
    "name": "Schola Sainte-Odile",
    "url": SITE_URL + "/",
    "alternateName": ["Chœur grégorien de Sainte-Odile", "Chorale de l'église Sainte-Odile"],
    "genre": ["Chant grégorien", "Plain-chant", "Polyphonie sacrée", "Musique sacrée", "Motets", "Cantiques"],
    "description": "Chœur liturgique de l'église Sainte-Odile (Paris 17e) : chant grégorien, polyphonie, "
                   "motets et cantiques au service de la liturgie traditionnelle.",
    "keywords": "chœur grégorien Paris, chorale grégorienne, plain-chant, schola, chant grégorien Paris 17e, "
                "musique sacrée, polyphonie, messe traditionnelle, liturgie traditionnelle, chorale paroissiale, "
                "chœur liturgique, chorale liturgique, messe de saint Pie V, messe tridentine, "
                "forme extraordinaire du rite romain, missel de 1962",
    "email": "scholasainteodile@gmail.com",
    "image": SITE_URL + "/images/apercu-partage.jpg",
    "logo": SITE_URL + "/apple-touch-icon.png",
    "areaServed": {"@type": "City", "name": "Paris"},
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
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="google-site-verification" content="M3VZghlCGwG6WWZfvN73WMn9SONsfBhNgNC5m83VB0o">
{robots}
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="Schola Sainte-Odile">
<meta property="og:locale" content="fr_FR">
<meta property="og:image" content="{site}/images/apercu-partage.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Schola Sainte-Odile : incipit grégorien Cantate Domino canticum novum">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Alegreya:ital,wght@0,400;0,600;1,400&family=Alegreya+SC:wght@500&family=Uncial+Antiqua&display=swap">
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
<div class="staff-wrap">{staff}</div>
<main>
{body}
</main>
<footer class="site-foot">
  <span>Schola Sainte-Odile · Église Sainte-Odile, 2, avenue Stéphane-Mallarmé, 75017 Paris · Métro ligne 3 et tram T3b, Porte de Champerret</span>
  <span>En lien avec l'<a href="https://www.orguesainteodileparis.fr/">Association musicale de Sainte-Odile</a> et la <a href="https://sainteodile.fr/">paroisse Sainte-Odile</a>.</span>
</footer>
<!-- Visit counter (GoatCounter, no cookies): https://scholasainteodile.goatcounter.com -->
<script data-goatcounter="https://scholasainteodile.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
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
        staff = (ROOT / "pages" / "_staff.svg").read_text(encoding="utf-8")
        html = TEMPLATE.format(title=title, site=SITE_URL, description=description, canonical=canonical,
                               schema=schema, nav=nav,
                               robots='<meta name="robots" content="noindex">' if NOINDEX else "", body=body.strip(), staff=staff, choristers=CHORISTERS_URL)
        (ROOT / f"{name}.html").write_text(html, encoding="utf-8")
        print("built", name)


if __name__ == "__main__":
    build()
