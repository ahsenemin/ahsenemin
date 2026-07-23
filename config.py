"""
Central config for the GitHub profile art pipeline.
Fill these in before running any script.
"""

# Your GitHub username. The repo itself must also be named exactly this
# (github.com/<username>/<username>) for the README to show on your profile.
GITHUB_USERNAME = "ahsenemin"

# --- files -------------------------------------------------------------
SOURCE_PHOTO = "source-photo.jpg"        # your original photo, put it in repo root
PREPPED_PHOTO = "source-prepped.png"     # produced by prep_photo.py

ASCII_SVG = "avi-ascii.svg"
INFO_CARD_SVG = "info-card.svg"
HEATMAP_SVG = "contrib-heatmap.svg"
CONTRIB_JSON = "data/contributions.json"

# --- info card content ---------------------------------------------------
# This is just a starting point - edit freely to match how you want to
# present yourself.
INFO_CARD = {
    "now": "TEKNOFEST 2026 - TR-ackAI (Akilli Yol Guvenligi, 5G + AI)",
    "prev": "Mobil Uygulama Gelistirme Kulubu - Baskan Yardimcisi",
    "stack": ["PHP", "MySQL", "Vue 3", "Quasar", "TypeScript", "Deno", "Python"],
    "highlights": [
        "TR-ackAI - OTR asamasi 91/100",
        "Full-stack web & mobil projeler",
        "Ozel CMS + tema sistemi gelistirme",
    ],
}
