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


entries = []
for i in range(4):
    entry = Entry(root)
    entry.grid(row = 2, column = i, padx= 0, pady= 0)
    entries.append(entry)

firstname = Label(root, text="First")
lastname = Label(root, text="Last")
fromdate = Label(root, text="From")
todate = Label(root, text="To")
firstname.grid(row=3, column = 0, pady=1, padx = 1)
lastname.grid(row=3, column = 1, pady=1, padx = 1)
fromdate.grid(row=3, column = 2, pady=1, padx = 1)
todate.grid(row=3, column = 3, pady=1, padx = 1)


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

    GaussianMixtureCompatible.gaussian_mixture(df, first, last)




button = Button(root, text="Gaussian Mixture", command=gaussian_mixture_model)
button.grid(row = 4, column = 1, pady = 10)

root.mainloop()