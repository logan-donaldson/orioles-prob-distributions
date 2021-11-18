from sklearn.neighbors import KernelDensity
import seaborn as sns
import matplotlib.pyplot as plt
from pybaseball import playerid_lookup
from pybaseball import statcast_batter
from tkinter import *
import pandas as pd

import GaussianMixtureCompatible

root = Tk()
root.title("Gaussian Mixture Model For Batted Balls")

instruction = Label(root, text="Player Search")
instruction.grid(row = 0, column = 1, pady = 10)
instruction2 = Label(root, text="Similarity Score")
instruction2.grid(row = 4, column = 1, pady = 10)


entries = []
for i in range(4):
    entry = Entry(root)
    entry.grid(row = 2, column = i, padx= 0, pady= 0)
    entries.append(entry)


for i in range(4):
    entry = Entry(root)
    entry.grid(row = 5, column = i, padx= 0, pady= 0)
    entries.append(entry)

for i in range(4):
    entry = Entry(root)
    entry.grid(row = 7, column = i, padx= 0, pady= 0)
    entries.append(entry)

firstname = Label(root, text="First")
lastname = Label(root, text="Last")
fromdate = Label(root, text="From")
todate = Label(root, text="To")
firstname.grid(row=1, column = 0, pady=1, padx = 1)
lastname.grid(row=1, column = 1, pady=1, padx = 1)
fromdate.grid(row=1, column = 2, pady=1, padx = 1)
todate.grid(row=1, column = 3, pady=1, padx = 1)
firstname = Label(root, text="First")
lastname = Label(root, text="Last")
fromdate = Label(root, text="From")
todate = Label(root, text="To")
firstname.grid(row=6, column = 0, pady=1, padx = 1)
lastname.grid(row=6, column = 1, pady=1, padx = 1)
fromdate.grid(row=6, column = 2, pady=1, padx = 1)
todate.grid(row=6, column = 3, pady=1, padx = 1)


def gaussian_mixture_model():
    first = entries[0].get()
    last = entries[1].get()
    fromdate = entries[2].get()
    todate = entries[3].get()
    idDf = pd.DataFrame(playerid_lookup(last, first))
    id = idDf["key_mlbam"][0]
    playerstats = statcast_batter(fromdate, todate, id)
    launchangle = playerstats["launch_angle"]
    exitvelocity = playerstats["launch_speed"]
    d = {"Launch Angle": launchangle, "Exit Velocity": exitvelocity}
    df = pd.DataFrame(data=d)
    df = df.dropna(how='any')
    df = df.reindex(columns=["Exit Velocity","Launch Angle"])

    GaussianMixtureCompatible.gaussian_mixture(df, first, last, True)

def similarity_score():
    first1 = entries[4].get()
    last1 = entries[5].get()
    fromdate = entries[6].get()
    todate = entries[7].get()
    idDf = pd.DataFrame(playerid_lookup(last1, first1))
    id = idDf["key_mlbam"][0]
    playerstats = statcast_batter(fromdate, todate, id)
    launchangle = playerstats["launch_angle"]
    exitvelocity = playerstats["launch_speed"]
    d = {"Launch Angle": launchangle, "Exit Velocity": exitvelocity}
    df1 = pd.DataFrame(data=d)
    df1 = df1.dropna(how='any')
    df1 = df1.reindex(columns=["Exit Velocity", "Launch Angle"])

    first2 = entries[8].get()
    last2 = entries[9].get()
    fromdate = entries[10].get()
    todate = entries[11].get()
    idDf = pd.DataFrame(playerid_lookup(last2, first2))
    id = idDf["key_mlbam"][0]
    playerstats = statcast_batter(fromdate, todate, id)
    launchangle = playerstats["launch_angle"]
    exitvelocity = playerstats["launch_speed"]
    d = {"Launch Angle": launchangle, "Exit Velocity": exitvelocity}
    df2 = pd.DataFrame(data=d)
    df2 = df2.dropna(how='any')
    df2 = df2.reindex(columns=["Exit Velocity", "Launch Angle"])

    print(GaussianMixtureCompatible.similarity_score(df1, df2, first1, last1, first2, last2))


gaussian_mixture_button = Button(root, text="Gaussian Mixture", command=gaussian_mixture_model)
gaussian_mixture_button.grid(row = 3, column = 1, pady = 10)

similarity_score_button = Button(root, text="Similarity Score", command=similarity_score)
similarity_score_button.grid(row = 8, column = 1, pady = 10)

root.mainloop()