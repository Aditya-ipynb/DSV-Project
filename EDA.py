# ============================================================
# EXPERIMENT 2: EXPLORATORY DATA ANALYSIS - POKEMON DATASET
# ============================================================

import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# STEP 1: CONFIGURE DATASET PATH
# ============================================================

DATASET_PATH = (
    Path("image_organization")
    / "pokemon_cleaned_images.json"
)


# ============================================================
# STEP 2: LOAD DATASET
# ============================================================

if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found at: {DATASET_PATH.resolve()}"
    )

with open(DATASET_PATH, "r", encoding="utf-8") as file:
    raw_data = json.load(file)


# ------------------------------------------------------------
# Support the expected list-based JSON structure
# ------------------------------------------------------------

if isinstance(raw_data, list):

    pokemon_records = raw_data

elif isinstance(raw_data, dict):

    # Fallback support in case the JSON structure changes
    if "Pokemon" in raw_data:

        pokemon_data = raw_data["Pokemon"]

        if isinstance(pokemon_data, dict):
            pokemon_records = list(pokemon_data.values())

        elif isinstance(pokemon_data, list):
            pokemon_records = pokemon_data

        else:
            raise TypeError(
                "Unsupported structure inside the 'Pokemon' key."
            )

    else:

        pokemon_records = list(raw_data.values())

else:

    raise TypeError(
        f"Unsupported JSON root type: "
        f"{type(raw_data).__name__}"
    )


# ------------------------------------------------------------
# Flatten nested JSON
#
# Example:
# stats.hp             -> stats_hp
# stats.attack         -> stats_attack
# stats.bst            -> stats_bst
# ------------------------------------------------------------

df = pd.json_normalize(
    pokemon_records,
    sep="_"
)


print("\n" + "=" * 70)
print("DATASET LOADED SUCCESSFULLY")
print("=" * 70)

print(f"Total records    : {len(df)}")
print(f"Total attributes : {len(df.columns)}")


# ============================================================
# STEP 3: DISPLAY FIRST AND LAST FIVE RECORDS
# ============================================================

print("\n" + "=" * 70)
print("FIRST FIVE RECORDS")
print("=" * 70)

print(df.head())


print("\n" + "=" * 70)
print("LAST FIVE RECORDS")
print("=" * 70)

print(df.tail())


# ============================================================
# STEP 4: CHECK DATASET SHAPE
# ============================================================

print("\n" + "=" * 70)
print("DATASET SHAPE")
print("=" * 70)

print("Rows   :", df.shape[0])
print("Columns:", df.shape[1])


# ============================================================
# STEP 5: DATASET INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("DATASET INFORMATION")
print("=" * 70)

df.info()


# ============================================================
# STEP 6: CHECK DATA TYPES
# ============================================================

print("\n" + "=" * 70)
print("DATA TYPES")
print("=" * 70)

print(df.dtypes)


# ============================================================
# STEP 7: STATISTICAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("NUMERICAL STATISTICAL SUMMARY")
print("=" * 70)

print(
    df.describe(
        include=[np.number]
    ).round(2)
)


# ------------------------------------------------------------
# Categorical summary
#
# We explicitly select object/string columns because newer
# Pandas versions handle string dtype differently.
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("CATEGORICAL STATISTICAL SUMMARY")
print("=" * 70)

categorical_df = df.select_dtypes(
    include=["object", "string", "str"]
)

print(categorical_df.describe())


# ============================================================
# STEP 8: CHECK MISSING VALUES
# ============================================================

print("\n" + "=" * 70)
print("MISSING VALUE REPORT")
print("=" * 70)

missing_values = df.isnull().sum()

missing_report = pd.DataFrame({
    "Missing Values": missing_values,
    "Percentage": (
        missing_values / len(df) * 100
    ).round(2)
})

missing_report = missing_report[
    missing_report["Missing Values"] > 0
].sort_values(
    by="Missing Values",
    ascending=False
)

if missing_report.empty:

    print("No missing values found.")

else:

    print(missing_report)


# ============================================================
# STEP 9: CHECK DUPLICATE RECORDS
# ============================================================

print("\n" + "=" * 70)
print("DUPLICATE RECORD REPORT")
print("=" * 70)


# ------------------------------------------------------------
# 'abilities' contains Python lists.
#
# Lists are unhashable, therefore df.duplicated() cannot
# directly process the column.
#
# Convert lists into tuples temporarily.
# ------------------------------------------------------------

duplicate_df = df.copy()

duplicate_df["abilities"] = (
    duplicate_df["abilities"]
    .apply(
        lambda value:
        tuple(value)
        if isinstance(value, list)
        else value
    )
)


# Exact duplicate records

duplicate_count = (
    duplicate_df
    .duplicated()
    .sum()
)

print(
    "Exact duplicate records:",
    duplicate_count
)


# ------------------------------------------------------------
# Duplicate Pokémon identities
#
# Multiple forms may legitimately share the same dex_number,
# so dex_number alone must NOT be used to detect duplicates.
# ------------------------------------------------------------

identity_duplicate_count = (
    duplicate_df
    .duplicated(
        subset=[
            "dex_number",
            "species",
            "variant"
        ]
    )
    .sum()
)

print(
    "Duplicate Pokémon identities:",
    identity_duplicate_count
)


# ============================================================
# STEP 10: UNIQUE CATEGORICAL VALUES
# ============================================================

print("\n" + "=" * 70)
print("UNIQUE VALUES IN IMPORTANT CATEGORICAL COLUMNS")
print("=" * 70)


categorical_columns = [
    "type",
    "secondary_type",
    "hidden_ability",
    "variant"
]


for column in categorical_columns:

    print("\n" + "-" * 50)
    print(column.upper())
    print("-" * 50)

    print(
        "Unique values:",
        df[column].nunique(
            dropna=True
        )
    )

    print(
        df[column]
        .value_counts(
            dropna=False
        )
    )


# ------------------------------------------------------------
# Abilities require special treatment because each record
# contains a list of abilities.
# ------------------------------------------------------------

all_abilities = (
    df["abilities"]
    .explode()
    .dropna()
)

print("\n" + "-" * 50)
print("ABILITIES")
print("-" * 50)

print(
    "Unique abilities:",
    all_abilities.nunique()
)

print(
    all_abilities.value_counts()
)


# ============================================================
# STEP 11: UNIVARIATE ANALYSIS
# ============================================================


# ------------------------------------------------------------
# 11A: Distribution of Base Stat Total
# ------------------------------------------------------------

plt.figure(
    figsize=(9, 5)
)

sns.histplot(
    data=df,
    x="stats_bst",
    bins=30,
    kde=True
)

plt.title(
    "Distribution of Pokémon Base Stat Total (BST)"
)

plt.xlabel(
    "Base Stat Total"
)

plt.ylabel(
    "Frequency"
)

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 11B: Pokémon Count by Primary Type
# ------------------------------------------------------------

type_counts = (
    df["type"]
    .value_counts()
)

plt.figure(
    figsize=(11, 6)
)

sns.barplot(
    x=type_counts.index,
    y=type_counts.values
)

plt.title(
    "Number of Pokémon by Primary Type"
)

plt.xlabel(
    "Primary Type"
)

plt.ylabel(
    "Number of Records"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 11C: Box Plot of BST
# ------------------------------------------------------------

plt.figure(
    figsize=(9, 5)
)

sns.boxplot(
    data=df,
    x="stats_bst"
)

plt.title(
    "Box Plot of Base Stat Total"
)

plt.xlabel(
    "BST"
)

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 11D: Primary Type Distribution Pie Chart
# ------------------------------------------------------------

plt.figure(
    figsize=(10, 10)
)

type_counts.plot(
    kind="pie",
    autopct="%1.1f%%",
    startangle=90
)

plt.title(
    "Primary Type Distribution"
)

plt.ylabel("")

plt.tight_layout()
plt.show()


# ============================================================
# STEP 12: BIVARIATE ANALYSIS
# ============================================================


# ------------------------------------------------------------
# 12A: Attack vs Defense
# ------------------------------------------------------------

plt.figure(
    figsize=(11, 7)
)

sns.scatterplot(
    data=df,
    x="stats_attack",
    y="stats_defense",
    hue="type",
    alpha=0.7
)

plt.title(
    "Attack vs Defense by Primary Type"
)

plt.xlabel(
    "Attack"
)

plt.ylabel(
    "Defense"
)

plt.legend(
    title="Primary Type",
    bbox_to_anchor=(1.05, 1),
    loc="upper left"
)

plt.tight_layout()
plt.show()


# ------------------------------------------------------------
# 12B: Average BST by Primary Type
# ------------------------------------------------------------

avg_bst_by_type = (
    df
    .groupby("type")["stats_bst"]
    .mean()
    .sort_values(
        ascending=False
    )
)


print("\n" + "=" * 70)
print("AVERAGE BST BY PRIMARY TYPE")
print("=" * 70)

print(
    avg_bst_by_type.round(2)
)


plt.figure(
    figsize=(11, 6)
)

sns.barplot(
    x=avg_bst_by_type.index,
    y=avg_bst_by_type.values
)

plt.title(
    "Average BST by Primary Type"
)

plt.xlabel(
    "Primary Type"
)

plt.ylabel(
    "Average BST"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()
plt.show()


# ============================================================
# STEP 13: CORRELATION MATRIX AND HEATMAP
# ============================================================

battle_stats = [
    "stats_hp",
    "stats_attack",
    "stats_defense",
    "stats_special_attack",
    "stats_special_defense",
    "stats_speed",
    "stats_bst"
]


correlation_matrix = (
    df[battle_stats]
    .corr()
)


print("\n" + "=" * 70)
print("CORRELATION MATRIX")
print("=" * 70)

print(
    correlation_matrix.round(2)
)


plt.figure(
    figsize=(10, 8)
)

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    square=True,
    linewidths=0.5
)

plt.title(
    "Correlation Heatmap of Pokémon Battle Statistics"
)

plt.tight_layout()
plt.show()


# ============================================================
# ADDITIONAL USEFUL EDA
# ============================================================


# ------------------------------------------------------------
# Distribution of Individual Battle Statistics
# ------------------------------------------------------------

stats_for_plot = [
    "stats_hp",
    "stats_attack",
    "stats_defense",
    "stats_special_attack",
    "stats_special_defense",
    "stats_speed"
]


# Rename only for cleaner graph labels.
stats_plot_df = df[
    stats_for_plot
].rename(
    columns={
        "stats_hp": "HP",
        "stats_attack": "Attack",
        "stats_defense": "Defense",
        "stats_special_attack": "Sp. Attack",
        "stats_special_defense": "Sp. Defense",
        "stats_speed": "Speed"
    }
)


plt.figure(
    figsize=(11, 6)
)

sns.boxplot(
    data=stats_plot_df
)

plt.title(
    "Distribution of Pokémon Battle Statistics"
)

plt.xlabel(
    "Battle Statistic"
)

plt.ylabel(
    "Base Stat Value"
)

plt.xticks(
    rotation=25
)

plt.tight_layout()
plt.show()


# ============================================================
# STEP 14: USEFUL SUMMARY TABLES AND OBSERVATIONS
# ============================================================


# ------------------------------------------------------------
# Top 10 Pokémon / Forms by BST
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TOP 10 POKÉMON / FORMS BY BST")
print("=" * 70)


top_bst = (
    df[
        [
            "dex_number",
            "species",
            "variant",
            "type",
            "secondary_type",
            "stats_bst"
        ]
    ]
    .sort_values(
        by="stats_bst",
        ascending=False
    )
    .head(10)
)

print(
    top_bst.to_string(
        index=False
    )
)


# ------------------------------------------------------------
# Lowest 10 Pokémon / Forms by BST
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("LOWEST 10 POKÉMON / FORMS BY BST")
print("=" * 70)


lowest_bst = (
    df[
        [
            "dex_number",
            "species",
            "variant",
            "type",
            "secondary_type",
            "stats_bst"
        ]
    ]
    .sort_values(
        by="stats_bst",
        ascending=True
    )
    .head(10)
)

print(
    lowest_bst.to_string(
        index=False
    )
)


# ------------------------------------------------------------
# Average Battle Statistics by Primary Type
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("AVERAGE BATTLE STATS BY PRIMARY TYPE")
print("=" * 70)


type_stat_summary = (
    df
    .groupby("type")[battle_stats]
    .mean()
    .round(2)
    .sort_values(
        by="stats_bst",
        ascending=False
    )
)

print(type_stat_summary)


# ============================================================
# ADDITIONAL DATA QUALITY ANALYSIS
# ============================================================


# ------------------------------------------------------------
# Base Pokémon vs Variant Records
# ------------------------------------------------------------

base_count = (
    df["variant"]
    .isna()
    .sum()
)

variant_count = (
    df["variant"]
    .notna()
    .sum()
)


print("\n" + "=" * 70)
print("BASE SPECIES / VARIANT DISTRIBUTION")
print("=" * 70)

print(
    "Base Pokémon records :",
    base_count
)

print(
    "Variant records      :",
    variant_count
)


# ------------------------------------------------------------
# Image Mapping Status
# ------------------------------------------------------------

mapped_images = (
    df["image"]
    .notna()
    .sum()
)

missing_images = (
    df["image"]
    .isna()
    .sum()
)


print("\n" + "=" * 70)
print("IMAGE MAPPING STATUS")
print("=" * 70)

print(
    "Mapped images  :",
    mapped_images
)

print(
    "Missing images :",
    missing_images
)

print(
    "Image coverage :",
    f"{(mapped_images / len(df)) * 100:.2f}%"
)


# ------------------------------------------------------------
# Records with Missing Images
# ------------------------------------------------------------

if missing_images > 0:

    missing_image_records = df.loc[
        df["image"].isna(),
        [
            "dex_number",
            "species",
            "variant"
        ]
    ]

    print(
        "\nFirst 20 records with missing images:"
    )

    print(
        missing_image_records
        .head(20)
        .to_string(index=False)
    )


# ============================================================
# STEP 15: FINAL DATASET SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("EDA SUMMARY")
print("=" * 70)


print(
    "Total records:",
    len(df)
)

print(
    "Total flattened attributes:",
    len(df.columns)
)

print(
    "Exact duplicate records:",
    duplicate_count
)

print(
    "Duplicate Pokémon identities:",
    identity_duplicate_count
)

print(
    "Unique Pokédex numbers:",
    df["dex_number"].nunique()
)

print(
    "Unique species:",
    df["species"].nunique()
)

print(
    "Primary types:",
    df["type"].nunique()
)

print(
    "Secondary types:",
    df["secondary_type"].nunique(
        dropna=True
    )
)

print(
    "Base Pokémon records:",
    base_count
)

print(
    "Variant records:",
    variant_count
)

print(
    "Unique abilities:",
    all_abilities.nunique()
)

print(
    "Average BST:",
    round(
        df["stats_bst"].mean(),
        2
    )
)

print(
    "Median BST:",
    round(
        df["stats_bst"].median(),
        2
    )
)

print(
    "Standard Deviation of BST:",
    round(
        df["stats_bst"].std(),
        2
    )
)

print(
    "Maximum BST:",
    df["stats_bst"].max()
)

print(
    "Minimum BST:",
    df["stats_bst"].min()
)

print(
    "Images mapped:",
    mapped_images
)

print(
    "Images missing:",
    missing_images
)

print(
    "Image coverage:",
    f"{(mapped_images / len(df)) * 100:.2f}%"
)


# ============================================================
# IDENTIFY EXTREME BST RECORDS
# ============================================================

print("\n" + "=" * 70)
print("POKÉMON WITH MAXIMUM BST")
print("=" * 70)

max_bst = df["stats_bst"].max()

max_bst_records = df.loc[
    df["stats_bst"] == max_bst,
    [
        "dex_number",
        "species",
        "variant",
        "type",
        "secondary_type",
        "stats_bst"
    ]
]

print(
    max_bst_records.to_string(
        index=False
    )
)


print("\n" + "=" * 70)
print("POKÉMON WITH MINIMUM BST")
print("=" * 70)

min_bst = df["stats_bst"].min()

min_bst_records = df.loc[
    df["stats_bst"] == min_bst,
    [
        "dex_number",
        "species",
        "variant",
        "type",
        "secondary_type",
        "stats_bst"
    ]
]

print(
    min_bst_records.to_string(
        index=False
    )
)


# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("EXPLORATORY DATA ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 70)