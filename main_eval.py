import numpy as np
import json
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Gill Sans"
plt.rcParams.update({'mathtext.default':  'regular' })
FONTSIZE = 13
import pandas as pd

def fig5():
    tolerance = [0.25,0.5,0.75,1]
    sla = []
    avg_exe = []
    carbon = []
    water = []
    for j in range(len(tolerance)):
        with open(f'./fig5_logs/waterwise/time_{tolerance[j]+1}.json') as f:
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
        with open(f'./fig5_logs/waterwise/carbon_{tolerance[j]+1}.json') as f:
            carbon_data = json.load(f)
        carbon_lst =[]
        for k,v in carbon_data.items():
            if len(v)!=0:
                for i in v:
                    carbon_lst.append(float(i[2]))
        carbon.append(sum(carbon_lst)/len(carbon_lst))
        with open(f'./fig5_logs/waterwise/water_{tolerance[j]+1}.json') as f:
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
        with open(f'./fig5_logs/water_opt/water_{to+1}.json') as f:
            water_opt_water = json.load(f)
        with open(f'./fig5_logs/water_opt/carbon_{to+1}.json') as f:
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
        with open(f'./fig5_logs/carbon_opt/water_{to+1}.json') as f:
            carbon_opt_water = json.load(f)
        with open(f'./fig5_logs/carbon_opt/carbon_{to+1}.json') as f:
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

    with open(f'./fig5_logs/base/carbon.json') as f:
        base_carbon = json.load(f)
    with open(f'./fig5_logs/base/water.json') as f:
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

    fig, axs = plt.subplots(nrows=1, ncols=4, gridspec_kw={'hspace': 0.4, 'wspace': 0.2, 'bottom': 0.2, 
                        'top': 0.8, 'right':0.995, 'left':0.17}, figsize=(7.2,2.3), sharey=True)

    XLABEL = "Carbon Footprint Saving (% saving w.r.t. Baseline)"
    YLABEL = "Water Footprint Saving \n(% saving w.r.t. Baseline)"
    #axs[0].set_xlabel(XLABEL,fontsize=FONTSIZE)
    axs[0].set_ylabel(YLABEL,fontsize=FONTSIZE)
    Ttiles = ['25% Delay Tolerance', '50% Delay Tolerance', '75% Delay Tolerance','100% Delay Tolerance']
    for i,ax in enumerate(axs):
        ax.tick_params(axis='both', which='major', pad=1, labelsize=FONTSIZE)
        ax.grid(which='both', color='lightgrey', ls='dashed', zorder=-2)
        ax.set_title(Ttiles[i], fontsize=12)
    fig.text(0.58, 0.035, XLABEL, ha='center', fontsize=12)
    for i, ax in enumerate(axs):
        base_carbon = base_c[i]
        base_water = base_w[i]
        carbon_opt_sig = [(base_carbon-carbon_opt_carbon_lst[i])*100/base_carbon, (base_water-carbon_opt_water_lst[i])*100/base_water]
        water_opt_sig = [(base_carbon-water_opt_carbon_lst[i])*100/base_carbon, (base_water-water_opt_water_lst[i])*100/base_water]
        my_sig = [(base_c[i]-carbon[i])*100/base_c[i], (base_w[i]-water[i])*100/base_w[i]]
        #my_sig = [(base_c[i]-carbon[i])*100/base_c[i], (base_w[i]-water[i])*100/base_w[i]]
        ax.scatter(carbon_opt_sig[0],carbon_opt_sig[1], label='Carbon-Opt', marker='v', s=150, edgecolors="black",color='#7fc97f',zorder=3)
        ax.scatter(water_opt_sig[0],water_opt_sig[1], label='Water-Opt', marker='s', s=150, edgecolors="black",color="#4682B4",zorder=3)
        ax.scatter(my_sig[0],my_sig[1], label='WaterWise', marker='o', s=150, edgecolors="black",color='#FF69B4',zorder=3)
        ax.set_xlim(10, 40)
        ax.set_xticks(np.arange(10, 50, 10))
        ax.set_ylim(0, 30)
        ax.set_yticks(np.arange(0, 40, 10))

    LABELS = ['Carbon-Greedy-Opt','Water-Greedy-Opt','WaterWise']
    axs[0].legend(loc=(0.2,1.15), frameon = False ,ncol=5,labels=LABELS,fontsize=13,columnspacing=0.4,handletextpad =0.2)
    plt.savefig("./evaluations/fig5.pdf",bbox_inches='tight')
    plt.show()   
    print("Finished generating Fig 5. Check figures in ./evaluations!")
def table2():
    from tabulate import tabulate
    tolerances = [0.25,0.5,0.75,1]
    carbon_opt_avg_exe = []
    carbon_opt_func = []
    for tolerance in tolerances:
        with open(f'./fig5_logs/carbon_opt/time_{1+tolerance}.json') as f:
            data = json.load(f)
        count1 = 0
        count2=0
        list1= []
        for k,v in data.items():
            if len(v)!=0:
                for i in v:
                    list1.append(float(i[2])/float(i[1]))
                    count1+=1
                    if float(i[2])/float(i[1]) >1+tolerance:
                        count2+=1
        carbon_opt_func.append(100*count2/count1)
        carbon_opt_avg_exe.append(np.mean(list1))
    water_opt_avg_exe = []
    water_opt_func = []
    for tolerance in tolerances:
        with open(f'./fig5_logs/water_opt/time_{1+tolerance}.json') as f:
            data = json.load(f)
        count1 = 0
        count2=0
        list1= []
        for k,v in data.items():
            if len(v)!=0:
                for i in v:
                    list1.append(float(i[2])/float(i[1]))
                    count1+=1
                    if float(i[2])/float(i[1]) >1+tolerance:
                        count2+=1
        water_opt_func.append(100*count2/count1)
        water_opt_avg_exe.append(np.mean(list1))
    waterwise_avg_exe = []
    waterwise_func = []
    for tolerance in tolerances:
        with open(f'./fig5_logs/waterwise/time_{1+tolerance}.json') as f:
            data = json.load(f)
        count1 = 0
        count2=0
        list1= []
        for k,v in data.items():
            if len(v)!=0:
                for i in v:
                    list1.append(float(i[3])/float(i[2]))
                    count1+=1
                    if float(i[3])/float(i[2]) >1+tolerance:
                        count2+=1
        waterwise_func.append(100*count2/count1)
        waterwise_avg_exe.append(np.mean(list1))
    data_service_time = {
        "Delay Tolerance": ["25%", "50%", "75%", "100%"],
        "Baseline": ["1×", "1×", "1×", "1×"],
        "Carbon-Greedy-Opt": [f"{carbon_opt_avg_exe[0]}×", f"{1+carbon_opt_avg_exe[1]}×",f"{carbon_opt_avg_exe[2]}×",f"{carbon_opt_avg_exe[3]}×"],
        "Water-Greedy-Opt": [f"{water_opt_avg_exe[0]}×", f"{water_opt_avg_exe[1]}×",f"{water_opt_avg_exe[2]}×",f"{water_opt_avg_exe[3]}×"],
        "WaterWise": [f"{waterwise_avg_exe[0]}×", f"{waterwise_avg_exe[1]}×",f"{waterwise_avg_exe[2]}×",f"{waterwise_avg_exe[3]}×"]
    }

    data_job_violation = {
        "Delay Tolerance": ["25%", "50%", "75%", "100%"],
        "Baseline": ["0%", "0%", "0%", "0%"],
        "Carbon-Greedy-Opt": [f"{carbon_opt_func[0]}%", f"{1+carbon_opt_func[1]}%",f"{carbon_opt_func[2]}%",f"{carbon_opt_func[3]}%"],
        "Water-Greedy-Opt": [f"{water_opt_func[0]}%", f"{water_opt_func[1]}%",f"{water_opt_func[2]}%",f"{water_opt_func[3]}%"],
        "WaterWise": [f"{waterwise_func[0]}%", f"{waterwise_func[1]}%",f"{waterwise_func[2]}%",f"{waterwise_func[3]}%"]
    }
    df_service_time = pd.DataFrame(data_service_time)
    df_job_violation = pd.DataFrame(data_job_violation)
    df_combined = pd.concat(
        [
            df_service_time.set_index("Delay Tolerance"),
            df_job_violation.set_index("Delay Tolerance"),
        ],
        keys=["Service Time (norm. to execution time)", "% Job Violation"],
    )
    print(tabulate(df_combined, headers="keys", tablefmt="grid"))
def fig9():
    #fig 9
    tolerance = [0.25,0.5,0.75,1]
    sla = []
    avg_exe = []
    carbon = []
    water = []
    #compute my tech
    for j in range(len(tolerance)):
        with open(f'./fig9_logs/waterwise/time_{tolerance[j]+1}.json') as f:
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
        with open(f'./fig9_logs/waterwise/carbon_{tolerance[j]+1}.json') as f:
            carbon_data = json.load(f)
        carbon_lst =[]
        for k,v in carbon_data.items():
            if len(v)!=0:
                for i in v:
                    carbon_lst.append(float(i[2]))
        carbon.append(sum(carbon_lst)/len(carbon_lst))
        with open(f'./fig9_logs/waterwise/water_{tolerance[j]+1}.json') as f:
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
        with open(f'./fig9_logs/water_opt/water_{to+1}.json') as f:
            water_opt_water = json.load(f)
        with open(f'./fig9_logs/water_opt/carbon_{to+1}.json') as f:
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
        with open(f'./fig9_logs/carbon_opt/water_{to+1}.json') as f:
            carbon_opt_water = json.load(f)
        with open(f'./fig9_logs/carbon_opt/carbon_{to+1}.json') as f:
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

    with open(f'./fig9_logs/base/carbon.json') as f:
        base_carbon = json.load(f)
    with open(f'./fig9_logs/base/water.json') as f:
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
            
    fig, axs = plt.subplots(nrows=1, ncols=4, gridspec_kw={'hspace': 0.4, 'wspace': 0.2, 'bottom': 0.2, 
                        'top': 0.8, 'right':0.995, 'left':0.17}, figsize=(7.2,2.3), sharey=True)

    XLABEL = "Carbon Footprint Saving (% saving w.r.t. Baseline)"
    YLABEL = "Water Footprint Saving \n(% saving w.r.t. Baseline)"
    #axs[0].set_xlabel(XLABEL,fontsize=FONTSIZE)
    axs[0].set_ylabel(YLABEL,fontsize=FONTSIZE)
    Ttiles = ['25% Delay Tolerance', '50% Delay Tolerance', '75% Delay Tolerance','100% Delay Tolerance']
    for i,ax in enumerate(axs):
        ax.tick_params(axis='both', which='major', pad=1, labelsize=FONTSIZE)
        ax.grid(which='both', color='lightgrey', ls='dashed', zorder=-2)
        ax.set_title(Ttiles[i], fontsize=12)
    fig.text(0.58, 0.035, XLABEL, ha='center', fontsize=12)
    for i, ax in enumerate(axs):
        base_carbon = base_c[i]
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
    axs[0].legend(loc=(0.35,1.15), frameon = False ,ncol=5,labels=LABELS,fontsize=13,columnspacing=0.4,handletextpad =0.2)
    plt.savefig("./evaluations/fig9.pdf",bbox_inches='tight')
    plt.show()
    print("Finished generating Fig 9. Check figures in ./evaluations!")
def fig10():
    def calculate_average(file_path):
        with open(file_path) as f:
            data = json.load(f)
        lst = [
            float(i[2]) 
            for v in data.values() if v 
            for i in v
        ]
        return sum(lst) / len(lst) if lst else 0
    metrics = ["carbon", "water"]
    directories = {
        "least_load": "./other_logs/least_load/",
        "round_robin": "./other_logs/round_robin/",
        "waterwise": "./fig5_logs/waterwise/",
        "base": "./fig5_logs/base/",
    }
    least_load = [calculate_average(f"{directories['least_load']}{metric}.json") for metric in metrics]
    round_robin = [calculate_average(f"{directories['round_robin']}{metric}.json") for metric in metrics]
    waterwise = [calculate_average(f"{directories['waterwise']}{metric}_1.5.json") for metric in metrics]
    base = [calculate_average(f"{directories['base']}{metric}.json") for metric in metrics]
    fig, axs = plt.subplots(nrows=1, ncols=2, gridspec_kw={'hspace': 0.3, 'wspace': 0.3, 'bottom': 0.2, 
                        'top': 0.8, 'right':0.995, 'left':0.17}, figsize=(7,2.5), sharey=True)
    FONT_SIZE = 13
    colors = ['#fdb42f', '#4169E1']

    DATA1 = [(base[0]-round_robin[0])/base[0], (base[0]-least_load[0])/base[0], (base[0]-waterwise[0])/base[0]]
    DATA2 = [(base[1]-round_robin[1])/base[1], (base[1]-least_load[1])/base[1], (base[1]-waterwise[1])/base[1]]
    data1 = [i*100 for i in DATA1]
    data2 = [i*100 for i in DATA2]
    data =[data1, data2]
    # box plot of data
    x = np.arange(3)
    YLABELS = ["Carbon Footprint Saving \n(% saving w.r.t. Baseline)","Water Footprint Saving \n(% saving w.r.t. Baseline)"]
    REGIONS = ["Round-\nRobin","Least-\nLoad","WaterWise"]
    for i, ax in enumerate(axs):
        bars = ax.bar(x,data[i], width=0.6, zorder=3, edgecolor='black', linewidth=1, color=colors[i],label="Keep-alive Carbon")
        ax.set_ylabel(YLABELS[i],fontsize=FONT_SIZE)
        ax.grid(which='both', axis='y', ls='dashed', zorder=0)
        ax.set_xticks(x)
        ax.set_xticklabels(REGIONS,fontsize=12, rotation=0)
        ax.tick_params(axis='y', which='major', pad=1, labelsize=15)

    axs[0].set_yticks(np.arange(0, 40, 10))
    axs[1].set_yticks(np.arange(0, 40, 10))
    plt.savefig("./evaluations/fig10.pdf",bbox_inches='tight')
    plt.show()
    print("Finished generating Fig 10. Check figures in ./evaluations!")
def fig13():
    with open("./fig9_logs/waterwise/overhead_1.5.json", "r") as f:
        data1 = json.load(f)
    with open("./fig5_logs/waterwise/overhead_1.5.json", "r") as f:
        data2 = json.load(f)

    with open("./fig9_logs/waterwise/time_1.5.json", "r") as f:
        time_data1 = json.load(f)
        
    with open("./fig5_logs/waterwise/time_1.5.json", "r") as f:
        time_data2 = json.load(f)
   
    avg_alibaba = []
    regular_avg =[]
    for i in range(24*60*10):
        time = str(i)
        req_lst = time_data1[time]
        time_lst1 = []
        if len(req_lst) == 0:  
            avg_alibaba.append(0)
            continue
        for req in req_lst:
            time_lst1.append(req[-1])
        avg_alibaba.append(np.mean(time_lst1))

    for i in range(24*60*10):
        time = str(i)
        req_lst = time_data2[time]
        time_lst2 = []
        if len(req_lst) == 0:  
            regular_avg.append(0)
            continue
        for req in req_lst:
            time_lst2.append(req[-1])
        regular_avg.append(np.mean(time_lst2))

    assert len(avg_alibaba) == len(data1)
    assert len(regular_avg) == len(data2)

    fig, axs = plt.subplots(nrows=1, ncols=1, gridspec_kw={'hspace': 0.4, 'wspace': 0.4, 'bottom': 0.2, 
                        'top': 0.95, 'right':0.995, 'left':0.25}, figsize=(7.2,1.9))
    plot_data1 = []
    plot_data2 = []
    for i in range(len(data1)):
        if avg_alibaba[i] == 0 or regular_avg[i] == 0:
            plot_data1.append(0)
            plot_data2.append(0)
            continue
        plot_data1.append(100*data1[i]/avg_alibaba[i])
        plot_data2.append(100*data2[i]/regular_avg[i])
        
    #plot
    axs.plot(plot_data1[1650:1650+2*60], label="Alibaba Trace", color="brown")
    axs.plot(plot_data2[1650:1650+2*60], label="Google Trace", color="#008080")
    axs.grid(which='both', axis='both', color='lightgrey', ls='dashed', zorder=0)
    axs.set_xlim(0, 120)
    axs.set_ylim(0, 0.3)
    axs.tick_params(axis='both', which='major', labelsize=13)
    axs.set_xlabel("Time (minutes)", fontsize=FONTSIZE)
    axs.set_ylabel("Decision-making \nOverhead \n(% of average \nexecution time)", fontsize=FONTSIZE)
    axs.legend(loc='upper right', fontsize=FONTSIZE, ncol=2, frameon=False) 
    plt.savefig("./evaluations/fig13.pdf",bbox_inches='tight')
    plt.show()
    print("Finished generating Fig 13. Check figures in ./evaluations!")

def fig11():
    to = 0.5
    with open(f'./util25/water_opt/water_{to+1}.json') as f:
        water_opt_water = json.load(f)
    with open(f'./util25/water_opt/carbon_{to+1}.json') as f:
        water_opt_carbon = json.load(f)
    water_lst =[]
    carbon_lst =[]
    for k,v in water_opt_carbon.items():
        if len(v)!=0:
            for i in v:
                carbon_lst.append(float(i[1]))
    for k,v in water_opt_water.items():
        if len(v)!=0:
            for i in v:
                water_lst.append(float(i[1]))
    water_opt25_water  = np.mean(water_lst)
    water_opt25_carbon = np.mean(carbon_lst)

    with open(f'./util25/carbon_opt/water_{to+1}.json') as f:
        carbon_opt_water = json.load(f)
    with open(f'./util25/carbon_opt/carbon_{to+1}.json') as f:
        carbon_opt_carbon = json.load(f)
    water_lst =[]
    carbon_lst =[]
    for k,v in carbon_opt_carbon.items():
        if len(v)!=0:
            for i in v:
                carbon_lst.append(float(i[1]))
    for k,v in carbon_opt_water.items():
        if len(v)!=0:
            for i in v:
                water_lst.append(float(i[1]))
    carbon_opt25_water  = np.mean(water_lst)
    carbon_opt25_carbon = np.mean(carbon_lst)

    with open(f'./util25/waterwise/water_{to+1}.json') as f:
        water = json.load(f)
    with open(f'./util25/waterwise/carbon_{to+1}.json') as f:
        carbon = json.load(f)
    water_lst =[]
    carbon_lst =[]
    for k,v in carbon.items():
        if len(v)!=0:
            for i in v:
                carbon_lst.append(float(i[2]))
    for k,v in water.items():
        if len(v)!=0:
            for i in v:
                water_lst.append(float(i[2]))
    waterwise25_water  = np.mean(water_lst)
    waterwise25_carbon = np.mean(carbon_lst)


    with open(f'./util25/base/water.json') as f:
        base_water_25 = json.load(f)
    with open(f'./util25/base/carbon.json') as f:
        base_carbon_25 = json.load(f)
    water_lst =[]
    carbon_lst =[]
    for k,v in base_carbon_25.items():
        if len(v)!=0:
            for i in v:
                carbon_lst.append(float(i[2]))
    for k,v in base_water_25.items():
        if len(v)!=0:
            for i in v:
                water_lst.append(float(i[2]))
    base25_water  = np.mean(water_lst)
    base25_carbon = np.mean(carbon_lst)

    with open(f'./util5/water_opt/water_{to+1}.json') as f:
        water_opt_water = json.load(f)
    with open(f'./util5/water_opt/carbon_{to+1}.json') as f:
        water_opt_carbon = json.load(f)
    water_lst =[]
    carbon_lst =[]
    for k,v in water_opt_carbon.items():
        if len(v)!=0:
            for i in v:
                carbon_lst.append(float(i[1]))
    for k,v in water_opt_water.items():
        if len(v)!=0:
            for i in v:
                water_lst.append(float(i[1]))
    water_opt5_water  = np.mean(water_lst)
    water_opt5_carbon = np.mean(carbon_lst)

    with open(f'./util5/carbon_opt/water_{to+1}.json') as f:
        carbon_opt_water = json.load(f)
    with open(f'./util5/carbon_opt/carbon_{to+1}.json') as f:
        carbon_opt_carbon = json.load(f)
    water_lst =[]
    carbon_lst =[]
    for k,v in carbon_opt_carbon.items():
        if len(v)!=0:
            for i in v:
                carbon_lst.append(float(i[1]))
    for k,v in carbon_opt_water.items():
        if len(v)!=0:
            for i in v:
                water_lst.append(float(i[1]))
    carbon_opt5_water  = np.mean(water_lst)
    carbon_opt5_carbon = np.mean(carbon_lst)

    with open(f'./util5/waterwise/water_{to+1}.json') as f:
        water = json.load(f)
    with open(f'./util5/waterwise/carbon_{to+1}.json') as f:
        carbon = json.load(f)
    water_lst =[]
    carbon_lst =[]
    for k,v in carbon.items():
        if len(v)!=0:
            for i in v:
                carbon_lst.append(float(i[2]))
    for k,v in water.items():
        if len(v)!=0:
            for i in v:
                water_lst.append(float(i[2]))
    waterwise5_water  = np.mean(water_lst)
    waterwise5_carbon = np.mean(carbon_lst)

    with open(f'./util5/base/water.json') as f:
        base_water_25 = json.load(f)
    with open(f'./util5/base/carbon.json') as f:
        base_carbon_25 = json.load(f)
    water_lst =[]
    carbon_lst =[]
    for k,v in base_carbon_25.items():
        if len(v)!=0:
            for i in v:
                carbon_lst.append(float(i[2]))
    for k,v in base_water_25.items():
        if len(v)!=0:
            for i in v:
                water_lst.append(float(i[2]))
    base5_water  = np.mean(water_lst)
    base5_carbon = np.mean(carbon_lst)

    with open(f'./fig5_logs/water_opt/water_{to+1}.json') as f:
        water_opt_water = json.load(f)
    with open(f'./fig5_logs/water_opt/carbon_{to+1}.json') as f:
        water_opt_carbon = json.load(f)
    water_lst =[]
    carbon_lst =[]
    for k,v in water_opt_carbon.items():
        if len(v)!=0:
            for i in v:
                carbon_lst.append(float(i[1]))
    for k,v in water_opt_water.items():
        if len(v)!=0:
            for i in v:
                water_lst.append(float(i[1]))
    water_opt15_water  = np.mean(water_lst)
    water_opt15_carbon = np.mean(carbon_lst)

    with open(f'./fig5_logs/carbon_opt/water_{to+1}.json') as f:
        carbon_opt_water = json.load(f)
    with open(f'./fig5_logs/carbon_opt/carbon_{to+1}.json') as f:
        carbon_opt_carbon = json.load(f)
    water_lst =[]
    carbon_lst =[]
    for k,v in carbon_opt_carbon.items():
        if len(v)!=0:
            for i in v:
                carbon_lst.append(float(i[1]))
    for k,v in carbon_opt_water.items():
        if len(v)!=0:
            for i in v:
                water_lst.append(float(i[1]))
    carbon_opt15_water  = np.mean(water_lst)
    carbon_opt15_carbon = np.mean(carbon_lst)

    with open(f'./fig5_logs/waterwise/water_{to+1}.json') as f:
        water = json.load(f)
    with open(f'./fig5_logs/waterwise/carbon_{to+1}.json') as f:
        carbon = json.load(f)
    water_lst =[]
    carbon_lst =[]
    for k,v in carbon.items():
        if len(v)!=0:
            for i in v:
                carbon_lst.append(float(i[2]))
    for k,v in water.items():
        if len(v)!=0:
            for i in v:
                water_lst.append(float(i[2]))
    waterwise15_water  = np.mean(water_lst)
    waterwise15_carbon = np.mean(carbon_lst)

    with open(f'./fig5_logs/base/water.json') as f:
        base_water_25 = json.load(f)
    with open(f'./fig5_logs/base/carbon.json') as f:
        base_carbon_25 = json.load(f)
    water_lst =[]
    carbon_lst =[]
    for k,v in base_carbon_25.items():
        if len(v)!=0:
            for i in v:
                carbon_lst.append(float(i[2]))
    for k,v in base_water_25.items():
        if len(v)!=0:
            for i in v:
                water_lst.append(float(i[2]))
    base15_water  = np.mean(water_lst)
    base15_carbon = np.mean(carbon_lst)
    fig, axs = plt.subplots(nrows=1, ncols=3, gridspec_kw={'hspace': 0.4, 'wspace': 0.2, 'bottom': 0.2, 
                    'top': 0.8, 'right':0.995, 'left':0.17}, figsize=(7,2), sharey=True)

    XLABEL = "Carbon Footprint Saving (% saving w.r.t. Baseline)"
    YLABEL = "Water Footprint Saving \n(% saving w.r.t. Baseline)"
    #axs[0].set_xlabel(XLABEL,fontsize=FONTSIZE)
    axs[0].set_ylabel(YLABEL,fontsize=FONTSIZE)
    Ttiles = ['5% Avergae Utilization', "15% Average Utilization",'25% Average Utilization']
    base_c = [base5_carbon, base15_carbon, base25_carbon]
    base_w = [base5_water, base15_water, base25_water]
    carbon_opt_carbon_lst = [carbon_opt5_carbon, carbon_opt15_carbon, carbon_opt25_carbon]
    carbon_opt_water_lst = [carbon_opt5_water, carbon_opt15_water, carbon_opt25_water]
    water_opt_carbon_lst = [water_opt5_carbon, water_opt15_carbon, water_opt25_carbon]
    water_opt_water_lst = [water_opt5_water, water_opt15_water, water_opt25_water]
    carbon = [waterwise5_carbon, waterwise15_carbon, waterwise25_carbon]
    water = [waterwise5_water, waterwise15_water, waterwise25_water]
    for i,ax in enumerate(axs):
        ax.tick_params(axis='both', which='major', pad=1, labelsize=FONTSIZE)
        ax.grid(which='both', color='lightgrey', ls='dashed', zorder=-2)
        ax.set_title(Ttiles[i], fontsize=12)
    fig.text(0.58, 0.035, XLABEL, ha='center', fontsize=12)
    for i, ax in enumerate(axs):
        base_carbon = base_c[i]
        base_water = base_w[i]
        carbon_opt_sig = [(base_carbon-carbon_opt_carbon_lst[i])*100/base_carbon, (base_water-carbon_opt_water_lst[i])*100/base_water]
        water_opt_sig = [(base_carbon-water_opt_carbon_lst[i])*100/base_carbon, (base_water-water_opt_water_lst[i])*100/base_water]
        my_sig = [(base_c[i]-carbon[i])*100/base_c[i], (base_w[i]-water[i])*100/base_w[i]]
        ax.scatter(carbon_opt_sig[0],carbon_opt_sig[1], label='Carbon-Opt', marker='v', s=150, edgecolors="black",color='#7fc97f',zorder=3)
        ax.scatter(water_opt_sig[0],water_opt_sig[1], label='Water-Opt', marker='s', s=150, edgecolors="black",color="#4682B4",zorder=3)
        ax.scatter(my_sig[0],my_sig[1], label='WaterWise', marker='o', s=150, edgecolors="black",color='#FF69B4',zorder=3)
        ax.set_xlim(10, 40)
        
        ax.set_xticks(np.arange(10, 50, 10))
        ax.set_ylim(0, 30)

    LABELS = ['Carbon-Greedy-Opt','Water-Greedy-Opt','WaterWise']
    axs[0].legend(loc=(0.2,1.15), frameon = False ,ncol=5,labels=LABELS,fontsize=13,columnspacing=0.4,handletextpad =0.2)
    
    plt.savefig("./evaluations/fig11.pdf",bbox_inches='tight')
    plt.show()
    print("Finished generating Fig 11. Check figures in ./evaluations!")





print("Generating Fig.5 ........................")
fig5()
print("****"*7)
print("****"*7)
print("Generating Table 2 ........................")
table2()
print("****"*7)
print("****"*7)
print("Generating Fig.9 ........................")
fig9()
print("****"*7)
print("****"*7)
print("Generating Fig.10 ........................")
fig10()
print("****"*7)
print("****"*7)
print("Generating Fig.11 ........................")
fig11()
print("****"*7)
print("****"*7)
print("Generating Fig.13 ........................")
fig13()
print("****"*7)
print("****"*7)