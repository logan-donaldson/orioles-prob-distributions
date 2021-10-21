from sklearn.neighbors import KernelDensity
import seaborn as sns
import matplotlib.pyplot as plt
from pybaseball import playerid_lookup
from pybaseball import statcast_batter
from tkinter import *
import pandas as pd

root = Tk()
root.title("Compare Players")

header = Label(root, text="Player Comparison GUI")
header.grid(row = 0, column = 1)

instructions1 = Label(root, text="Lookup a Player")
instructions2 = Label(root, text="Compare Two Players")
instructions1.grid(row = 1, column = 1, pady = 1, padx = 1)
instructions2.grid(row = 5, column = 1, pady = 1, padx = 1)

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
firstname = Label(root, text="First")
lastname = Label(root, text="Last")
fromdate = Label(root, text="From")
todate = Label(root, text="To")
firstname.grid(row=7, column = 0, pady=1, padx = 1)
lastname.grid(row=7, column = 1, pady=1, padx = 1)
fromdate.grid(row=7, column = 2, pady=1, padx = 1)
todate.grid(row=7, column = 3, pady=1, padx = 1)
firstname = Label(root, text="First")
lastname = Label(root, text="Last")
fromdate = Label(root, text="From")
todate = Label(root, text="To")
firstname.grid(row=9, column = 0, pady=1, padx = 1)
lastname.grid(row=9, column = 1, pady=1, padx = 1)
fromdate.grid(row=9, column = 2, pady=1, padx = 1)
todate.grid(row=9, column = 3, pady=1, padx = 1)


for i in range(4):
    entry = Entry(root)
    entry.grid(row = 6, column = i)
    entries.append(entry)

for i in range(4):
    entry = Entry(root)
    entry.grid(row=8, column=i)
    entries.append(entry)

def KDE():
    firstname = entries[0].get()
    lastname = entries[1].get()
    fromdate = entries[2].get()
    todate = entries[3].get()
    idDf = pd.DataFrame(playerid_lookup(lastname, firstname))
    id = idDf["key_mlbam"][0]
    #yearstart = year + "-01-01"
    #yearend = year + "-12-01"
    playerstats = statcast_batter(fromdate, todate, id)
    launchangle = playerstats["launch_angle"]
    exitvelocity = playerstats["launch_speed"]
    d = {"Launch Angle": launchangle, "Exit Velocity": exitvelocity}
    df = pd.DataFrame(data=d)
    df = df.dropna(how='any')
    print(df.head(10))

    ##############################################
    # Testing something I saw in class: KL-Divergence
    # Supposedly is a good way to compare distributions of pdfs
    
    #############################################

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
    
button1 = Button(root, text="KDE", command=KDE)
button1.grid(row = 4, column = 1, pady = 10)

button2 = Button(root, text="Compare", command=KDE)
button2.grid(row = 10, column = 1, pady=10)

root.mainloop()