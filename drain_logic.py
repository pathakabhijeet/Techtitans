# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 11:27:43 2024

@author: DELL
"""
import pandas as pd
import matplotlib.pyplot as plt

path = 'C:/Users/DELL/Desktop/hackhive/'
#=======================================
file_name = 'sample'
#=======================================

fd = pd.read_excel(path + file_name+ ".xlsx", sheet_name = 'Sheet2') #190 #MC2ESHRC0PK229406
fd = fd.rename(columns={'FuelLevel':'fuelLevel'})
fd = fd.rename(columns={'HRLFC':'hrlfc'})

#=========================MODULE 01 CODE=======================================

def module_1(df):
    data = df['fuelLevel']
    hrlfc = df['hrlfc']
    
    window_size = 15
    
    # threshold = (20/tankCapacity) * 100
    
    num_windows = len(data) - window_size + 1

    
    ind = []
    std_i = []
    std_f = []
    lats =[]
    longs =[]

    for i in range(num_windows):
        window = data[i:i + window_size]
        window_2 = hrlfc[i:i + window_size]
        lat = df['Latitude']
        long= df['Longitude']
        
        
        
              
        f_3 = window_2[:6].iloc[2] if len(window_2) >= 6 else None
        l_3 = window_2[-6:].iloc[-2] if len(window_2) >= 6 else None
        hrlfc_diff = f_3 - l_3
        hrlfc_p = hrlfc_diff #/ tankCapacity
    
        f_6 = window[:6]
        l_6 = window[-6:]
        m_f_6 = sum(f_6) / len(f_6)
        std_f_6 = (sum((x - m_f_6) ** 2 for x in f_6) / len(f_6)) ** 0.5
    
        m_l_6 = sum(l_6) / len(l_6)
        std_l_6 = (sum((x - m_l_6) ** 2 for x in l_6) / len(l_6)) ** 0.5
    
        upper_bound = m_f_6 - std_f_6
        lower_bound = m_l_6 + std_l_6
    
        diff = upper_bound - lower_bound
        re = diff - hrlfc_p
        
        drain_cond = "D" if re > 7.7 else "N"
        
        if drain_cond == "D":
            ind.append([i, i+15])
            std_i.append(std_f_6)
            std_f.append(std_l_6)
            lats.append(lat)
            longs.append(long)
            
            
        
        f_index = []    
            
        for i in range(len(ind)):
            if i == 0 or ind[i][0] > ind[i-1][1]:
                f_index.append(ind[i])

    # print(filtered_indexes)    
    
    return f_index

def module_2(df):
    
    data = df['fuelLevel']
    hrlfc = df['hrlfc']
    # tnk = tankCapacity/100

    """Take cummulative difference of the hrlfc column"""
    
    df['cum_diff'] = (hrlfc.diff().cumsum())
    
    c_diff = df['cum_diff']
    
    """Now calculate virtual fuel level"""
    
    df['vfl'] = data + c_diff
    
    return df


m1 = module_1(fd)


m2 = module_2(fd)

new_fuel_level = pd.DataFrame(m2)

# new_fuel_level.dropna(inplace=True)
# new_fuel_level.reset_index()
new_fuel_level=new_fuel_level.drop(['fuelLevel'], axis=1)

new_fuel_level.rename(columns={'vfl':'fuelLevel'}, inplace=True)

m3 = module_1(new_fuel_level)

fig, axs = plt.subplots(2, 1, figsize=(10, 12))

# Plot for MODULE_01
axs[0].plot(fd.index, fd['fuelLevel'], label='Fuel Level')
for line in m1:
    axs[0].axvline(x=line[0], color='g', linestyle='--')
    axs[0].axvline(x=line[1], color='r', linestyle='--')
axs[0].set_xlabel('Index')
axs[0].set_ylabel('Fuel Level')
axs[0].set_title('MODULE_01')
axs[0].legend()
axs[0].grid(True)

# Plot for MODULE_02
axs[1].plot(fd.index, fd['fuelLevel'], label='Fuel Level')
for line in m3:
    axs[1].axvline(x=line[0], color='g', linestyle='--')
    axs[1].axvline(x=line[1], color='r', linestyle='--')
axs[1].set_xlabel('Index')
axs[1].set_ylabel('Fuel Level')
axs[1].set_title('MODULE_02')
axs[1].legend()
axs[1].grid(True)

plt.tight_layout()

# plt.savefig(path+str(file_name)+'.png')

plt.show()


# """
# Approach:
    
# Attributes taken: fuelLevel , hrlfc
# window_size = 15
# tankCapacity = 220  
# num_windows = no. of windows to iterate over (wrt fuelLevel Data)
# A loop iterates over each window in the data.
# For each window:
# Extracts a subset of fuelLevel and hrlfc based on the current window.
# Calculates the difference in hrlfc_diff between the third data point from the start and the second-to-last data point.
# Calculates the proportion of hrlfc_diff to tankCapacity :hrlfc_p.
# Calculates the mean and standard deviation for the first and last 6 elements of the fuel level data.
# Defines upper and lower bounds based on the mean and standard deviation.
# Calculates the difference between upper and lower bounds, subtracts hrlfc_p, and determines a drain condition (threshold 7.7).
# Appends the calculated values for each window to the results list.
    
# """
