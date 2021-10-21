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
    playerstats = statcast_batter(fromdate, todate, id)
    launchangle = playerstats["launch_angle"]
    exitvelocity = playerstats["launch_speed"]
    d = {"Launch Angle": launchangle, "Exit Velocity": exitvelocity}
    df = pd.DataFrame(data=d)
    df = df.dropna(how='any')
    df = df.reindex(columns=["Exit Velocity","Launch Angle"])
    print(df.head(10))


    kde = KernelDensity(bandwidth = 1.0, kernel = 'gaussian').fit(df)

    sns.set_theme(style="white")

    clip_min_x = min(df['Exit Velocity']) - 10
    clip_max_x = max(df['Exit Velocity']) + 10
    clip_min_y = min(df['Launch Angle']) - 10
    clip_max_y = max(df['Launch Angle']) + 10

    g = sns.JointGrid(data=df, x='Exit Velocity', y='Launch Angle', space=0)
    g.plot_joint(sns.kdeplot,
             fill=True, cut = 20, clip = ((clip_min_x,clip_max_x),(clip_min_y,clip_max_y)),
             thresh=0, levels=100, cmap="rocket")
    g.plot_marginals(sns.histplot, color="#03051A", alpha=1, bins=25)
    g.plot_joint(sns.scatterplot)
    if (lastname.upper()[-1] == 'S'):
        g.fig.suptitle(lastname.upper() + "' HEAT MAP\n", y = 1.00)
    else: 
        g.fig.suptitle(lastname.upper() + "'S HEAT MAP\n", y = 1.00)
    plt.show()

def Compare():
    firstname1 = entries[4].get()
    lastname1 = entries[5].get()
    fromdate1 = entries[6].get()
    todate1 = entries[7].get()
    idDf1 = pd.DataFrame(playerid_lookup(lastname1, firstname1))
    id1 = idDf1["key_mlbam"][0]
    playerstats1 = statcast_batter(fromdate1, todate1, id1)
    launchangle1 = playerstats1["launch_angle"]
    exitvelocity1 = playerstats1["launch_speed"]
    d1 = {"Launch Angle": launchangle1, "Exit Velocity": exitvelocity1}
    df1 = pd.DataFrame(data=d1)
    df1 = df1.dropna(how='any')

    kde1 = KernelDensity(bandwidth=1.0, kernel='gaussian').fit(df1)
    samples1 = kde1.sample(n_samples=10000, random_state=42)

    samples1 = pd.DataFrame(samples1, columns=['Launch Angle', 'Exit Velocity'])
    sns.set_theme(style="white")

    clip_min_y = min(samples1['Exit Velocity']) - 10
    clip_max_y = max(samples1['Exit Velocity']) + 10
    clip_min_x = min(samples1['Launch Angle']) - 10
    clip_max_x = max(samples1['Launch Angle']) + 10

    g1 = sns.JointGrid(data=samples1, x='Launch Angle', y='Exit Velocity', space=0)
    g1.plot_joint(sns.kdeplot,
                 fill=True, cut=20, clip=((clip_min_x, clip_max_x), (clip_min_y, clip_max_y)),
                 thresh=0, levels=100, cmap="rocket")
    g1.plot_marginals(sns.histplot, color="#03051A", alpha=1, bins=25)
    if (lastname1[-1] == 'S'):
        g1.fig.suptitle(lastname1.upper() + "' HEAT MAP\n", y=1.00)
    else:
        g1.fig.suptitle(lastname1.upper() + "'S HEAT MAP\n", y=1.00)
    #plt.show()
    firstname2 = entries[8].get()
    lastname2 = entries[9].get()
    fromdate2 = entries[10].get()
    todate2 = entries[11].get()
    idDf2 = pd.DataFrame(playerid_lookup(lastname2, firstname2))
    id2 = idDf2["key_mlbam"][0]
    playerstats2 = statcast_batter(fromdate2, todate2, id2)
    launchangle2 = playerstats2["launch_angle"]
    exitvelocity2 = playerstats2["launch_speed"]
    d2 = {"Launch Angle": launchangle2, "Exit Velocity": exitvelocity2}
    df2 = pd.DataFrame(data=d2)
    df2 = df2.dropna(how='any')

    kde2 = KernelDensity(bandwidth=1.0, kernel='gaussian').fit(df2)
    samples2 = kde2.sample(n_samples=10000, random_state=42)

    samples2 = pd.DataFrame(samples2, columns=['Launch Angle', 'Exit Velocity'])
    sns.set_theme(style="white")

    clip_min_y = min(samples2['Exit Velocity']) - 10
    clip_max_y = max(samples2['Exit Velocity']) + 10
    clip_min_x = min(samples2['Launch Angle']) - 10
    clip_max_x = max(samples2['Launch Angle']) + 10

    g2 = sns.JointGrid(data=samples2, x='Launch Angle', y='Exit Velocity', space=0)
    g2.plot_joint(sns.kdeplot,
                  fill=True, cut=20, clip=((clip_min_x, clip_max_x), (clip_min_y, clip_max_y)),
                  thresh=0, levels=100, cmap="rocket")
    g2.plot_marginals(sns.histplot, color="#03051A", alpha=1, bins=25)
    if (lastname2[-1] == 'S'):
        g2.fig.suptitle(lastname2.upper() + "' HEAT MAP\n", y=1.00)
    else:
        g2.fig.suptitle(lastname2.upper() + "'S HEAT MAP\n", y=1.00)
    plt.show()






button1 = Button(root, text="KDE", command=KDE)
button1.grid(row = 4, column = 1, pady = 10)

button2 = Button(root, text="Compare", command=Compare)
button2.grid(row = 10, column = 1, pady=10)

root.mainloop()