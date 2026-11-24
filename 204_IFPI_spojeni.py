import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import os

    return (os,)


@app.cell
def _():
    import pandas as pd

    return (pd,)


@app.cell
def _():
    folder = "data_raw"
    return (folder,)


@app.cell
def _(os):
    def seznam_souboru(slozka):
        seznam = []
        for file in os.listdir(slozka):
            seznam.append(file)
        return(seznam)

    return (seznam_souboru,)


@app.cell
def _(folder, seznam_souboru):
    raw_data = seznam_souboru(folder)
    return (raw_data,)



@app.cell
def _(folder, os, pd, raw_data):
    df = pd.DataFrame()
    count = 0
    for r in raw_data:
        count = count + 1
        print(f"done: {count} / total: {len(raw_data)} / {r}")
        if ".json" in r: 
            df = pd.concat([df, pd.read_json(os.path.join(folder,r))])
    return (df,)


@app.cell
def _(df, folder, os):
    df.to_csv(os.path.join(folder,"ifpi_raw.csv"))
    return


if __name__ == "__main__":
    app.run()
