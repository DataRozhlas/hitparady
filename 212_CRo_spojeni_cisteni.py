import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import os
    import json
    import polars as pl

    return json, os, pl


@app.cell
def _(json):
    def load_json_file(file):
        with open(file) as f:
            data = json.load(f)
        return data["data"]

    return (load_json_file,)


@app.cell
def _(load_json_file, os, pl):
    df = pl.DataFrame()

    for soubor in os.listdir("cro"):
        if soubor.endswith(".json"):
            try:
                dzejsn = load_json_file(os.path.join("cro", soubor))
            except Exception as e:
                print(f"{soubor}: {e}")
            try:
                stanicoden = pl.DataFrame(
                    dzejsn,
                    schema=pl.Schema(
                        {
                            "since": pl.String,
                            "id": pl.String,
                            "interpret": pl.String,
                            "track": pl.String,
                            "track_id": pl.String,
                            "stanice": pl.String,
                            "interpret_id": pl.String,
                            "itemcode": pl.String,
                        }
                    ),
                )
            except Exception as e:
                print(f"{soubor}: {e}")
            stanice = soubor.split("-2")[0]
            if len(stanicoden) > 0:
                try:
                    df = pl.concat(
                        [
                            df,
                            stanicoden.with_columns(
                                pl.lit(stanice).alias("stanice")
                            ),
                        ]
                    )
                except Exception as e:
                    print(f"{soubor}: {e}")

    df = (
        df.with_columns(pl.col("since").str.to_datetime(time_zone="Europe/Prague"))
        .drop("files", strict=False)
        .with_columns(pl.col("stanice").cast(pl.Categorical))
        .sort(by="since")
    )
    return (df,)


@app.cell
def _(df):
    df.sample(10)
    return


@app.cell
def _(df, os):
    df.write_parquet(os.path.join("data", "cro_x.parquet"), use_pyarrow=True)
    print("Uloženo.")
    return


@app.cell
def _(df, pl):
    df.filter(pl.col("since").dt.hour() == 0)
    return


if __name__ == "__main__":
    app.run()
