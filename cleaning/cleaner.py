import json

from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent

INPUT_FILE = PROJECT_ROOT / "pokemonDB.json"
OUTPUT_FILE = CURRENT_DIR / "pokemon_cleaned.json"

# Load original dataset
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

cleaned_data = []

# Iterate through every Pokémon
for pokemon in data["Pokemon"].values():

    cleaned_entry = {
        "dex_number": pokemon.get("dex_number"),
        "name": pokemon.get("name", "").strip(),
        "type": pokemon.get("primary_type"),
        "secondary_type": pokemon.get("secondary_type"),
        "stats": {
            "hp": pokemon.get("stats", {}).get("HP"),
            "bst": pokemon.get("stats", {}).get("BST"),
            "attack": pokemon.get("stats", {}).get("ATA"),
            "defense": pokemon.get("stats", {}).get("DEF"),
            "special_attack": pokemon.get("stats", {}).get("SPA"),
            "special_defense": pokemon.get("stats", {}).get("SPD"),
            "speed": pokemon.get("stats", {}).get("SPE")
        },
        "abilities": pokemon.get("abilities", []),
        "hidden_ability": pokemon.get("hidden_ability")
    }

    cleaned_data.append(cleaned_entry)

# Optional: sort by Dex number
cleaned_data.sort(key=lambda x: x["dex_number"])

# Save cleaned JSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, indent=4, ensure_ascii=False)

print(f"Cleaned dataset saved to '{OUTPUT_FILE}'")
print(f"Total Pokémon entries: {len(cleaned_data)}")