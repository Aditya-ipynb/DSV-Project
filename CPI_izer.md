# CPI_izer

**CPI_izer** (Cleaning, Preprocessing and Image-izer) is a reusable lightweight data preprocessing pipeline for the Pokémon dataset used in this project. It automates the transformation of the raw scraped dataset into a clean, standardized, and ML-ready dataset with correctly mapped images.

The pipeline is designed to be executed **once** whenever the Pokémon database or image collection is updated.

---

## Pipeline Flow

```
pokemonDB.json
        │
        ▼
Cleaning
(cleaner.py)
        │
        ▼
pokemon_cleaned.json
        │
        ▼
Preprocessing
(generate_variants.py)
        │
        ▼
variants.json
        │
        ▼
(update_variants.py)
        │
        ▼
pokemon_cleaned_variants.json
        │
        ▼
Image Organization
(image_organizer.py)
        │
        ▼
Organized static/ directory
        │
        ▼
(image_mapper.py)
        │
        ▼
pokemon_cleaned_images.json
```

---

## Stages

### 1. Cleaning

**Script:** `cleaning/cleaner.py`

- Reads the raw `pokemonDB.json`
- Removes unnecessary fields
- Standardizes attribute names
- Sorts Pokémon by Pokédex number
- Produces:

```
cleaning/pokemon_cleaned.json
```

---

### 2. Variant Generation

**Script:** `preprocessing/generate_variants.py`

Generates a standardized list of official Pokémon variant names.

Examples include:

- Mega
- Mega X
- Mega Y
- Alolan
- Galarian
- Hisuian
- Combat Breed
- Bloodmoon
- etc.

Produces:

```
preprocessing/variants.json
```

---

### 3. Variant Extraction

**Script:** `preprocessing/update_variants.py`

Processes every Pokémon entry and separates:

- Root species
- Variant

Example:

| Original Name | Species | Variant |
|--------------|---------|---------|
| Mega Charizard X | Charizard | Mega X |
| Tauros Combat Breed | Tauros | Combat Breed |
| Bulbasaur | Bulbasaur | None |

Produces:

```
preprocessing/pokemon_cleaned_variants.json
```

---

### 4. Image Organization

**Script:** `image_organization/image_organizer.py`

Organizes Pokémon images into folders using their National Pokédex number, if not done already.

Example:

```
static/

6/
    6.png
    6-mega-x.png
    6-mega-y.png

25/
    25.png
    25-belle.png
```

Unknown image variants are reported during execution.

---

### 5. Image Mapping

**Script:** `image_organization/image_mapper.py`

Matches each Pokémon entry with its corresponding image using:

- Pokédex Number
- Variant Name

Adds a new field:

```json
"image": "static/6/6-mega-x.png"
```

Produces the final dataset:

```
image_organization/pokemon_cleaned_images.json
```

---

## Final Dataset

The final dataset contains:

- Pokédex Number
- Species
- Variant
- Types
- Base Stats
- Abilities
- Hidden Ability
- Relative Image Path

This serves as the single source of truth for the machine learning models, recommendation engine, team builder, and future applications.

---

## Running the Pipeline

Execute the complete preprocessing pipeline using:

```bash
python CPIizer.py
```

The pipeline automatically performs every stage in sequence and generates the final processed dataset without requiring manual intervention.

---

## Output Files

| Stage | Output |
|--------|--------|
| Cleaning | `cleaning/pokemon_cleaned.json` |
| Variant Generation | `preprocessing/variants.json` |
| Variant Extraction | `preprocessing/pokemon_cleaned_variants.json` |
| Image Mapping | `image_organization/pokemon_cleaned_images.json` |

---

## Future Scope

CPI_izer has been designed to be modular, making it easy to extend with additional preprocessing stages such as:

- Dataset validation
- Feature engineering
- Statistical reports
- Image verification
- Data augmentation
- Automatic train/test dataset generation