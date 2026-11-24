import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl
    import altair as alt

    return alt, mo, pl


@app.cell
def _(pl):
    df = (
        pl.read_parquet("data/cro_x.parquet")
        .rename({"since": "timestamp"})
        .filter(
            pl.col("stanice").is_in(
                ["radiozurnal", "pohoda", "wave", "dvojka", "vltava"]
            )
        )
        .filter(pl.col("timestamp").dt.year().is_between(2021, 2025))
        .with_columns(
            pl.col("interpret").str.to_lowercase(),
            pl.col("track").str.to_lowercase(),
        )
        .with_columns(
            pl.col("interpret")
            .str.replace(",  ", ", ")
            .str.replace(" & ", ", ")
            .str.replace("!", "")
            .str.replace("/", ", ")
        )
        .with_columns(
            (pl.col("interpret") + pl.lit(": ") + pl.col("track")).alias(
                "pisen"
            )
        )
    )
    return (df,)


@app.cell
def _(df, pl):
    df.select(pl.col('timestamp').min())
    return


@app.cell
def _(df, pl):
    df.select(pl.col('timestamp').max())
    return


@app.cell
def _(df):
    df.sample(10)
    return


@app.cell
def _(df, pl):
    stanice_po_letech = (
        df.group_by([pl.col("stanice"), pl.col("timestamp").dt.year()])
        .len()
        .sort(by="timestamp")
    )

    stanice_po_letech
    return


@app.cell
def _(alt, df, pl):
    alt.Chart(
        df.group_by([pl.col("stanice"), pl.col("timestamp").dt.year()]).len(),
        width=700,
        heigh=50,
    ).mark_line().encode(
        alt.X("timestamp:Q"), alt.Y("len:Q"), alt.Color("stanice:N")
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Ryze vánoční
    """)
    return


@app.cell
def _(df, pl):
    hraje_od_unora_do_rijna = (
        df.filter(pl.col("timestamp").dt.month().is_between(2, 10))
        .select(pl.col("track_id"))
        .unique()
        .to_series()
        .to_list()
    )
    return (hraje_od_unora_do_rijna,)


@app.cell
def _(df, pl):
    hraje_v_prosinci = (
        df.filter(pl.col("timestamp").dt.month() == 12)
        .select(pl.col("track_id"))
        .unique()
        .to_series()
        .to_list()
    )
    return (hraje_v_prosinci,)


@app.cell
def _(hraje_od_unora_do_rijna, hraje_v_prosinci):
    hraje_hlavne_v_prosinci = [
        x for x in hraje_v_prosinci if x not in hraje_od_unora_do_rijna
    ]
    return (hraje_hlavne_v_prosinci,)


@app.cell
def _(df, hraje_hlavne_v_prosinci, pl):
    df.filter(pl.col("track_id").is_in(hraje_hlavne_v_prosinci)).group_by(
        ["interpret", "track"]
    ).len().sort(by="len", descending=True)
    return


@app.cell
def _(df, hraje_hlavne_v_prosinci, pl):
    po_tydnech = (
        df.filter(pl.col("track_id").is_in(hraje_hlavne_v_prosinci))
        .group_by(pl.col("timestamp").dt.week())
        .len()
        .sort(by="timestamp")
    )

    # 1. Create a DataFrame with all weeks from 1 to 52 (matching the i8 dtype)
    vsechny_tydny = pl.DataFrame(
        {"timestamp": pl.int_range(1, 53, dtype=pl.Int8, eager=True)}
    )

    # 2. Left join your grouped results onto the full list of weeks and fill nulls with 0
    po_tydnech = vsechny_tydny.join(
        po_tydnech, on="timestamp", how="left"
    ).with_columns(pl.col("len").fill_null(0))

    po_tydnech

    po_tydnech
    return po_tydnech, vsechny_tydny


@app.cell
def _(alt, po_tydnech):
    alt.Chart(po_tydnech).mark_bar().encode(
        alt.X("timestamp:N"), alt.Y("len:Q")
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Vánoční-ish
    """)
    return


@app.cell
def _(df, pl):
    nazvy = df.select(
        pl.col("pisen", "track_id", "interpret", "track")
    ).unique(subset="track_id")
    return (nazvy,)


@app.cell
def _(df, nazvy, pl):
    pomer_prosinec_neprosinec = (
        (
            df.filter(pl.col("timestamp").dt.month() == 12)
            .group_by("pisen")
            .len()
            .rename({"len": "prosinec"})
            .join(
                df.filter(pl.col("timestamp").dt.month().is_between(2, 10))
                .group_by("pisen")
                .len()
                .rename({"len": "unor-rijen"}),
                how="left",
                on="pisen",
            )
            .with_columns(
                (pl.col("prosinec") / pl.col("unor-rijen")).alias("r")
            )
            .join(nazvy, how="left", on="pisen")
        )
        .join(
            df.group_by("pisen").agg(pl.col("stanice").unique().len()),
            how="left",
            on="pisen",
        )
        .join(
            df.group_by("pisen")
            .agg(pl.col("timestamp").dt.year().unique().len())
            .rename({"timestamp": "roky"}),
            how="left",
            on="pisen",
        )
    )
    return (pomer_prosinec_neprosinec,)


@app.cell
def _(pl, pomer_prosinec_neprosinec):
    pomer_prosinec_neprosinec.filter(
        pl.col("prosinec") >= pl.col("roky")
    ).filter(pl.col("unor-rijen").is_null()).filter(
        pl.col("stanice") >= 2
    ).sort(by="roky", descending=True)
    return


@app.cell
def _(pl, pomer_prosinec_neprosinec):
    vyber = (
        pomer_prosinec_neprosinec.filter(pl.col("prosinec") >= 10)
        .filter(pl.col("stanice") >= 2)
        .filter((pl.col("r") > 1) | (pl.col("r").is_null()))
        .filter(pl.col("roky") >= 3)
        .sort(by="prosinec", descending=True)
    )

    vyber
    return (vyber,)


@app.cell
def _():
    import os

    return (os,)


@app.cell
def _(os, pl, vyber):
    kam = "data/vanoce26"

    vyber.rename(
        {
            "prosinec": "prehrani_v_prosinci_v_cro",
            "unor-rijen": "prehrani_v_unoru_az_rijnu_v_rcro",
            "r": "r_cro",
        }
    ).select(
        pl.col(
            [
                "pisen",
                "prehrani_v_prosinci_v_cro",
                "prehrani_v_unoru_az_rijnu_v_rcro",
                "r_cro",
            ]
        )
    ).write_json(os.path.join(kam, "cro.json"))
    return


@app.cell
def _(pl, vyber):
    vyber_ids = vyber.select(pl.col("track_id")).to_series().to_list()
    return


@app.cell
def _(df, hraje_hlavne_v_prosinci, pl, po_tydnech, vsechny_tydny):
    po_tydnech_lepsi = (
        df.filter(pl.col("track_id").is_in(hraje_hlavne_v_prosinci))
        .group_by(pl.col("timestamp").dt.week())
        .len()
        .sort(by="timestamp")
    )

    # 2. Left join your grouped results onto the full list of weeks and fill nulls with 0
    po_tydnech_lepsi = vsechny_tydny.join(
        po_tydnech, on="timestamp", how="left"
    ).with_columns(pl.col("len").fill_null(0))
    return (po_tydnech_lepsi,)


@app.cell
def _(alt, po_tydnech_lepsi):
    alt.Chart(po_tydnech_lepsi).mark_bar().encode(
        alt.X("timestamp:N"), alt.Y("len:Q")
    )
    return


@app.cell
def _(df, hraje_hlavne_v_prosinci, pl):
    dny_v_listopadu = (
        df.filter(pl.col("track_id").is_in(hraje_hlavne_v_prosinci))
        .filter(pl.col("timestamp").dt.month() == 11)
        .group_by(pl.col("timestamp").dt.day())
        .len()
        .sort(by="timestamp")
    )
    return (dny_v_listopadu,)


@app.cell
def _(df, hraje_hlavne_v_prosinci, pl):
    dny_v_prosinci = (
        df.filter(pl.col("track_id").is_in(hraje_hlavne_v_prosinci))
        .filter(pl.col("timestamp").dt.month() == 12)
        .group_by(pl.col("timestamp").dt.day())
        .len()
        .sort(by="timestamp")
    )
    return (dny_v_prosinci,)


@app.cell
def _(alt, dny_v_listopadu):
    alt.Chart(dny_v_listopadu).mark_bar().encode(
        alt.X("timestamp:N"), alt.Y("len:Q")
    )
    return


@app.cell
def _(alt, dny_v_prosinci):
    alt.Chart(dny_v_prosinci).mark_bar().encode(
        alt.X("timestamp:N"), alt.Y("len:Q")
    )
    return


@app.cell
def _(pl, pomer_prosinec_neprosinec):
    pomer_prosinec_neprosinec.filter(pl.col("prosinec") >= 10).filter(
        pl.col("stanice") == 1
    ).filter((pl.col("r") > 1) | (pl.col("r").is_null())).sort(
        by="prosinec", descending=True
    )
    return


@app.cell
def _(pl, pomer_prosinec_neprosinec):
    pomer_prosinec_neprosinec.filter(pl.col("prosinec") >= 10).filter(
        pl.col("stanice") == 3
    ).filter((pl.col("r") > 1) | (pl.col("r").is_null())).sort(
        by="prosinec", descending=True
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Během prosince
    """)
    return


@app.cell
def _(df, pl, vyber):
    top_vyber_vanocnich = (
        df.filter(
            pl.col("pisen").is_in(
                vyber.head(20).select(pl.col("pisen")).to_series().to_list()
            )
        )
        .group_by("pisen")
        .len()
        .sort(by="len", descending=True)
        .head(30)
        .select(pl.col("pisen"))
        .to_series()
        .to_list()
    )
    return (top_vyber_vanocnich,)


@app.cell
def _(df, pl, top_vyber_vanocnich):
    behem_prosince = (
        df.filter(pl.col("timestamp").dt.month() == 12)
        .filter(pl.col("pisen").is_in(top_vyber_vanocnich))
        .group_by(["pisen", pl.col("timestamp").dt.day()])
        .len()
        .sort(by="len", descending=True)
        .with_columns(
            (
                (pl.col("timestamp") * pl.col("len")).sum().over("pisen")
                / pl.col("len").sum().over("pisen")
            ).alias("weighted_mean")
        )
    )

    behem_prosince_poradi = (
        behem_prosince.sort(by="weighted_mean")
        .select(pl.col("pisen"))
        .unique()
        .to_series()
        .to_list()
    )

    behem_prosince
    return behem_prosince, behem_prosince_poradi


@app.cell
def _(df, pl):
    df.filter(pl.col("track").str.starts_with("DO THEY"))
    return


@app.cell
def _(alt, behem_prosince, behem_prosince_poradi):
    alt.Chart(behem_prosince, width=600, height=1000).mark_circle().encode(
        alt.X("timestamp"),
        alt.Y("pisen:N", sort=behem_prosince_poradi),
        alt.Size("len:Q"),
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Silvestr
    """)
    return


@app.cell
def _(df, pl):
    hraje_na_silvestra = (
        df.filter(
            (pl.col("timestamp").dt.month() == 12)
            & (pl.col("timestamp").dt.day() == 31)
        )
        .select(pl.col("track_id"))
        .unique()
        .to_series()
        .to_list()
    )

    hraje_jindy_nez_na_silvestra = (
        df.filter(
            ~(
                (pl.col("timestamp").dt.month() == 12)
                & (pl.col("timestamp").dt.day() == 31)
            )
        )
        .select(pl.col("track_id"))
        .unique()
        .to_series()
        .to_list()
    )

    hraje_jen_na_silvestra = [
        x for x in hraje_na_silvestra if x not in hraje_jindy_nez_na_silvestra
    ]
    return (hraje_jen_na_silvestra,)


@app.cell
def _(df, hraje_jen_na_silvestra, pl):
    df.filter(pl.col("track_id").is_in(hraje_jen_na_silvestra)).group_by(
        ["interpret", "track"]
    ).len().sort(by="len", descending=True)
    return


if __name__ == "__main__":
    app.run()
