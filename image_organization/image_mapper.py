import json
from pathlib import Path
import sys

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent

# ==========================================================
# CONFIG
# ==========================================================

INPUT_JSON = (
    PROJECT_ROOT
    / "preprocessing"
    / "pokemon_cleaned_variants.json"
)

OUTPUT_JSON = (
    CURRENT_DIR
    / "pokemon_cleaned_images.json"
)

STATIC_DIR = (
    PROJECT_ROOT
    / "static"
)

IMAGE_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".webp"
}

# ==========================================================
# UTF-8 OUTPUT
# ==========================================================

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


# ==========================================================
# CHECK IF IMAGES ARE ALREADY ORGANIZED
# ==========================================================

def images_already_organized():
    """
    Checks whether Pokémon images are already organized
    inside numeric Dex-number folders.

    Expected structure:

        static/
            1/
                1.png
            6/
                6.png
                6-mega-x.png
                6-mega-y.png
            19/
                19.png
                19-alolan.png

    Returns:
        True  -> Images are already organized
        False -> Images are not organized
    """

    if not STATIC_DIR.exists():
        return False

    # ------------------------------------------------------
    # Check for images directly inside static/
    # ------------------------------------------------------

    for item in STATIC_DIR.iterdir():

        if (
            item.is_file()
            and item.suffix.lower() in IMAGE_EXTENSIONS
        ):
            return False

    # ------------------------------------------------------
    # Find Dex-number folders
    # ------------------------------------------------------

    dex_folders = [
        item
        for item in STATIC_DIR.iterdir()
        if item.is_dir()
        and item.name.isdigit()
    ]

    if not dex_folders:
        return False

    # ------------------------------------------------------
    # Make sure Dex folders actually contain images
    # ------------------------------------------------------

    for folder in dex_folders:

        for file in folder.iterdir():

            if (
                file.is_file()
                and file.suffix.lower() in IMAGE_EXTENSIONS
            ):
                return True

    return False


# ==========================================================
# LOAD DATA
# ==========================================================

with open(INPUT_JSON, "r", encoding="utf-8") as f:
    pokemon_data = json.load(f)


# ==========================================================
# HELPERS
# ==========================================================

def normalize_variant(variant: str | None) -> str | None:
    """
    Converts variant names into filename format.

    Example:
        Mega X -> mega-x
        Combat Breed -> combat-breed
    """

    if variant is None:
        return None

    return (
        variant
        .lower()
        .replace(" ", "-")
        .strip()
    )


# ==========================================================
# MAP IMAGES
# ==========================================================

mapped = 0
missing = 0

print("\n" + "=" * 70)
print("Mapping Images")
print("=" * 70)


for pokemon in pokemon_data:

    dex = str(pokemon["dex_number"]).strip()

    # ------------------------------------------------------
    # IMPORTANT:
    # Images are stored inside:
    #
    # static/<dex>/
    #
    # Example:
    # static/6/6.png
    # static/6/6-mega-x.png
    # ------------------------------------------------------

    folder = STATIC_DIR / dex

    image_path = None

    # ------------------------------------------------------
    # Root Pokémon
    # ------------------------------------------------------

    if pokemon.get("variant") is None:

        filename_candidates = [
            f"{dex}.png",
            f"{dex}.jpg",
            f"{dex}.jpeg",
            f"{dex}.webp"
        ]

    # ------------------------------------------------------
    # Variant Pokémon
    # ------------------------------------------------------

    else:

        variant = normalize_variant(
            pokemon["variant"]
        )

        filename_candidates = [
            f"{dex}-{variant}.png",
            f"{dex}-{variant}.jpg",
            f"{dex}-{variant}.jpeg",
            f"{dex}-{variant}.webp"
        ]

    # ------------------------------------------------------
    # Search for image
    # ------------------------------------------------------

    for filename in filename_candidates:

        candidate = folder / filename

        if candidate.exists():

            image_path = candidate

            break

    # ------------------------------------------------------
    # Image found
    # ------------------------------------------------------

    if image_path:

        pokemon["image"] = image_path.as_posix()

        mapped += 1

        print(
            f"Mapped    : "
            f"{pokemon['species']} "
            f"({pokemon.get('variant')}) "
            f"-> {image_path.as_posix()}"
        )

    # ------------------------------------------------------
    # Image missing
    # ------------------------------------------------------

    else:

        pokemon["image"] = None

        missing += 1

        print(
            f"Missing Image : "
            f"{pokemon['species']} "
            f"({pokemon.get('variant')})"
        )


# ==========================================================
# SAVE
# ==========================================================

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:

    json.dump(
        pokemon_data,
        f,
        indent=4,
        ensure_ascii=False
    )


# ==========================================================
# SUMMARY
# ==========================================================

print("\n" + "=" * 70)
print("Image Mapping Complete")
print("=" * 70)

print(f"Mapped  : {mapped}")
print(f"Missing : {missing}")

print("=" * 70)