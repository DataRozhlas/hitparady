import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    folder = "cro"
    return (folder,)


@app.cell
def _(folder):
    import os

    if not os.path.exists(folder):
        os.mkdir(folder)
    else:
        pass
    return (os,)


@app.cell
def _():
    import requests

    return (requests,)


@app.cell
def _():
    from datetime import date, timedelta

    return date, timedelta


@app.cell
def _(date, timedelta):
    start_dt = date(2020, 12, 1)
    end_dt = date(2025, 6, 3)
    delta = timedelta(days=1)
    dates = []
    while start_dt <= end_dt:
        dates.append(str(start_dt.isoformat()))
        start_dt += delta
    return (dates,)


@app.cell
def _():
    stanice = ['radiozurnal','radiowave','dvojka','vltava','plus','d-dur','jazz','pohoda']
    return (stanice,)


@app.cell
def _(dates):
    dates
    return


@app.cell
def _(dates, folder, os, requests, stanice):
    stazene = set(os.listdir('cro'))

    for s in stanice:
        for d in dates:
            if f"{s}-{d}.json" not in stazene:
                url = f"""https://api.rozhlas.cz/data/v2/playlist/day/{d.replace("-", "/")}/{s}.json"""
                r = requests.get(url)
                with open(os.path.join(folder, f"{s}-{d}.json"), 'w+', encoding='utf-8') as f:
                    print(url)
                    f.write(r.text)
    return


if __name__ == "__main__":
    app.run()
