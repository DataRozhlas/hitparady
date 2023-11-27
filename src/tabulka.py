def tabulka(
    frame,
    titulek="",
    podtitulek="",
    vysvetlivka="",  # zpětná kompatibilita
    bez_tecky=[],
    na_procenta=[],
    poradi=False,
    bez_zavorek=True,
    apostrofy=True
):
    import pandas as pd

    if podtitulek != "":
        vysvetlivka = podtitulek

    df_tabulka = frame.copy()

    def cela(x):
        try:
            x = int(x)
        except:
            x = "–"
        return x

    import re

    if poradi:
        sloupce = df_tabulka.columns.tolist()
        df_tabulka = df_tabulka.reset_index(drop=True)
        df_tabulka[" "] = pd.to_numeric(df_tabulka.index)
        df_tabulka[" "] = df_tabulka[" "].apply(lambda x: str(x + 1) + ".")
        nove_sloupce = [" "]
        for s in sloupce:
            nove_sloupce.append(s)
        df_tabulka = df_tabulka[nove_sloupce]

    sloupcu = len(df_tabulka.columns)

    if len(bez_tecky) > 0:
        for b in bez_tecky:
            df_tabulka[b] = df_tabulka[b].apply(lambda x: cela(x))

    if len(na_procenta) > 0:
        for p in na_procenta:
            df_tabulka[p] = df_tabulka[p].apply(lambda x: "{:.1%}".format(x))
            df_tabulka[p] = (
                df_tabulka[p]
                .astype("string")
                .apply(lambda x: x.replace(".", ",").replace("%", " %"))
            )
            
    df_tabulka = re.sub("\\n\s*", "", df_tabulka.to_html(index=False))
    df_tabulka = (
        df_tabulka.replace("<th>", '<th class="text-nowrap">')
        .replace("<tbody>", '<tbody class="text-sm">')
        .replace("border=\"1\" ", "")
        .replace(
            'class=\"dataframe\"',
            'class=\"dataframe table table--responsive table--w100p table--striped-red table--plain\"',
        )
        .replace(" , ", ", ")
    )

    if apostrofy == True:
        df_tabulka = df_tabulka.replace("\'","’")
    
    if len(titulek) > 0:
        df_tabulka = df_tabulka.replace(
            "<thead", f"<caption>{titulek}</caption><thead")

    if len(vysvetlivka) > 0:
        df_tabulka = df_tabulka.replace(
            "</tbody>",
            f'</tbody><tfoot><tr style="text-align: center;"><td colspan={sloupcu}>{vysvetlivka}</td></tr></tfoot>',
        )

    if bez_zavorek:
        df_tabulka = re.sub("\([\d]*\)", "", df_tabulka)
        df_tabulka = df_tabulka.replace(" </td>", "</td>")
        
    return (df_tabulka)