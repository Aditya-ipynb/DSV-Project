import json
from pathlib import Path
import sys

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent

# ==========================================================
# CONFIG
# ==========================================================

STATIC_DIR = PROJECT_ROOT / "static"

POKEMON_JSON = (
    PROJECT_ROOT
    / "preprocessing"
    / "pokemon.json"
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
# CHECK IF STATIC DIRECTORY IS ALREADY ORGANIZED
# ==========================================================

def is_static_organized():
    """
    Returns True if static/ already contains Pokémon images
    organized inside numeric Dex-number folders.

    Expected:

        static/
            1/
                1.png
            2/
                2.png
            6/
                6.png
                6-mega-x.png
                6-mega-y.png

    Returns:
        True  -> Images are already organized
        False -> Organization is not complete
    """

    if not STATIC_DIR.exists():
        return False

    # If there are images directly inside static/,
    # the directory is not organized.
    for item in STATIC_DIR.iterdir():

        if item.is_file() and item.suffix.lower() in IMAGE_EXTENSIONS:
            return False

    # Find numeric Dex folders containing images
    dex_folders = [
        folder
        for folder in STATIC_DIR.iterdir()
        if folder.is_dir() and folder.name.isdigit()
    ]

    # No Dex folders means images haven't been organized
    if not dex_folders:
        return False

    # Make sure the Dex folders actually contain images
    for folder in dex_folders:

        has_image = any(
            file.is_file()
            and file.suffix.lower() in IMAGE_EXTENSIONS
            for file in folder.iterdir()
        )

        if not has_image:
            return False

    return True


# ==========================================================
# SKIP IF ALREADY ORGANIZED
# ==========================================================

if is_static_organized():

    print("\n" + "=" * 70)
    print("IMAGE ORGANIZATION CHECK")
    print("=" * 70)
    print("Images are already organized.")
    print("Skipping image mapping.")
    print("=" * 70)

    sys.exit(0)


# ==========================================================
# FIND IMAGE
# ==========================================================

def find_image(dex_number, variant):
    """
    Find a Pokémon image inside the organized static directory.

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
    """

    dex_number = str(dex_number).strip()

    pokemon_folder = STATIC_DIR / dex_number

    if not pokemon_folder.exists():
        return None

    # ======================================================
    # NORMAL / DEFAULT POKEMON
    # ======================================================

    if not variant or variant.lower() in {
        "not applicable",
        "none",
        "normal",
        ""
    }:

        for extension in IMAGE_EXTENSIONS:

            image_path = (
                pokemon_folder
                / f"{dex_number}{extension}"
            )

            if image_path.exists():
                return image_path

        return None

    # ======================================================
    # VARIANT
    # ======================================================

    variant_name = (
        str(variant)
        .strip()
        .lower()
        .replace(" ", "-")
    )

    filename = f"{dex_number}-{variant_name}"

    for extension in IMAGE_EXTENSIONS:

        image_path = (
            pokemon_folder
            / f"{filename}{extension}"
        )

        if image_path.exists():
            return image_path

    return None


# ==========================================================
# LOAD POKEMON DATA
# ==========================================================

with open(POKEMON_JSON, "r", encoding="utf-8") as f:
    pokemon_data = json.load(f)


# ==========================================================
# MAP IMAGES
# ==========================================================

mapped_count = 0
missing_count = 0

print("\n" + "=" * 70)
print("Mapping Images")
print("=" * 70)


for pokemon in pokemon_data:

    dex_number = pokemon["dex_number"]
    species = pokemon["species"]
    variant = pokemon.get("variant", "Not Applicable")

    image_path = find_image(
        dex_number,
        variant
    )

    # ------------------------------------------------------
    # IMAGE FOUND
    # ------------------------------------------------------

    if image_path:

        pokemon["image"] = str(
            image_path.relative_to(PROJECT_ROOT)
        ).replace("\\", "/")

        mapped_count += 1

        print(
            f"Mapped    : "
            f"{species} ({variant}) "
            f"-> {pokemon['image']}"
        )

    # ------------------------------------------------------
    # IMAGE MISSING
    # ------------------------------------------------------

    else:

        pokemon["image"] = None

        missing_count += 1

        print(
            f"Missing Image : "
            f"{species} ({variant})"
        )


# ==========================================================
# SUMMARY
# ==========================================================

print("\n" + "=" * 70)
print("IMAGE MAPPING COMPLETE")
print("=" * 70)

print(f"Mapped Images  : {mapped_count}")
print(f"Missing Images : {missing_count}")

print("=" * 70)