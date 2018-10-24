import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import scipy.stats as stats
import pandas

dfA = pandas.read_csv("/home/tepex/AARI/SAGA/scatterplots/source/Scatterplot [Aldegonda_elev_2018_crop]-[Ablation].txt",
                      "\t")

dfB = pandas.read_csv(
    "/home/tepex/AARI/SAGA/scatterplots/source/Scatterplot: [Aldegonda_elev_2018_crop]-[Total Insolation].txt", "\t")# dfB = pandas.read_csv("/home/tepex/AARI/SAGA/scatterplots/source/Scatterplot: [ArcticDEM_for_radiation]-[Total Insolation April15].txt", "\t")

dfC = pandas.read_csv(
    "/home/tepex/AARI/SAGA/scatterplots/source/Scatterplot: [two_zones_poly [id]]-[Aldegonda_elev_2018_crop].txt", "\t")

data = pandas.merge(dfA, dfB, on="ID")

data.columns = ["ID", "Elevation", "Ablation", "Ablation per year", "Radiation"]

data = data.iloc[:-2:2]  # let's simply remove the half of the pixels

data["Ablation per year"] = data["Ablation"] / 4

# p1 = data.plot(x="Elevation", y="Ablation", kind="scatter", s=1, c="Radiation", cmap="YlOrBr", vmin=300, vmax=600)
p1 = data.plot(x="Elevation", y="Ablation per year", kind="scatter", s=1, c="Radiation", cmap="RdBu_r", vmin=450,
               vmax=550)  # , norm=matplotlib.colors.LogNorm()

z = np.polyfit(data["Elevation"], data["Ablation per year"], 2) # 2nd order poly fit
p = np.poly1d(z)

plt.plot([x for x in range(150, 480, 10)], p([x for x in range(150, 480, 10)]), "b--", linewidth=1)
# the line equation:
print "y=%.6fx^2+%.6fx+(%.6f)" % (z[0], z[1], z[2])

#  Estimates of Error in Data/Model (prediction error):
x = data["Elevation"]
n = x.size  # number of observations
m = z.size  # number of parameters
DF = n - m  # degrees of freedom
t = stats.t.ppf(0.95, n - m)  # quantile of Student's distribution for p=0.05

ablation_modelled = np.polyval(z, data["Elevation"])  # models the ablation using our poly
resid = data["Ablation per year"] - ablation_modelled  # residuals
s_err = np.sqrt(np.sum(resid**2) / DF)  # standard deviation of the residuals

# plotting prediction band:
x2 = np.linspace(150, 450, 100)
y2 = np.linspace(np.max(ablation_modelled), np.min(ablation_modelled), 100)

a = (x2 - np.mean(x))**2
b = np.sum((x-np.mean(x))**2)  # variance, or squared standard deviation
pi = t * s_err * np.sqrt(1 + 1 / n + a / b)

# plt.fill_between(x2, p(x2)+pi, p(x2)-pi, color="None", linestyle="--")
plt.plot(x2, p(x2)-pi, "--", color="0.5", linewidth=1, label="95% Prediction Band")
plt.plot(x2, p(x2)+pi, "--", color="0.5", linewidth=1)


p2 = data.plot(x="Radiation", y="Ablation", kind="scatter", s=2, c="Elevation", cmap="RdYlGn_r", vmin=150, vmax=400)

# plotting ablation against elevation, but coloring according to zones:
data = pandas.merge(data, dfC, on="ID")
p3 = data.plot(x="Elevation", y="Ablation per year", kind="scatter", s=1, c="two_zones_poly [id]", cmap="Set1",
               norm=matplotlib.colors.BoundaryNorm(boundaries=[0, 1.1, 2.1], ncolors=2))

plt.show()
