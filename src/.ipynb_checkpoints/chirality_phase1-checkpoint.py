"""
Phase 1: Bennu vs Earth chirality "answer key"

- Builds a dummy Bennu + Earth amino-acid table.
- Handles chiral vs achiral (e.g., glycine) cleanly.
- Provides a grouped bar plot comparing L/D fractions
  for each molecule across environments.

You can later swap the dummy blocks for real CSV/Excel loads
from the Bennu Nature / PDS supplements.
"""

import pandas as pd
import matplotlib.pyplot as plt


def build_dummy_tables() -> pd.DataFrame:
    """
    Construct a combined Bennu + Earth chirality table.

    Columns:
        molecule (str)
        L_fraction (float or NaN)
        D_fraction (float or NaN)
        total_abundance_ppb (float or <NA>)
        notes (str)
        environment ({"Bennu", "Earth"})
    """

    # ------------------------
    # Bennu: dummy meteoritic data
    # ------------------------
    bennu_rows = [
        # molecule,   L_fraction, D_fraction, total_abundance_ppb, notes
        ("Alanine",   0.49,       0.51,       35.0,
         "near-racemic; chiral"),

        ("β-Alanine", 0.52,       0.48,       15.0,
         "near-racemic; chiral"),

        ("Isovaline", 0.50,       0.50,        8.0,
         "classic meteoritic amino acid; chiral"),

        # Glycine is achiral → no L/D fractions; abundance only
        ("Glycine",   None,       None,      120.0,
         "achiral; abundance-only in this toy table"),
    ]

    bennu_cols = [
        "molecule",
        "L_fraction",
        "D_fraction",
        "total_abundance_ppb",
        "notes",
    ]

    df_bennu = pd.DataFrame(bennu_rows, columns=bennu_cols)
    df_bennu["environment"] = "Bennu"

    # ------------------------
    # Earth: dummy biological control
    # ------------------------
    earth_rows = [
        # molecule,   L_fraction, D_fraction, notes
        ("Alanine",   1.00,       0.00,
         "proteinogenic; homochiral L in biology"),

        ("β-Alanine", 1.00,       0.00,
         "treated as 'all L' control here"),

        ("Isovaline", 1.00,       0.00,
         "hypothetical Earth-life use case; all L"),

        # Glycine again is achiral, no L/D split
        ("Glycine",   None,       None,
         "achiral; abundance-only control"),
    ]

    df_earth = pd.DataFrame(
        earth_rows,
        columns=["molecule", "L_fraction", "D_fraction", "notes"],
    )
    df_earth["environment"] = "Earth"

    # Earth control table doesn't need a real abundance here
    df_earth["total_abundance_ppb"] = pd.NA

    # ------------------------
    # Combine
    # ------------------------
    df_all = pd.concat([df_bennu, df_earth], ignore_index=True)

    # Enforce column ordering
    df_all = df_all[
        [
            "molecule",
            "environment",
            "L_fraction",
            "D_fraction",
            "total_abundance_ppb",
            "notes",
        ]
    ]

    return df_all


def plot_chirality_grouped(df: pd.DataFrame, molecule_name: str) -> None:
    """
    Grouped bar plot of L vs D fractions for a given molecule
    across environments (Bennu vs Earth).

    Skips molecules with no chirality data (e.g., Glycine).
    """

    # Require both L and D to be non-null for plotting
    subset = df[
        (df["molecule"] == molecule_name)
        & df["L_fraction"].notna()
        & df["D_fraction"].notna()
    ].copy()

    if subset.empty:
        print(f"[skip] {molecule_name}: no chirality data to plot.")
        return

    melted = subset.melt(
        id_vars=["environment"],
        value_vars=["L_fraction", "D_fraction"],
        var_name="handedness",
        value_name="fraction",
    )

    envs = list(melted["environment"].unique())
    width = 0.35
    x = range(len(envs))

    fig, ax = plt.subplots(figsize=(6, 4))

    for i, hand in enumerate(["L_fraction", "D_fraction"]):
        vals = [
            melted[
                (melted["environment"] == env)
                & (melted["handedness"] == hand)
            ]["fraction"].iloc[0]
            for env in envs
        ]
        offset = (i - 0.5) * width
        labels = hand.replace("_fraction", "")  # "L" or "D"
        ax.bar(
            [xi + offset for xi in x],
            vals,
            width,
            label=labels,
        )

    ax.set_xticks(list(x))
    ax.set_xticklabels(envs)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Fraction")
    ax.set_title(f"Chirality comparison: {molecule_name}")
    ax.legend()
    plt.tight_layout()
    plt.show()


def main() -> None:
    """
    Convenience entry point: build the tables and plot all molecules.
    """

    df_all = build_dummy_tables()

    print("\nCombined Bennu + Earth chirality table:\n")
    print(df_all.to_string(index=False))

    print("\nGenerating chirality plots for each molecule...\n")
    for mol in df_all["molecule"].unique():
        plot_chirality_grouped(df_all, mol)


if __name__ == "__main__":
    main()
