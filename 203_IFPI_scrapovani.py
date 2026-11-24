import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import os
    import pandas as pd
    from bs4 import BeautifulSoup

    return BeautifulSoup, os


@app.cell
def _():
    folder = "ifpi"
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
def _(BeautifulSoup, os):
    def scrapuj_hitparadu(slozka, soubor):
        with open(os.path.join(slozka, soubor), "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

            h1_tag = soup.find("h1")
            subtitle_tag = soup.find(class_="header__subtitle")

            # Return None if the page doesn't have the expected chart header (e.g., 404/empty page)
            if not h1_tag or not subtitle_tag:
                return None

            hitparada = h1_tag.text.strip()
            obdobi = subtitle_tag.text.strip()
            tracky = soup.find_all(class_="chart-full-row")
            zebricek = []

            for t in tracky:
                pos_tag = t.find(class_="chart-full-row__position")
                title_tag = t.find(class_="chart-full-row__title")
                interp_tag = t.find(class_="chart-full-row__interpreter")

                if not (pos_tag and title_tag and interp_tag):
                    continue

                track = {}
                track["hitparada"] = hitparada
                track["obdobi"] = obdobi
                track["pozice"] = int(pos_tag.text.strip().split(".")[0])
                track["track/album"] = title_tag.text.strip()

                interpretstvo = interp_tag.text.strip().split("\n")
                track["interpret"] = interpretstvo[0].strip()
                track["vydavatel"] = interpretstvo[-1][2:].strip() if len(interpretstvo) > 1 else ""

                odkazy = t.find(class_="play-dropdown__menu")
                if odkazy is not None:
                    for o in odkazy.find_all("a"):
                        if o.text.strip().lower() == "youtube" and o.has_attr("href"):
                            track["youtube"] = o["href"]

                track["soubor"] = soubor
                zebricek.append(track)

        return zebricek

    return (scrapuj_hitparadu,)


@app.cell
def _():
    import time

    return (time,)


@app.cell
def _():
    kolik = 30
    return


@app.cell
def _(os):
    if not os.path.exists('data_raw'):
        os.mkdir('data_raw')
    else:
        pass
    return


@app.cell
def _():
    import json

    return (json,)



@app.cell
def _(json, os, scrapuj_hitparadu, seznam_souboru, time):
    def scrapuj_hitparady(slozka, kolik = None):
        count = 0 
        start_time = time.time()
        ke_zpracovani = [x for x in seznam_souboru(slozka)]
        for s in ke_zpracovani[:kolik]:
            time_taken = time.time() - start_time
            count = count + 1
            time_remaining = (time_taken / count) * (len(ke_zpracovani[:kolik]) - count)
            if time_remaining >= 1:
                time_remaining = int(time_remaining)
            else:
                time_remaining = "--"
            print(f"done: {count} / total: {len(ke_zpracovani[:kolik])} / ETR: {time_remaining} s / {s}")
            h = scrapuj_hitparadu(slozka, s)
            with open(os.path.join("data_raw",s.replace(".html",".json")), "w") as file:
                json.dump(h, file)

    return (scrapuj_hitparady,)


@app.cell
def _(folder, scrapuj_hitparady):
    scrapuj_hitparady(folder)
    return


if __name__ == "__main__":
    app.run()
