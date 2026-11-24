import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    from pathlib import Path
    import marimo as mo
    import polars as pl
    import altair as alt

    odkud="data/vanoce26"
    return Path, alt, odkud, os, pl


@app.cell
def _(Path, odkud, os, pl):
    def nacti_hitparadu(cesta: str | Path, format="json") -> pl.DataFrame:

        if format == "json":
            dfp = pl.read_json(os.path.join(cesta))
        else:
            if format == "parquet":
                dfp = pl.read_parquet(os.path.join(cesta))
            elif format == "csv":
                dfp = pl.read_csv(os.path.join(cesta))
            dfp = dfp.with_columns((pl.col("interpret") + pl.lit(": ") + pl.col("track")).str.to_lowercase().alias("pisen"))
    
        return dfp.with_columns(
                pl.col("pisen")
                .str.split("(")
                .list.slice(0, 1)
                .list.join("")
                .str.strip_chars()
            ).with_columns(
                pl.col("pisen")
                .str.to_lowercase()
                .str.replace_all(r"´", "'")
                .str.replace_all(r"\s+", " ")
                # Sjednocení oddělovačů interpretů (&, /, čárka) na ", "
                .str.replace_all(r"\s*(?:&|/|,)\s*", ", ")
                # Odstranění rozdílné interpunkce (apostrofy, vykřičníky, otazníky)
                .str.replace_all(r"['!?]", "")
                # Ad hoc sjednocení konkrétních odlišností u interpretů
                .str.replace_many(
                    [
                        "band aid ii.:",
                        "john lennon, yoko ono:",
                        "johny machette, teri blitzen:",
                    ],
                    [
                        "band aid:",
                        "john lennon:",
                        "johny machette:",
                    ],
                )
                .alias("klic")
            ).unique(subset="klic", keep="first", maintain_order=True)


    df = (
        nacti_hitparadu(os.path.join(odkud,"cro.json"))
        .join(
            nacti_hitparadu(os.path.join(odkud,"rozhlasove_hitparady.json")),
            on="klic",
            how="full",
            coalesce=True,
            suffix="_radio",
        )
        .join(
            nacti_hitparadu(os.path.join(odkud,"stream_hitparady.json")),
            on="klic",
            how="full",
            coalesce=True,
            suffix="_stream",
        )
        .drop("klic")
        .rename({"pisen": "pisen_cro"})
    )
    return df, nacti_hitparadu


@app.cell
def _(df, pl):
    porovnani = df.sort(by='pisen_cro').select(pl.col(["pisen_cro","pisen_radio","pisen_stream"]))
    porovnani
    return (porovnani,)


@app.cell
def _(pl, porovnani):
    vsechny_vanocni = porovnani.select(pl.col("pisen_cro")).unique().to_series().to_list() + porovnani.select(pl.col("pisen_radio")).unique().to_series().to_list() + porovnani.select(pl.col("pisen_stream")).unique().to_series().to_list()

    vsechny_vanocni = list(set(vsechny_vanocni))

    len(vsechny_vanocni)
    return (vsechny_vanocni,)


@app.cell
def _(pl, porovnani):
    porovnani.filter(
        pl.any_horizontal(
            pl.all().str.contains("půlnoční")
        )
    )
    return


@app.cell
def _(porovnani):
    porovnani.drop_nulls()
    return


@app.cell
def _(pl, porovnani):
    porovnani.filter(pl.col("pisen_cro").is_null()).drop("pisen_cro").drop_nulls()
    return


@app.cell
def _(pl, porovnani):
    porovnani.filter(pl.col("pisen_radio").is_null()).drop("pisen_radio").drop_nulls()
    return


@app.cell
def _(pl, porovnani):
    porovnani.filter(pl.col("pisen_stream").is_null()).drop("pisen_stream").drop_nulls()
    return


@app.cell
def _(pl, porovnani):
    porovnani.filter(pl.col("pisen_cro").is_null() & pl.col('pisen_radio').is_null())
    return


@app.cell
def _(nacti_hitparadu, os):
    df_rozhlas = nacti_hitparadu(os.path.join("data","cro_x.parquet"),format="parquet")
    return (df_rozhlas,)


@app.cell
def _(df_rozhlas, pl, vsechny_vanocni):
    df_rozhlas_v = df_rozhlas.filter(pl.col("pisen").is_in(vsechny_vanocni)).group_by(pl.col("since").dt.week()).len().rename({'since':'tyden','len':'rozhlas'})
    return (df_rozhlas_v,)


@app.cell
def _(nacti_hitparadu, os, pl):
    df_stream = nacti_hitparadu(os.path.join("data","CZ_SINGLES_DIGITAL_TOP_100_tydenni.csv"),format="csv").filter(pl.col("rok") >= 2016)
    return (df_stream,)


@app.cell
def _(df_stream, pl, vsechny_vanocni):
    df_stream_v = df_stream.filter(pl.col("pisen").is_in(vsechny_vanocni)).group_by(pl.col("tyden")).len().rename({'len':'stream'})
    return (df_stream_v,)


@app.cell
def _(nacti_hitparadu, os, pl):
    df_radio = nacti_hitparadu(os.path.join("data","CZ_RADIO_TOP_100_tydenni.csv"),format="csv").filter(pl.col("rok") >= 2016)
    return (df_radio,)


@app.cell
def _(df_radio, pl, vsechny_vanocni):
    df_radio_v = df_radio.filter(pl.col("pisen").is_in(vsechny_vanocni)).group_by(pl.col("tyden")).len().rename({'len':'radio'})
    return (df_radio_v,)


@app.cell
def _():
    tydny = [{'tyden':x} for x in range(0,53)]
    return (tydny,)


@app.cell
def _(df_radio_v, df_rozhlas_v, df_stream_v, pl, tydny):
    porovnani_radio_stream = pl.DataFrame(tydny).join(df_radio_v,on='tyden',how='left').join(
        df_stream_v,how="full",on="tyden"
    ).drop("tyden_right").join(df_rozhlas_v, on="tyden", how="left").unpivot(index="tyden",on=["radio","stream",'rozhlas'])

    porovnani_radio_stream.tail(10)
    return (porovnani_radio_stream,)


@app.cell
def _(alt, porovnani_radio_stream):
    alt.Chart(
        porovnani_radio_stream, width=600, height=200
    ).mark_bar().encode(alt.X("tyden:Q"),alt.Y("value:Q"),alt.Color("variable:N"))
    return


if __name__ == "__main__":
    app.run()
