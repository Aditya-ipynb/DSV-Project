"""
============================================================

CPI_izer Pipeline

Cleaning
Preprocessing
Image
-izer

============================================================
"""

import subprocess
import sys
import time
from pathlib import Path
from dataclasses import dataclass

# ==========================================================
# PROJECT ROOT
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

# ==========================================================
# STAGE CLASS
# ==========================================================

@dataclass
class Stage:
    name: str
    script: Path

# ==========================================================
# PIPELINE
# ==========================================================

PIPELINE = [

    Stage(
        "Cleaning Dataset",
        PROJECT_ROOT / "cleaning" / "cleaner.py"
    ),

    Stage(
        "Generating Variant Database",
        PROJECT_ROOT / "preprocessing" / "generate_variants.py"
    ),

    Stage(
        "Updating Pokémon Variants",
        PROJECT_ROOT / "preprocessing" / "update_variants.py"
    ),

    Stage(
        "Organizing Images",
        PROJECT_ROOT / "image_organization" / "image_organizer.py"
    ),

    Stage(
        "Mapping Images",
        PROJECT_ROOT / "image_organization" / "image_mapper.py"
    )

]

# ==========================================================
# RUN STAGE
# ==========================================================

def run_stage(stage: Stage):

    print("\n")
    print("=" * 70)
    print(stage.name)
    print("=" * 70)

    if not stage.script.exists():
        raise FileNotFoundError(stage.script)

    start = time.perf_counter()

    result = subprocess.run(
        [sys.executable, str(stage.script)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )

    runtime = time.perf_counter() - start

    if result.returncode != 0:

        print(result.stdout)
        print(result.stderr)

        raise RuntimeError(
            f"\nPipeline stopped at '{stage.name}'."
        )

    if result.stdout.strip():
        print(result.stdout)

    print(f"Completed in {runtime:.2f} sec")

# ==========================================================
# MAIN
# ==========================================================

def main():

    total_start = time.perf_counter()

    print("=" * 70)
    print("CPIizer")
    print("Cleaning • Preprocessing • Image-izer")
    print("=" * 70)

    for stage in PIPELINE:
        run_stage(stage)

    total_runtime = time.perf_counter() - total_start

    print("\n")
    print("=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 70)
    print(f"Total Runtime : {total_runtime:.2f} sec")
    print("=" * 70)

if __name__ == "__main__":
    main()