from pybaseball import playerid_lookup
from pybaseball import statcast_batter
from tkinter import *
import pandas as pd

root = Tk()
e = Entry(root, width=50)
e.pack()

def myClick():
    specs = e.get().split(",")
    lastname = specs[0]
    firstname = specs[1]
    year = specs[2]
    idDf = pd.DataFrame(playerid_lookup(lastname, firstname))
    id = idDf["key_mlbam"][0]
    yearstart = year + "-01-01"
    yearend = year + "-12-01"
    playerstats = statcast_batter(yearstart, yearend, id)
    launchangle = playerstats["launch_angle"]
    exitvelocity = playerstats["launch_speed"]
    d = {"Launch Angle": launchangle, "Exit Velocity": exitvelocity}
    df = pd.DataFrame(data=d)
    df = df.dropna(how='any')
    print(df.head(10))


button = Button(root, text="Enter Player and Year Specifications in format: lastname,firstname,year", command=myClick)
button.pack()

root.mainloop()