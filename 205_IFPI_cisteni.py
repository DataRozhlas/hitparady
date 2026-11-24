import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    dropnout soubor
    vyexportovat youtube
    """)
    return


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
def _(folder, os, pd):
    df = pd.read_csv(os.path.join(folder,"ifpi_raw.csv"))
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Špatně označené roky
    """)
    return


@app.cell
def _(df):
    df.groupby(['hitparada','obdobi'])['track/album'].nunique().nlargest(50)
    return


@app.cell
def _(df):
    df.groupby('obdobi')['track/album'].nunique().nlargest(10)
    return


@app.cell
def _(df):
    df[df['obdobi'] == '8. týden 2017'][['hitparada','soubor']].drop_duplicates()
    return


@app.cell
def _(df):
    df[df['soubor'].str.contains('2503')].groupby('obdobi').size()
    return


@app.cell
def _(df):
    df[df['obdobi'] == '8. týden 2018']
    return


@app.cell
def _(df):
    df.loc[df['soubor'].str.contains('2503'),'obdobi']="8. týden 2018"
    return


@app.cell
def _(df):
    df[df['obdobi'] == '5. týden 2022'][['hitparada','soubor']].drop_duplicates()
    return


@app.cell
def _(df):
    df[df['soubor'].str.contains('2819')].groupby('obdobi').size()
    return


@app.cell
def _(df):
    df[df['obdobi'] == '5. týden 2023']
    return


@app.cell
def _(df):
    df.loc[df['soubor'].str.contains('2819'),'obdobi']="5. týden 2023"
    return


@app.cell
def _(df):
    df.groupby('obdobi')['track/album'].nunique().nlargest(10)
    return


@app.cell
def _(df):
    df_1 = df.drop(columns=['soubor'])
    return (df_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Opravy a čištění
    """)
    return


@app.cell
def _(df_1):
    hitparady = df_1['hitparada'].drop_duplicates().to_list()
    hitparady
    return (hitparady,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Aby byla data strojově čitelná
    """)
    return


@app.cell
def _(df_1):
    df_1['tyden'] = df_1['obdobi'].apply(lambda x: x.split('. t')[0] if '. t' in x else None)
    return


@app.cell
def _(df_1):
    df_1['tyden'] = df_1['tyden'].str.zfill(2)
    return


@app.cell
def _(df_1):
    df_1['mesic'] = df_1['obdobi'].apply(lambda x: x.split('/')[0].split(' ')[1] if 'Měsíc' in x else None)
    return


@app.cell
def _(df_1):
    df_1['mesic'] = df_1['mesic'].str.zfill(2)
    return


@app.cell
def _(df_1):
    df_1['rok'] = df_1['obdobi'].apply(lambda x: x[-4:])
    return


@app.cell
def _(df_1):
    df_1.groupby('tyden')['track/album'].nunique().nsmallest(15)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Oprava chybných dat
    """)
    return


@app.cell
def _(df_1):
    df_1['rok'] = df_1['rok'].apply(lambda x: x.replace('223', '2023').replace(' 201', '2010').replace('2104', '2014').strip())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Týdny dvouciferně
    """)
    return


@app.cell
def _(df_1):
    df_1['tyden'].drop_duplicates().to_list()
    return


@app.function
def cistetydny(x):
    
    try:
        
        x = x.replace(".","").replace("+","")
        if len(x) == 2:
            t = x
        else:
            if x[0:2] != "52":
                t = x[-2:]
            else:
                t = "52"
    
    except:
        
        t = x
    
    return t


@app.cell
def _():
    cistetydny('200809')
    return


@app.cell
def _(df_1):
    df_1['tyden'] = df_1['tyden'].apply(lambda x: cistetydny(x))
    return


@app.cell
def _(df_1):
    df_1['tyden'].drop_duplicates().to_list()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Doplnění týdne
    """)
    return


@app.function
def weekuj(rok, tyden):
    try:
        return f"""{rok}-{tyden:02}"""
    except:
        return None


@app.cell
def _(df_1):
    df_1['week'] = df_1.apply(lambda x: weekuj(x['rok'], x['tyden']), axis=1)
    return


@app.cell
def _(df_1):
    df_1['week']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Pryč s dvojitými mezerami
    """)
    return


@app.cell
def _(df_1):
    df_2 = df_1.apply(lambda x: x.replace('  ', ' '))
    return (df_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Pryč s velkými písmeny (nebo jejich většinou)
    """)
    return


@app.cell
def _(df_2):
    slovodelice = [' ', '.', '/']
    for s in slovodelice:
        df_2['interpret'] = df_2['interpret'].apply(lambda x: s.join((word.title() for word in str(x).split(s))))
        df_2['vydavatel'] = df_2['vydavatel'].apply(lambda x: s.join((word.title() for word in str(x).split(s))))
    return


@app.cell
def _(df_2):
    df_2.sample(5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Sjednocení jmen
    """)
    return


@app.cell
def _(df_2):
    df_2[df_2['interpret'].str.lower().str.contains('vířat', na=False)]['interpret'].drop_duplicates().to_list()
    return


@app.cell
def _():
    spravna_jmena = {
        "Ondřej G. Brzobohatý": "Ondřej Brzobohatý",
        "M. Cyrus": "Miley Cyrus",
        "Ulrychovi Hana & Petr": "Hana A Petr Ulrychovi",
        "Ulrychovci":  "Hana A Petr Ulrychovi",
        "Miroslav Žbirka": "Miro Žbirka",
        "P.Hapka": "Petr Hapka",
        "Natalie Grossová": "Natálie Grossová",
        "Tichá Kateřina Marie": "Kateřina Marie Tichá",
        "Al Dhaba Gába": "Gabriela Al Dhábba",
        "Křížek Láďa": "Ladislav Křížek",
        "AC/DC": "ACDC",
        " A Jiní": "",
        " A ": " a "
    }
    return (spravna_jmena,)


@app.cell
def _(df_2):
    _interpreti = df_2['interpret'].drop_duplicates().to_list()
    [x for x in _interpreti if len(x.split()) > 1 and f'{x.split()[1]} {x.split()[0]}' in _interpreti]
    return


@app.cell
def _():
    obracena_jmena = ["Bohouš Josef","Bílá Lucie","Žbirka Miro","Vondráčková Lucie", "Jiřina Anna Jandová", "Smolík Jakub", "Sofian Medjmedj", "Josef Bohouš", "Müller Richard","Rolins Dara", "Zmožek Marcel", "Hrůza Michal", "Deyl David", "Bende Petr", "Zonyga Jiří", "Hapka Petr", "Nedvěd František", "Mrózek Daniel", "Issa Sámer","Koller David","Ondra Jakub", "Smejkal Jaro", "Vondráčková Helena", "Střihavka Kamil", "Charvátová Jitka", "Goldová Gabriela","Přenosilová Yvonne", "Machálková Leona","Prokop Michal","Suchý Jiří","Langerová Aneta","Daniel Šafařík", "Jandová Marta", "Horváth Vlastimil", "Horecká Hana", "Farna Ewa", "John Wolfhooker", "Adam Janota",  "Dyk Vojtěch", "Jíšová Pavlína", "Sanchez Yvonne", "Ruppert Matěj", "Burian Michael", "Brzobohatá Katka", "Václav Rouček", "Šinkorová Daniela", "Šeps Michal", "Absolonová Monika", "Zíma Josef", "Rouček Václav","Schmitzer Jiří","Ztracený Marek", "Zemanová Bára", "Bastien Alan", "Maxa Martin", "Matuš Bohuš", "Hron Vláďa", "Hudček Michal", "Háma Aleš", "Hübsch Kamila", "Hůlka Daniel", "Milfajtová Sára", "Krajčo Richard", "Kraus David", "Kreyson Memorial", "Krézlová Karolína", "Josef Vágner, Charlotte Gottová", "Hladík Radim", "Peter Fider", "Drda Zbyněk", "Paul Project", "Povýšilová Monika", "Poláček Petr", "Poliak Michal", "Hanák Tomáš", "Hayek Martin", "Nekonečný Dan", "Neckář Václav", "Novotný Miloš","Rosová Sandra","Vojtek Roman","Bagová Ivanna","Kerndlová Tereza","Kotvald Petr",'Simon Paul',"Albarn Damon",
     'Jones Norah',
     'Baumaxa Xavier',
     'Chao Manu',
     'Gahan Dave',
     'Lipa Peter',
     'Pospíšil Luboš',
     'Sodoma Viktor',
     'Ward Shayne',
     'Toxxx Hugo',
     'Tobias Szidi',
     'Cohen Avishai',
     'Petřina Ota',
     'Janů Petra',
     'Pop Iggy',
     'Streisand Barbra',
     'Satriani Joe',
     'Bárta Dan',
     'Knechtová Katarína',
     'Hybš Václav',
     'Spálený Jan',
     'Šporcl Pavel',
     'Ruml Ondřej',
     'Merta Vladimír',
     'Havelka Ondřej',
     'Dragoun Roman',
     'Smith Patti',
     'Young Neil',
     'Brown Chris',
     'Mercury Freddie',
     'Caballé Monserrat',
     'Horáček Michal',
     'Havelka Ondřej',
     'Merta Vladimír',
     'Dědeček Jiří',
     'Bruni Carla',
     'Mišík Vladimír',
     'Bonamassa Joe',
     'Zagorová Hana',
     'Petty Tom',
     'Bennett Tony',
     'Dusilová Lenka',
     'Ondřej Havelka',
     'Ruml Ondřej',
     'Szidi Tobias',
     'Ondřej Havelka',
     'Roman Dragoun And His Angels',
     'Avishai Cohen Trio',
     'Sinatra Frank',
     'Zdeněk Bína',
     'Melody Gardot',
     'Petřina Ota',
     'Cooper Alice',
     'Satriani Joe',
     'Veverka Vilém',
     'Bernstein Leonard',
     'Dragoun Roman',
     'Clyro Biffy',
     'Gardot Melody',
     'Spálený Jan',
     'Hybš Václav',
     'Michal Hromek',
     'Bernstein Leonard',
     'Veverka Vilém',
     'Svěcený Jaroslav',
     'Semerádová Jana',
     'Ramazzotti Eros & Anastacia',
     'Foret Michael',
     'Ward Shayne',
     'Keys Alicia & White Jack',
     'Burke Alexandra Feat. Flo Rida',
     'Bieber Justin',
     'Tempah Tinie',
     'Williams Robbie',
     'Iglesias Enrique',
     'Solveig Martin',
     'Lopez Jennifer',
     'Sinclar Bob',
     'Posner Mike',
     'Brown Chris',
     'Solveig Martin',
     'Lopez Jennifer',
     'Brown Chris',
     'Gomez Selena',
     'Murs Olly',
     'Harris Calvin',
     'Burke Alexandra',
     'Konvičková Markéta',
     'Harris Calvin',
     'Grey Skylar',
     'Romero Nicky',
     'Solveig Martin',
     'Derulo Jason',
     'Tempah Tinie',
     'Lavigne Avril',
     'Harris Calvin',
     'Bublé Michael',
     'Aristone Peter',
     'Garand Paulie',
     'Azalea Iggy',
     'Paul Sean',
     'Ponte Gabry',
     'Cooper Alice',
     'Bína Zdeněk',
     'Bezdeda Tomáš',
     'Opatovský Robo',
     'Kerndlová Tereza',
     'Kmeťo Igor',
     'Lipa Peter',
     'Tomáš Bezdeda',
     'Mirgová Dominika',
                     'Gahan Dave',
                     'Cohen Avishai',
                     'Smith Patti',
                     'Dragoun Roman',
                     'Gott Karel',
                     'Savka Tomáš',
                     'Schmitzer Jiří',
                     'Cristovao Ben',
                     "Norisová Zuzana",
                     "Guetta David",
                     "Gaudino Alex",
                     "Dione Aura",
                     "Wolf Laurent",
                     "Scherzinger Nicole",
                     "Kingston Sean",
                     "Hilson Keri",
                     "Ryan Kate",
                     "Wolf Karl"]
    return (obracena_jmena,)


@app.cell
def _(obracena_jmena):
    obracena_jmena
    return


@app.cell
def _(obracena_jmena, spravna_jmena):
    for o in obracena_jmena:
        spravna_jmena[o] = f"{o.split()[1]} {o.split()[0]}"
    return


@app.cell
def _(df_2, spravna_jmena):
    for key, val in spravna_jmena.items():
        df_2['interpret'] = df_2['interpret'].apply(lambda x: x.replace(key, val))
    return


@app.cell
def _(df_2):
    _interpreti = df_2['interpret'].drop_duplicates().to_list()
    [x for x in _interpreti if len(x.split()) > 1 and f'{x.split()[1]} {x.split()[0]}' in _interpreti]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Hlavní intepreti
    """)
    return


@app.cell
def _(df_2):
    df_2[df_2['interpret'].str.contains(' a ')]['interpret'].drop_duplicates()
    return


@app.function
def kdojeprvni(x):
    delice = ["&","/","(feat.","feat.","Feat."," a "]
    for d in delice:
        if d in x:
            x = x.split(d)[0]
    return x.strip()


@app.cell
def _(df_2):
    df_2['interpret_hlavni'] = df_2['interpret'].apply(lambda x: kdojeprvni(x))
    return


@app.cell
def _(df_2):
    df_2['interpret_hlavni'].drop_duplicates().to_list()
    return


@app.cell
def _(df_2):
    len(df_2[df_2['hitparada'] == 'CZ - RADIO - TOP 100']['interpret_hlavni'].drop_duplicates().to_list())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Album/track
    """)
    return


@app.cell
def _(df_2):
    df_2['album'] = df_2.apply(lambda row: row['track/album'] if 'ALBUM' in row['hitparada'] else None, axis=1)
    return


@app.cell
def _(df_2):
    df_2['track'] = df_2.apply(lambda row: row['track/album'] if 'ALBUM' not in row['hitparada'] else None, axis=1)
    return


@app.cell
def _(df_2):
    df_3 = df_2.drop(columns=['track/album', 'obdobi'])
    return (df_3,)


@app.cell
def _():
    poradi = ['hitparada','rok','mesic','tyden','week','pozice','album','track','interpret','interpret_hlavni','vydavatel','youtube']
    return (poradi,)


@app.cell
def _(df_3, poradi):
    df_4 = df_3.reindex(columns=poradi)
    return (df_4,)


@app.cell
def _(df_4):
    df_4[(df_4['week'] == '2017-08') & df_4['hitparada'].str.contains('RADIO')].shape
    return


@app.cell
def _(df_4):
    df_4[(df_4['week'] == '2017-08') & df_4['hitparada'].str.contains('RADIO')].head(60)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Seřazení
    """)
    return


@app.cell
def _(df_4):
    df_5 = df_4.sort_values(by=['hitparada', 'rok', 'mesic', 'tyden', 'pozice'])
    return (df_5,)


@app.cell
def _(df_5):
    df_5.sample(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Oprava chybných oprav (nutno zde)
    """)
    return


@app.cell
def _(df_5):
    df_5.loc[df_5['interpret'] == 'Nico & Vinz', 'interpret_hlavni'] = 'Nico & Vinz'
    df_5.loc[df_5['interpret'] == 'Zagorová', 'interpret_hlavni'] = 'Hana Zagorová'
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Youtube do samostatného dataframu
    """)
    return


@app.cell
def _(os):
    if not os.path.exists('data'):
        os.mkdir('data')
    else:
        pass
    return


@app.cell
def _(df_5):
    df_5
    return


@app.cell
def _(df_5, os):
    yt = df_5[['interpret_hlavni', 'track', 'youtube']].drop_duplicates()
    yt.to_csv(os.path.join('data', 'youtube_linky.csv'))
    return


@app.cell
def _(df_5):
    df_6 = df_5.drop(columns=['youtube'])
    return (df_6,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Export do jednotlivých dataframů
    """)
    return


@app.cell
def _(df_6):
    df_6
    return


@app.cell
def _(df_6, hitparady, os):
    for h in hitparady:
        df_p = df_6[df_6['hitparada'] == h].reset_index(drop=True)
        if 'ALBUMS' in h:
            df_p = df_p.drop(columns=['track'])
        else:
            df_p = df_p.drop(columns=['album'])
        df_p2 = df_p[~df_p['mesic'].isnull()]
        h = h.replace(' ', '_').replace('-_', '')
        if len(df_p2) > 0:
            df_p2 = df_p2.drop(columns=['tyden'])
            df_p2.to_csv(os.path.join('data', f'{h}_mesicni.csv'), index=False)
        df_p2 = df_p[~df_p['tyden'].isnull()]
        if len(df_p2) > 0:
            df_p2 = df_p2.drop(columns=['mesic'])
            df_p2.to_csv(os.path.join('data', f'{h}_tydenni.csv'), index=False)
    return


if __name__ == "__main__":
    app.run()
