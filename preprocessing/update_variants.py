import json
import re

from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent

INPUT_JSON = PROJECT_ROOT / "cleaning" / "pokemon_cleaned.json"
OUTPUT_JSON = CURRENT_DIR / "pokemon_cleaned_variants.json"
VARIANT_FILE = CURRENT_DIR / "variants.json"


# -------------------------------------------------------
# Load variants
# -------------------------------------------------------

with open(VARIANT_FILE, "r", encoding="utf-8") as f:
    OFFICIAL_VARIANTS = sorted(json.load(f), key=len, reverse=True)


# -------------------------------------------------------
# Normalize whitespace
# -------------------------------------------------------

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


# -------------------------------------------------------
# Split species + variant
# -------------------------------------------------------

def split_species_variant(name: str):

    name = clean_text(name)

    # Variant at beginning

    for variant in OFFICIAL_VARIANTS:

        if name.startswith(variant + " "):
            species = name[len(variant):].strip()
            return species, variant

    # Variant at end

    for variant in OFFICIAL_VARIANTS:

        if name.endswith(" " + variant):
            species = name[:-len(variant)].strip()
            return species, variant

    return name, None


# -------------------------------------------------------
# Process JSON
# -------------------------------------------------------

with open(INPUT_JSON, "r", encoding="utf-8") as f:
    pokemon = json.load(f)

    for entry in pokemon:

        original_name = clean_text(entry.pop("name"))

        species, variant = split_species_variant(original_name)

        entry["species"] = species
        entry["variant"] = variant

        if entry.get("secondary_type") is None:
            entry["secondary_type"] = "Not Applicable"
            
        if entry.get("variant") is None:
            entry["variant"] = "Not Applicable"


    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(pokemon, f, indent=4, ensure_ascii=False)

    print(f"Processed {len(pokemon)} Pokémon.")
    print(f"Saved to {OUTPUT_JSON}")