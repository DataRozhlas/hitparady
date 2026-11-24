import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import os
    import marimo as mo
    import polars as pl
    import altair as alt

    return alt, os, pl


@app.cell
def _(pl):
    df = pl.read_csv(
        "data/CZ_SINGLES_DIGITAL_TOP_100_tydenni.csv"
    ).with_columns(
        pl.col(["track", "interpret"])
        .str.to_lowercase()
        .str.replace_many(["!"], [""])
    ).filter(
        pl.col('rok') >= 2021
    )
    return (df,)


@app.cell
def _(df):
    df
    return


@app.cell
def _(alt, df):
    alt.Chart(df.group_by("tyden").len()).mark_bar().encode(
        alt.X("tyden:Q"), alt.Y("len:Q")
    )
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.filter(pl.col("track").str.contains("(?i)christ"))
        .group_by("tyden")
        .len(),
        width=900,
    ).mark_bar().encode(alt.X("tyden:Q"), alt.Y("len:Q"))
    return


@app.cell
def _(df, pl):
    vanocni = (
        df.filter(pl.col("tyden").is_between(48, 52))
        .group_by(pl.col(["track", "interpret"]))
        .agg(pl.col("rok").unique().len())
        .filter(pl.col("rok") > 1)
        .with_columns(
            (pl.col("interpret") + pl.lit(": ") + pl.col("track")).alias(
                "pisen"
            )
        )
        .select(pl.col("pisen"))
        .unique()
        .to_series()
        .to_list()
    )

    vanocni[0:10]
    return (vanocni,)


@app.cell
def _(df, pl):
    nevanocni = (
        df.filter(pl.col("tyden").is_between(5, 45))
        .group_by(pl.col(["track", "interpret"]))
        .agg(pl.col("rok").unique().len())
        .with_columns(
            (pl.col("interpret") + pl.lit(": ") + pl.col("track")).alias(
                "pisen"
            )
        )
        .select(pl.col("pisen"))
        .unique()
        .to_series()
        .to_list()
    )

    nevanocni[0:10]
    return (nevanocni,)


@app.cell
def _(nevanocni, vanocni):
    ryze_vanocni = [x for x in vanocni if x not in nevanocni]
    ryze_vanocni
    return (ryze_vanocni,)


@app.cell
def _(df, os, pl, ryze_vanocni):
    zebricek = (
        df.with_columns(
            (pl.col("interpret") + pl.lit(": ") + pl.col("track")).alias(
                "pisen"
            )
        )
        .filter(pl.col("pisen").is_in(ryze_vanocni))
        .group_by("pisen")
        .len()
        .sort(by="len", descending=True)
        .rename({"len": "tydnu_ve_streamovacich_hitparadach"})
    )

    kam = "data/vanoce26/"

    os.makedirs(kam, exist_ok=True)

    zebricek.write_json(os.path.join(kam, "stream_hitparady.json"))

    zebricek
    return


if __name__ == "__main__":
    app.run()
