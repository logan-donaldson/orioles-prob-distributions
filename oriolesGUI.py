from sklearn.neighbors import KernelDensity
import seaborn as sns
import matplotlib.pyplot as plt
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

    kde = KernelDensity(bandwidth = 1.0, kernel = 'gaussian').fit(df)
    samples = kde.sample(n_samples = 10000, random_state = 42)

    samples = pd.DataFrame(samples, columns=['Launch Angle','Exit Velocity'])
    sns.set_theme(style="white")

    clip_min_y = min(samples['Exit Velocity']) - 10
    clip_max_y = max(samples['Exit Velocity']) + 10
    clip_min_x = min(samples['Launch Angle']) - 10
    clip_max_x = max(samples['Launch Angle']) + 10

    g = sns.JointGrid(data=samples, x='Launch Angle', y='Exit Velocity', space=0)
    g.plot_joint(sns.kdeplot,
             fill=True, cut = 20, clip = ((clip_min_x,clip_max_x),(clip_min_y,clip_max_y)),
             thresh=0, levels=100, cmap="rocket")
    g.plot_marginals(sns.histplot, color="#03051A", alpha=1, bins=25)
    if (lastname[-1] == 'S'):
        g.fig.suptitle(lastname.upper() + "' HEAT MAP\n", y = 1.00)
    else: 
        g.fig.suptitle(lastname.upper() + "'S HEAT MAP\n", y = 1.00)
    plt.show()
    
button = Button(root, text="Enter Player and Year Specifications in format: lastname,firstname,year", command=myClick)
button.pack()

root.mainloop()