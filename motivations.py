
#motivation 1

import matplotlib.pyplot as plt
import matplotlib.pyplot as mp
import json
import numpy as np

plt.style.use(['default'])
mp.rcParams['pdf.fonttype'] = 42
mp.rcParams['ps.fonttype'] = 42
plt.rc('axes', axisbelow=True)
plt.rcParams["font.family"] = "Gill Sans"

sources = ['nuclear', 'wind', 'hydro', 'geothermal', 'solar', 'biomass', 'gas', 'oil', 'coal']
sources_title = ['Nuclear', 'Wind', 'Hydro', 'Geo-\nthermal', 'Solar', 'Biomass', 'Gas', 'Oil', 'Coal']

with open('./data/source_ci_ewif.json', 'r') as file:
    data = json.load(file)

CI = []
EWIF = []
 
for i in sources:
    CI.append(data[i]["CI"])
    EWIF.append(data[i]["EWIF"])
barWidth=0.6
fig = mp.figure(figsize=(7.5,1.5))
mp.subplots_adjust(wspace=0.33, hspace=0.2)
axs = mp.subplot(121)
plt.bar([i for i in range(len(CI))],CI, width = barWidth, color = '#fdb42f', edgecolor = 'black',capsize=15)
axs.set_xticks([0,1,2,3,4,5,6,7,8])
axs.set_xticklabels(sources_title, rotation=90, fontsize=13)
axs.grid(which='major', axis='y', ls='dotted', zorder=0)
axs.tick_params(labelsize=13)
axs.set_ylabel("Carbon Intensity\n (gCO$_2$/kWh)" , fontsize=13,labelpad=-3)
axs.axvline(x=5.5, linewidth=1, linestyle='--', color='black')
axs.set_yticks(np.arange(0, 1600, 400))
axs = mp.subplot(122)

axs.axvline(x=5.5, linewidth=1, linestyle='--', color='black')
axs.bar([i for i in range(len(EWIF))],EWIF, width = barWidth, color = '#4169E1', edgecolor = 'black')
axs.set_axisbelow(True)
axs.set_xticks([0,1,2,3,4,5,6,7,8])
axs.set_xticklabels(sources_title, rotation=90, fontsize=13)
axs.set_ylabel("Energy Water \n Intensity Factor \n(L/kWh)" , fontsize=13,labelpad=-2)#, y=0.4)
axs.text(5.5,19,"Fossil Energy", fontsize=13,color='black')
axs.text(-7.2,19,"Fossil Energy", fontsize=13,color='black')
axs.text(-13,19,"Renewable Energy", fontsize=13,color='black')
axs.text(-0.5,19,"Renewable Energy", fontsize=13,color='black')
axs.tick_params(labelsize=13)
axs.set_yticks(np.arange(0, 20, 6))
axs.grid(which='major', axis='y', ls='dotted', zorder=0)
plt.savefig("./motivations/motiv1.pdf",bbox_inches='tight')
plt.show()

#Fig 2
import matplotlib.pyplot as plt
import matplotlib.pyplot as mp
import json
import numpy as np
from matplotlib.gridspec import GridSpec
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
plt.rc('axes', axisbelow=True)
plt.rcParams["font.family"] = "Gill Sans"
def get_wue(s,tw_c):
    tw = (tw_c*9/5)+32
    factor = s/(s-1)
    return factor*(6*(10**-5)*tw**3-0.01*tw**2+0.61*tw-10.4)
def get_ewif(d_region, d_sources):
    ratio_ewif = 0
    for source in d_sources:
        ratio_ewif += 0.01*d_region[source]*d_sources[source]["EWIF"]
    return ratio_ewif
S=3
REGIONS = ["Zurich","Madrid","Oregon","Milan","Mumbai"]
regions = ["zurich","madrid","oregon","milan","mumbai"]
colors = ['#fdb42f', '#4169E1', '#33AFFF', '#FF6433']
with open('./data/source_ci_ewif.json', 'r') as file:
    energy_data = json.load(file)
with open('./data/region_mix_2023.json', 'r') as file:
    region_data = json.load(file)
sources =  ['nuclear', 'wind', 'hydro', 'geothermal', 'solar', 'biomass', 'gas', 'oil', 'coal']
CI = []
WSF = []
WUE = []
EWIF = []
for region in regions:
    CI.append(region_data[region]["ci"])
    WSF.append(region_data[region]["wsf"])
    WUE.append(get_wue(S,region_data[region]["temp"]))
    EWIF.append(get_ewif(region_data[region],energy_data))
barWidth=0.5
fig = plt.figure(figsize=(12.8, 2.2))
gs = GridSpec(1, 4, figure=fig, wspace=0.25, left=0.1, right=0.96)
x=np.arange(5)
axs =fig.add_subplot(gs[0, 0])
axs.bar(x, CI, width=barWidth,  zorder=3, edgecolor='black', linewidth=1, color=colors[0],label="Keep-alive Carbon")
axs.set_xticks(x)
axs.set_xticklabels(REGIONS,fontsize=12,rotation=15)
axs.grid(which='major', axis='y', ls='dotted', zorder=0)
axs.tick_params(labelsize=13,axis='y')
axs.set_ylabel("Carbon Intensity \n(gCO$_2$/kWh)", fontsize=13,labelpad=0)
axs.set_yticks(np.arange(0, 1200, 400))
axs.set_title("(a)", fontsize=12, y=-0.33)
axs = fig.add_subplot(gs[0, 1])
axs.bar([i for i in range(5)],EWIF, width = barWidth, color = colors[1], edgecolor = 'black')
axs.set_axisbelow(True)
axs.set_xticks([0,1,2,3,4])
axs.set_xticklabels(REGIONS,fontsize=12,rotation=15)
axs.set_ylabel("Energy Water \nIntensity Factor (L/kWh)" , fontsize=13,labelpad=0)#, y=0.4)
axs.tick_params(labelsize=13,axis='y')
axs.grid(which='major', axis='y', ls='dotted', zorder=0)
axs.set_yticks(np.arange(0, 9, 3))
axs.set_title("(b)", fontsize=12, y=-0.33)
axs = fig.add_subplot(gs[0, 2])
plt.bar([i for i in range(5)],WUE, width = barWidth, color =colors[2], edgecolor = 'black',capsize=15)
axs.set_axisbelow(True)
axs.set_xticks([0,1,2,3,4])
axs.set_xticklabels(REGIONS,rotation=15,fontsize=12)
axs.set_ylabel( "Water Usage \nEffectiveness (L/kWh)", fontsize=13,labelpad=0)#, y=0.4)
axs.tick_params(labelsize=13,axis='y')
axs.grid(which='major', axis='y', ls='dotted', zorder=0)
axs.set_yticks(np.arange(0, 10, 4))
axs.set_title("(c)", fontsize=12, y=-0.33)
axs =fig.add_subplot(gs[0, 3])
plt.bar([i for i in range(5)],WSF, width = barWidth, color = colors[3], edgecolor = 'black',capsize=15)
axs.set_axisbelow(True)
axs.set_xticks([0,1,2,3,4])
axs.set_xticklabels(REGIONS,rotation=15,fontsize=12)
axs.set_ylabel( "Water Scarcity Factor", fontsize=13,labelpad=0)#, y=0.4)
axs.tick_params(labelsize=13,axis='y')
axs.grid(which='major', axis='y', ls='dotted', zorder=0)
axs.set_title("(d)", fontsize=12, y=-0.33)
axs.set_yticks(np.arange(0, 0.9, 0.4))
FONTSIZE = 12
X_Lable = "Months of 2023 (Oregon, USA)"
gs2 = GridSpec(1, 1, figure=fig, wspace=0.5, left=1.025, right=1.17)
axs =fig.add_subplot(gs2[0, 0])
axs.tick_params(axis='both', which='major', labelsize=FONTSIZE)
MONTH = [1,2,3,4,5,6,7,8,9,10,11,12]
PUE=1.2
CI1 =[232,213,224,133,49,105,166,235,266,336,252,247]
EWIF1= [3.4,3.3,3.7,4.3,4.8,4.0,3.8,3.8,3.9,2.8,3.4,3.6]
WUE1 = [2.05,2.19,2.62,2.96,3.42,3.75,4.02,4.08,3.79,3.34,2.66,2.0]
WI_REAL1 = [WUE1[i]+PUE*EWIF1[i] for i in range(12)]
ax2 = axs.twinx()
colors = [ '#fdb42f','#4169E1']
axs.plot([i for i in range(12)],CI1, color = colors[0], marker = 'o', label = "CI", linewidth = 2)
ax2.plot([i for i in range(12)],WI_REAL1, color = colors[1], marker = 'v', label = "WI", linewidth = 2)
axs.set_xticks([0,5,11])
axs.set_xticklabels(["Jan.","Jun.","Dec."],fontsize=FONTSIZE)
ax2.tick_params(axis='both', which='major', labelsize=13)
axs.tick_params(axis='both', which='major', labelsize=13)
axs.set_yticks(np.arange(30,550,175))
ax2.set_yticks(np.arange(6,12,2))
axs.set_xlim(-0.3,11.3)
axs.grid(which='major', ls='dotted', zorder=0)
axs.set_ylabel("Carbon Intensity \n(gCO$_2$/kWh)", fontsize=13,labelpad=0)
ax2.set_ylabel("Water Intensity (L/kWh)", fontsize=13,labelpad=0)
axs.set_title("(e)", fontsize=12, y=-0.33)
axs.set_xlim(-0.3,11.3)
ax2.set_xlim(-0.3,11.3)
axs.legend(loc=(0,1), frameon = False ,ncol=5,labels=["Carbon Intensity","Water Intensity"],fontsize=13,columnspacing=0.4,handletextpad =0.2)
ax2.legend(loc=(0,1.1), frameon = False ,ncol=5,labels=["Water Intensity"],fontsize=13,columnspacing=0.4,handletextpad =0.2)
plt.savefig("./motivations/motiv2.pdf",bbox_inches='tight')
plt.show()



#Fig. 3
tol=0.01
with open(f'./motivations/carbon_opt/carbon_{tol+1}.json') as f:
    energy = json.load(f)
carbon_opt_carbon = []
carbon_opt_water = []
water_opt_carbon = []
water_opt_water = []
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        reg = sig[0]
        carbon_opt_carbon.append(sig[1])
with open(f'./motivations/water_opt/water_{tol+1}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        reg = sig[0]
        water_opt_water.append(sig[1])
with open(f'./motivations/water_opt/carbon_{tol+1}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        water_opt_carbon.append(sig[1])
with open(f'./motivations/carbon_opt/water_{tol+1}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        carbon_opt_water.append(sig[1])

carbon_opt1 = [np.mean(carbon_opt_carbon),np.mean(carbon_opt_water)]
water_opt1 = [np.mean(water_opt_carbon),np.mean(water_opt_water)]


tol = 0.1
with open(f'./motivations/carbon_opt/carbon_{tol+1}.json') as f:
    energy = json.load(f)
util1 = {"zurich":0,"madrid":0,"oregon":0,"milan":0,"mumbai":0}
carbon_opt_carbon = []
carbon_opt_water = []
water_opt_carbon = []
water_opt_water = []
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        reg = sig[0]
        util1[reg]+=1
        carbon_opt_carbon.append(sig[1])

util2 = {"zurich":0,"madrid":0,"oregon":0,"milan":0,"mumbai":0}
with open(f'./motivations/water_opt/water_{tol+1}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        reg = sig[0]
        util2[reg]+=1
        water_opt_water.append(sig[1])
with open(f'./motivations/water_opt/carbon_{tol+1}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        water_opt_carbon.append(sig[1])
with open(f'./motivations/carbon_opt/water_{tol+1}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        carbon_opt_water.append(sig[1])

carbon_opt10 = [np.mean(carbon_opt_carbon),np.mean(carbon_opt_water)]
water_opt10 = [np.mean(water_opt_carbon),np.mean(water_opt_water)]


carbon_opt_carbon = []
carbon_opt_water = []
water_opt_carbon = []
water_opt_water = []
tol = 1
with open(f'./motivations/carbon_opt/carbon_{1+tol}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        carbon_opt_carbon.append(sig[1])
with open(f'./motivations/carbon_opt/water_{1+tol}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        carbon_opt_water.append(sig[1])
with open(f'./motivations/water_opt/water_{1+tol}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        water_opt_water.append(sig[1])
with open(f'./motivations/water_opt/carbon_{1+tol}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        water_opt_carbon.append(sig[1])

carbon_opt100 = [np.mean(carbon_opt_carbon),np.mean(carbon_opt_water)]
water_opt100 = [np.mean(water_opt_carbon),np.mean(water_opt_water)]



carbon_opt_carbon = []
carbon_opt_water = []
water_opt_carbon = []
water_opt_water = []
tol = 10
with open(f'./motivations/carbon_opt/carbon_{1+tol}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        carbon_opt_carbon.append(sig[1])
with open(f'./motivations/carbon_opt/water_{1+tol}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        carbon_opt_water.append(sig[1])
with open(f'./motivations/water_opt/water_{1+tol}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        water_opt_water.append(sig[1])
with open(f'./motivations/water_opt/carbon_{1+tol}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        water_opt_carbon.append(sig[1])
carbon_opt1000 = [np.mean(carbon_opt_carbon),np.mean(carbon_opt_water)]
water_opt1000 = [np.mean(water_opt_carbon),np.mean(water_opt_water)]
fig, axs = plt.subplots(nrows=2, ncols=1, gridspec_kw={'hspace': 0.2, 'wspace': 0.25, 'bottom': 0.25, 
                    'top': 0.9, 'right':0.995, 'left':0.15}, figsize=(3.5,3.2),sharex=True)

REGIONS = ["Zurich","Madrid","Oregon","Milan","Mumbai"]
regions = ['zurich','madrid','oregon','milan','mumbai']

for i, ax in enumerate(axs):
    ax.set_xticks(np.arange(5))
    ax.set_xticklabels(REGIONS, fontsize=12.5)
    ax.tick_params(axis='y', labelsize=12.5)
    ax.set_ylabel('Jobs (%)', fontsize=12.5)
    ax.grid(which='major', axis='y', ls='dotted', zorder=-3)

colors = ['#fdb42f', '#4169E1']
axs[0].bar(np.arange(5), [util1[reg]*100/sum(util1.values()) for reg in regions], color="#33ffc4",label='Carbon',width=0.4,edgecolor='black',zorder = 3)
axs[1].bar(np.arange(5), [util2[reg]*100/sum(util2.values()) for reg in regions], color="#33ffc4",label='Water',width=0.4,edgecolor='black',zorder=3)
axs[0].set_yticks(np.arange(0,90,30))
axs[1].set_yticks(np.arange(0,90,30))
axs[1].set_title("(b)", fontsize=12, y=-0.6)
axs[0].text(1.8,47,"Carbon-Greedy-Opt", fontsize=13,color='black')
axs[1].text(1.8,47,"Water-Greedy-Opt", fontsize=13,color='black')
axs[0].set_title("Percentage of Jobs (10% Delay Tolerance)", fontsize=12)
plt.savefig('./motivations/motiv3(1).pdf', format='pdf', bbox_inches='tight')
plt.show()
carbon_opt_carbon = []
carbon_opt_water = []
water_opt_carbon = []
water_opt_water = []
tol = 10
with open(f'./motivations/carbon_opt/carbon_{1+tol}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        carbon_opt_carbon.append(sig[1])
with open(f'./motivations/carbon_opt/water_{1+tol}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        carbon_opt_water.append(sig[1])
with open(f'./motivations/water_opt/water_{1+tol}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        water_opt_water.append(sig[1])
with open(f'./motivations/water_opt/carbon_{1+tol}.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        water_opt_carbon.append(sig[1])
carbon_lst = []
water_lst = []
with open(f'./motivations/base/carbon.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        carbon_lst.append(sig[2])
with open(f'./motivations/base/water.json') as f:
    energy = json.load(f)
for i in range(0,1440):
    onetime = energy[str(i)]
    for sig in onetime:
        water_lst.append(sig[2])
avg_base_carbon = np.mean(carbon_lst)
avg_base_water = np.mean(water_lst)
fig, axs = plt.subplots(nrows=1, ncols=1, gridspec_kw={'hspace': 0.4, 'wspace': 0.1, 'bottom': 0.2, 
                    'top': 0.8, 'right':0.995, 'left':0.17}, figsize=(2.5,2.75), sharey=True)
FONTSIZE =12.5
XLABEL = "Carbon Footprint Saving \n(% saving w.r.t Baseline)"
YLABEL = "Water Footprint Saving \n(% saving w.r.t Baseline)"
axs.set_xlabel(XLABEL, fontsize=FONTSIZE)
axs.set_ylabel(YLABEL, fontsize=FONTSIZE)

carbon_opt1_perc = [100*(avg_base_carbon-carbon_opt1[0])/avg_base_carbon,100*(avg_base_water-carbon_opt1[1])/avg_base_water]
water_opt1_perc = [100*(avg_base_carbon-water_opt1[0])/avg_base_carbon,100*(avg_base_water-water_opt1[1])/avg_base_water]
carbon_opt10_perc = [100*(avg_base_carbon-carbon_opt10[0])/avg_base_carbon,100*(avg_base_water-carbon_opt10[1])/avg_base_water]
water_opt10_perc = [100*(avg_base_carbon-water_opt10[0])/avg_base_carbon,100*(avg_base_water-water_opt10[1])/avg_base_water]
carbon_opt100_perc = [100*(avg_base_carbon-carbon_opt100[0])/avg_base_carbon,100*(avg_base_water-carbon_opt100[1])/avg_base_water]
water_opt100_perc = [100*(avg_base_carbon-water_opt100[0])/avg_base_carbon,100*(avg_base_water-water_opt100[1])/avg_base_water]
carbon_opt1000_perc = [100*(avg_base_carbon-carbon_opt1000[0])/avg_base_carbon,100*(avg_base_water-carbon_opt1000[1])/avg_base_water]
water_opt1000_perc = [100*(avg_base_carbon-water_opt1000[0])/avg_base_carbon,100*(avg_base_water-water_opt1000[1])/avg_base_water]


axs.scatter(carbon_opt1_perc[0],carbon_opt1_perc[1],label='Carbon-Opt', marker='v', s=150, edgecolors="black",color='#7fc97f',zorder=3)
axs.scatter(water_opt1_perc[0],water_opt1_perc[1], label='Water-Opt', marker='s', s=150, edgecolors="black",color="#4682B4",zorder=3)
axs.scatter(carbon_opt10_perc[0],carbon_opt10_perc[1],label='Carbon-Opt', marker='v', s=150, edgecolors="black",color='#7fc97f',zorder=3)
axs.scatter(water_opt10_perc[0],water_opt10_perc[1], label='Water-Opt', marker='s', s=150, edgecolors="black",color="#4682B4",zorder=3)
axs.scatter(carbon_opt100_perc[0],carbon_opt100_perc[1],label='Carbon-Opt', marker='v', s=150, edgecolors="black",color='#7fc97f',zorder=3)
axs.scatter(water_opt100_perc[0],water_opt100_perc[1], label='Water-Opt', marker='s', s=150, edgecolors="black",color="#4682B4",zorder=3)
axs.scatter(carbon_opt1000_perc[0],carbon_opt1000_perc[1],label='Carbon-Opt', marker='v', s=150,edgecolors="black",color='#7fc97f',zorder=-1)
axs.scatter(water_opt1000_perc[0],water_opt1000_perc[1], label='Water-Opt', marker='s', s=150, edgecolors="black",color="#4682B4",zorder=-1)

axs.set_xticks(np.arange(0,55,10))
axs.set_yticks(np.arange(0,40,10))
axs.tick_params(axis='both', which='major', labelsize=FONTSIZE)
axs.grid(which='both', color='lightgrey', ls='dashed', zorder=-2)
axs.text(23,-16,"(a)", fontsize=12,color='black')
axs.legend(loc=(-0.4,1.15), frameon = False ,ncol=5,labels=["Carbon-Greedy-Opt","Water-Greedy-Opt"],fontsize=13,columnspacing=0.4,handletextpad =0.2)
axs.set_title("Different Delay Tolerance", fontsize=12)
plt.savefig("./motivations/motiv3(2).pdf",bbox_inches='tight')
plt.show()