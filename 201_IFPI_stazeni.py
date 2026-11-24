import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    hitparady = {
        "CZ - ALBUMS - TOP 100": "14",
        "CZ - ALBUMS CLASSICAL - TOP 10": "25",
        "CZ - RADIO - TOP 100": "2",
        "CZ - RADIO - TOP 20 MODERN ROCK": "21",
        "CZ - RADIO - TOP 50 CZ": "7",
        "CZ - SINGLES DIGITAL - TOP 100": "30",
        "CZ - SINGLES DIGITAL - TOP 50 CZ": "32",
        "SK - ALBUMS - TOP 100": "36",
        "SK - RADIO - TOP 100": "40",
        "SK - RADIO - TOP 50 SK": "42",
        "SK - SINGLES DIGITAL - TOP 100": "43",
        "SK - SINGLES DIGITAL - TOP 50 SK": "44"
    }
    return (hitparady,)


@app.cell
def _(hitparady):
    len(hitparady)
    return


@app.cell
def _():
    folder = "ifpi"
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
def _(folder, os, requests):
    def stahni_hitparady(hitparady, weekmin, weekmax):
        celkem = len(hitparady) * (weekmax - weekmin + 1)
        prubeh = 0
        for key, val in hitparady.items():
            for i in range (weekmin, weekmax + 1):
                url = f"https://ifpicr.cz/hitparada/{val}?weekId={i}"
                soubor = f"{val}-{i}.html"
                prubeh = prubeh + 1
                if soubor not in os.listdir(folder):
                    r = requests.get(url)
                    print(f"{prubeh}/{celkem} / {url}")
                    if "Při načítání hitparády došlo k chybě" not in r.text:
                        with open(os.path.join(folder, soubor), 'w+', encoding='utf-8') as f:
                            f.write(r.text)

    return (stahni_hitparady,)


@app.cell
def _(hitparady, stahni_hitparady):
    stahni_hitparady(hitparady, 1296, 3043)
    return


if __name__ == "__main__":
    app.run()
