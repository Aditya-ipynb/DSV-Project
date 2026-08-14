import json

from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent

OFFICIAL_VARIANTS = sorted({

    # Mega
    "Mega",
    "Mega X",
    "Mega Y",

    # Regional Forms
    "Alolan",
    "Galarian",
    "Hisuian",
    "Paldean",

    # Tauros
    "Combat Breed",
    "Blaze Breed",
    "Aqua Breed",

    # Pikachu
    "Partner",
    "Belle",
    "Libre",
    "PhD",
    "Pop Star",
    "Rock Star",
    "Cosplay",

    # Kyurem
    "Black",
    "White",

    # Necrozma
    "Dusk Mane",
    "Dawn Wings",
    "Ultra",

    # Shaymin
    "Sky Forme",

    # Giratina
    "Origin Forme",
    "Altered Forme",

    # Tornadus / Thundurus / Landorus / Enamorus
    "Incarnate Forme",
    "Therian Forme",

    # Deoxys
    "Attack Forme",
    "Defense Forme",
    "Speed Forme",

    # Lycanroc
    "Midday Form",
    "Midnight Form",
    "Dusk Form",

    # Wishiwashi
    "School Form",
    "Solo Form",

    # Zygarde
    "10% Forme",
    "50% Forme",
    "Complete Forme",

    # Keldeo
    "Ordinary Form",
    "Resolute Form",

    # Zacian/Zamazenta
    "Crowned Sword",
    "Crowned Shield",

    # Ogerpon
    "Teal Mask",
    "Wellspring Mask",
    "Hearthflame Mask",
    "Cornerstone Mask",

    # Rotom
    "Heat",
    "Wash",
    "Frost",
    "Fan",
    "Mow",

    # Calyrex
    "Ice Rider",
    "Shadow Rider",

    # Ursaluna
    "Bloodmoon",

    # Misc
    "Ash",
    "Male",
    "Female"

}, key=len, reverse=True)

OUTPUT_FILE = CURRENT_DIR / "variants.json"

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(OFFICIAL_VARIANTS, f, indent=4)

print(f"Saved {len(OFFICIAL_VARIANTS)} variants.")
print(f"Location : {OUTPUT_FILE}")