import pandas as pd


EVSE_CAT = {
    "PCN": [
        'Slow AC recharging point, single-phase (P < 7.4kW)',
        'Medium-speed AC recharging point, triple-phase (7.4kW ≤ P ≤ 22kW)'
    ],
    "PCR": [
        'Fast AC recharging point, triple-phase (P > 22kW)',
        'Slow DC recharging point (P < 50kW)',
        'Fast DC recharging point (50kW ≤ P <150kW)',
    ],
    "PCR": [
        'Fast AC recharging point, triple-phase (P > 22kW)',
        'Slow DC recharging point (P < 50kW)',
        'Fast DC recharging point (50kW ≤ P <150kW)',
    ],
    "PCUR": [
        'Level 1 - Ultra-fast DC recharging point (150kW ≤ P < 350kW)',
        'Level 2 - Ultra-fast DC recharging point (P ≥ 350kW)',
    ]
}


def load_fleet():
    df = pd.concat(
        [
            (
                pd.read_csv("notebooks/europe_comparison/rawdata/2021-afo-contry_comparison-fleet.csv")
                .assign(year=lambda _: 2021)
            ),
            (
                pd.read_csv("notebooks/europe_comparison/rawdata/2022-afo-contry_comparison-fleet.csv")
                .assign(year=lambda _: 2022)
            ),
        ],
        ignore_index=True
    )
    df = df.drop(columns=["H2", "LPG", "CNG", "LNG"])
    df = df.rename(
        columns={
            "Category": "Country"
        }
    )
    return df


def load_evses():
    df = pd.concat(
        [
            (
                pd.read_csv("notebooks/europe_comparison/rawdata/2021-afo-contry_comparison-evses.csv")
                .assign(year=lambda _: 2021)
            ),
            (
                pd.read_csv("notebooks/europe_comparison/rawdata/2022-afo-contry_comparison-evses.csv")
                .assign(year=lambda _: 2022)
            ),
        ],
        ignore_index=True
    )
    df = df.rename(
        columns={
            "Category": "Country"
        }
    )
    return df


def load_joined_fleet_evses():
    df_fleet = load_fleet()
    df_evses = load_evses()

    df = df_fleet.merge(df_evses, on=["year", "Country"], how="outer")

    return df


def load():
    
    df = load_joined_fleet_evses()

    df["EVS"] = df["BEV"] + df["PHEV"]

    for cat, cols in EVSE_CAT.items():
        df[cat] = df[cols].sum(axis=1)
        df = df.drop(columns=cols)

    return df


if __name__ == "__main__":
    pass
