import numpy as np
import json
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Gill Sans"
plt.rcParams.update({'mathtext.default':  'regular' })
FONTSIZE = 13

def fig9_verify(sig_tolerance):
    tolerance = [sig_tolerance]
    
    sla = []
    avg_exe = []
    carbon = []
    water = []
    #compute my tech
    for j in range(len(tolerance)):
        with open(f'./verify_logs/waterwise/time_{tolerance[j]+1}.json') as f:
            data = json.load(f)
        count1 = 0
        count2=0
        list1= []
        for k,v in data.items():
            if len(v)!=0:
                for i in v:
                    list1.append(float(i[4])/float(i[2]))
                    count1+=1
                    if float(i[4])/float(i[2]) >1+tolerance[j]:
                        count2+=1
        sla.append(count2/count1)
        assert count1 == len(list1)
        avg_exe.append(np.mean(list1))
        with open(f'./verify_logs/waterwise/carbon_{tolerance[j]+1}.json') as f:
            carbon_data = json.load(f)
        carbon_lst =[]
        for k,v in carbon_data.items():
            if len(v)!=0:
                for i in v:
                    carbon_lst.append(float(i[2]))
        carbon.append(sum(carbon_lst)/len(carbon_lst))
        with open(f'./verify_logs/waterwise/water_{tolerance[j]+1}.json') as f:
            water_data = json.load(f)
        water_lst =[]
        for k,v in water_data.items():
            if len(v)!=0:
                for i in v:
                    water_lst.append(float(i[2]))
        water.append(sum(water_lst)/len(water_lst))

    water_opt_water_lst = []
    water_opt_carbon_lst = []
    for index, to in enumerate(tolerance):
        with open(f'./verify_logs/water_opt/water_{to+1}.json') as f:
            water_opt_water = json.load(f)
        with open(f'./verify_logs/water_opt/carbon_{to+1}.json') as f:
            water_opt_carbon = json.load(f)
        water_lst =[]
        carbon_lst =[]
        for k,v in water_opt_carbon.items():
            if len(v)!=0:
                for i in v:
                    carbon_lst.append(float(i[1]))
        water_opt_carbon_lst.append(sum(carbon_lst)/len(carbon_lst))
        for k,v in water_opt_water.items():
            if len(v)!=0:
                for i in v:
                    water_lst.append(float(i[1]))

        water_opt_water_lst.append(sum(water_lst)/len(water_lst))
        
    carbon_opt_water_lst = []
    carbon_opt_carbon_lst = []
    for index, to in enumerate(tolerance):
        with open(f'./verify_logs/carbon_opt/water_{to+1}.json') as f:
            carbon_opt_water = json.load(f)
        with open(f'./verify_logs/carbon_opt/carbon_{to+1}.json') as f:
            carbon_opt_carbon = json.load(f)
        water_lst =[]
        carbon_lst =[]
        for k,v in carbon_opt_carbon.items():
            if len(v)!=0:
                for i in v:
                    carbon_lst.append(float(i[1]))
        carbon_opt_carbon_lst.append(sum(carbon_lst)/len(carbon_lst))
        for k,v in carbon_opt_water.items():
            if len(v)!=0:
                for i in v:
                    water_lst.append(float(i[1]))
        carbon_opt_water_lst.append(sum(water_lst)/len(water_lst))

    with open(f'./verify_logs/base/carbon.json') as f:
        base_carbon = json.load(f)
    with open(f'./verify_logs/base/water.json') as f:
        base_water = json.load(f)
    base_carbon_lst = []
    base_water_lst = []
    for k,v in base_carbon.items():
        if len(v)!=0:
            for i in v:
                base_carbon_lst.append(float(i[2]))
    for k,v in base_water.items():
        if len(v)!=0:
            for i in v:
                base_water_lst.append(float(i[2]))
    base_c = [sum(base_carbon_lst)/len(base_carbon_lst)]*5
    base_w = [sum(base_water_lst)/len(base_water_lst)]*5
            
    fig, axs = plt.subplots(nrows=1, ncols=1, gridspec_kw={'hspace': 0.4, 'wspace': 0.2, 'bottom': 0.2, 
                        'top': 0.8, 'right':0.995, 'left':0.17}, figsize=(1.8,2.3), sharey=True)

    XLABEL = "Carbon Footprint Saving (% saving w.r.t. Baseline)"
    YLABEL = "Water Footprint Saving \n(% saving w.r.t. Baseline)"
    #axs[0].set_xlabel(XLABEL,fontsize=FONTSIZE)
    axs.set_ylabel(YLABEL,fontsize=FONTSIZE)
    Ttiles = [f'{sig_tolerance*100}% Delay Tolerance']
    axs.tick_params(axis='both', which='major', pad=1, labelsize=FONTSIZE)
    axs.grid(which='both', color='lightgrey', ls='dashed', zorder=-2)
    axs.set_title(Ttiles[0], fontsize=12)
    fig.text(0.58, 0.035, XLABEL, ha='center', fontsize=12)
    i=0
    ax=axs
    base_carbon = base_c[0]
    base_water = base_w[i]
    carbon_opt_sig = [(base_carbon-carbon_opt_carbon_lst[i])*100/base_carbon, (base_water-carbon_opt_water_lst[i])*100/base_water]
    water_opt_sig = [(base_carbon-water_opt_carbon_lst[i])*100/base_carbon, (base_water-water_opt_water_lst[i])*100/base_water]
    my_sig = [(base_c[i]-carbon[i])*100/base_c[i], (base_w[i]-water[i])*100/base_w[i]]
    ax.scatter(carbon_opt_sig[0],carbon_opt_sig[1], label='Carbon-Opt', marker='v', s=150, edgecolors="black",color='#7fc97f',zorder=3)
    ax.scatter(water_opt_sig[0],water_opt_sig[1], label='Water-Opt', marker='s', s=150, edgecolors="black",color="#4682B4",zorder=3)
    ax.scatter(my_sig[0],my_sig[1], label='WaterWise', marker='o', s=150, edgecolors="black",color='#FF69B4',zorder=3)
    ax.set_xlim(10,25)
    ax.set_xticks(np.arange(10,30, 5))
    ax.set_ylim(5, 20)

    LABELS = ['Carbon-Greedy-Opt','Water-Greedy-Opt','WaterWise']
    axs.legend(loc=(0.35,1.15), frameon = False ,ncol=5,labels=LABELS,fontsize=13,columnspacing=0.4,handletextpad =0.2)
    plt.savefig("./verify_p9.pdf",bbox_inches='tight')
    plt.show()

print("****"*7)
sig_tolerance = 1
fig9_verify(sig_tolerance)