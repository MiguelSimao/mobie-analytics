import pandas as pd


def load_tariffs_ceme() -> pd.DataFrame:

    input_path = "data/ceme_plans.csv"

    df = pd.read_csv(
        input_path,
        parse_dates=["Data atualização", "Data Tarifário", "Data Fim Tarifário"],
    )
    df = (
        df
        .reset_index()
        .dropna(subset=["CEME | CONTRATO"])
        .astype({
            "Inclui EGME": "bool",
            "Inclui IEC": "bool",
            "Inclui TAR": "bool",
        })
        .assign(
            **{
                "Ponta": lambda _: _["Ponta"].where(_["Inclui TAR"], _["Ponta.1"]),
                "Cheias / Fora de Vazio": lambda _: _["Cheias / Fora de Vazio"].where(_["Inclui TAR"], _["Cheias / Fora de Vazio.1"]),
                "Vazio": lambda _: _["Vazio"].where(_["Inclui TAR"], _["Vazio.1"]),
            }
        )
    )
    df = df[[
        "index",
        "CEME | CONTRATO",
        "Condicionantes",
        "URL",
        "Data atualização", 
        "Data Tarifário", 
        "Data Fim Tarifário",
        "Tarifa",
        "Inclui EGME",
        "Inclui IEC",
        "Inclui TAR",
        "Ativacao",
        "Ponta",
        "Cheias / Fora de Vazio",
        "Vazio",
    ]]
    df = df.rename(
        columns={
            "index": "idx_ceme",
            "CEME | CONTRATO": "ceme_name", 
            "Condicionantes": "ceme_constraints", 
            "URL": "url", 
            "Data atualização": "date_updated", 
            "Data Tarifário": "date_tariff_start", 
            "Data Fim Tarifário": "date_tariff_end", 
            "Tarifa": "tariff_cycle", 
            "Inclui EGME": "includes_egme", 
            "Inclui IEC": "includes_iec", 
            "Inclui TAR": "includes_tar", 
            "Ativacao": "fee_activation", 
            "Ponta": "fee_peak", 
            "Cheias / Fora de Vazio": "fee_offpeak", 
            "Vazio": "fee_empty", 
        }
    )
    return df


def load_erse_tar(latest: bool = True):

    path_input = "data/erse_tar.csv"

    df = (
        pd
        .read_csv(
            path_input,
            parse_dates=["Calendário"],
            usecols=["Calendário", "Tensão", "Tarifa", "Ponta", "Cheias/Não Vazio", "Vazio"]
        )
        .rename(columns={
            "Calendário": "date_starts", 
            "Tensão": "voltage_level", 
            "Tarifa": "tariff_cycle", 
            "Ponta": "tar_peak", 
            "Cheias/Não Vazio": "tar_offpeak", 
            "Vazio": "tar_empty", 
        })
        .assign(
            year=lambda _: pd.to_numeric(_.date_starts.str[:4]),
            month=lambda _: pd.to_numeric(_.date_starts.str[4:]).fillna(1),
            day=lambda _: 1,
            date_starts=lambda _: pd.to_datetime(_[["year", "month", "day"]])
        )
        .drop(columns=["year", "month", "day"])
    )
    if latest:
        df = df.loc[df.date_starts == df.date_starts.max()]
    return df


def load_tax_iec(latest: bool = True):

    path_input = "data/erse_iec.csv"
    
    df = (
        pd
        .read_csv(
            path_input,
            parse_dates=["Ano"],
        )
        .rename(columns={
            "Ano": "date_starts", 
            "IEC (€/kWh)": "tax_iec_kwh", 
        })
    )
    if latest:
        df = df.loc[df.date_starts == df.date_starts.max()]
    return df


def load_fees_egme():

    path_input = "data/erse_egme.csv"

    df = (
        pd
        .read_csv(
            path_input,
            parse_dates=["Calendário"],
            usecols=["Calendário", "CEME", "OPC", "Apoio CEME"],
        )
        .rename(columns={
            "Calendário": "date_starts",
            "CEME": "fee_egme_ceme",
            "OPC": "fee_egme_opc",
            "Apoio CEME": "fee_egme_ceme_discount"
        })
    )
    return df


def load_and_join_tariffs():

    df_ceme = load_tariffs_ceme()
    df_tar = load_erse_tar()
    df_iec = load_tax_iec()

