# -*- coding: utf-8 -*-
"""
Created on Wed Oct 03 09:03:54 2018

@author: avenner
"""
#timestamp = np.genfromtxt('timestamp_' + str(filename), dtype = [('date','|S10'),('time','|S9')])
#timestamp = np.loadtxt('timestamp_hdc104_cno10.txt', dtype = '|S19', delimiter = ',') 

# Programme to average multiple trials for wane, NREM and REM and plot percent time spent in various sleep stages against time

import os
import numpy as np
import numpy.ma as ma
import matplotlib.mlab as mb
import datetime as dt
import matplotlib.dates as md
import matplotlib.pyplot as plt
import scipy.stats as st


### VARIABLES WE CAN CHANGE
mouse = 'vip480_cno'
condition1 = 'wake'
condition2 = 'sws'
condition3 = 'rem'
timestamp = np.loadtxt('timestamp_vip461_sal10a.txt', dtype = '|S19', delimiter = ',') 
fig_title = '% sleep stages in ' + mouse + ' after 10am CNO'
path = 'E:/VMPO Data/vip vmpo m3_sept2019/sleep_wake/results/'  # insert the path to the directory of interest
export_folder = 'E:/VMPO Data/vip vmpo m3_sept2019/sleep_wake/results/averages/'
value_threshold = -1


### MANIPULATING DATA FOR PLOTTING

dirList= os.listdir(path)
filename = []
filename_data = []
file_dict = {}

for fname in dirList:
    if mouse in fname:
        filename = np.append(filename, fname)

fdata = list(filename)
        
for i in np.arange(filename.size):        
    fdata[i] = np.loadtxt(str(path)+str(filename[i]))
    

for i in np.arange(filename.size):
        file_dict[filename[i]] = fdata[i]

index_keys = np.arange(len(file_dict.keys()))
num_files = []
num_files1 = []
num_files2= []
    
for i in np.arange(index_keys.size):
    if condition1 in file_dict.keys()[i]:
        num_files = np.append(num_files, 1)
    else:
        if condition2 in file_dict.keys()[i] :
            num_files1 = np.append(num_files1, 1)
        else:
            if condition3 in file_dict.keys()[i] :
                num_files2 = np.append(num_files2, 1)
            
arraylen = 0 
x = 0      

for i in np.arange(index_keys.size):
    if condition1 in file_dict.keys()[i]:
        x = np.size(file_dict.values()[i])
        if x > arraylen:
            arraylen = np.size(file_dict.values()[i])

null = -1
extra = []
app_values = [] 
       
for i in np.arange(index_keys.size):
    if arraylen > np.size(file_dict.values()[i]):
        extra = arraylen - np.size(file_dict.values()[i])
        app_values = np.tile(null, extra)
        file_dict[file_dict.keys()[i]] = np.append(file_dict.values()[i], app_values)
                              
selected_values = np.zeros((len(num_files), arraylen))
selected_keys = range(0, len(num_files)) 

selected_values1 = np.zeros((len(num_files1), arraylen))
selected_keys1 = range(0, len(num_files1))

selected_values2 = np.zeros((len(num_files2), arraylen))
selected_keys2 = range(0, len(num_files2))
         
q = -1
p = -1
r = -1
       
for i in np.arange(index_keys.size):
    if condition1 in file_dict.keys()[i]:
        q = q + 1
        selected_keys[q] = file_dict.keys()[i] 
        selected_values[q,:] = file_dict.values()[i]
    else:
        if condition2 in file_dict.keys()[i]:
            p = p + 1
            selected_keys1[p] = file_dict.keys()[i] 
            selected_values1[p,:] = file_dict.values()[i]
        else:
            if condition3 in file_dict.keys()[i]:
                r = r + 1
                selected_keys2[r] = file_dict.keys()[i] 
                selected_values2[r,:] = file_dict.values()[i]
            
sorted_keys = np.sort(selected_keys)
order_index = np.arange(len(num_files))

sorted_keys1 = np.sort(selected_keys1)
order_index1 = np.arange(len(num_files1))

sorted_keys2 = np.sort(selected_keys2)
order_index2 = np.arange(len(num_files2))
    
for i in np.arange(num_files.size):
    order_index[i] = mb.find(sorted_keys == selected_keys[i])
    
for i in np.arange(num_files1.size):
    order_index1[i] = mb.find(sorted_keys1 == selected_keys1[i])  

for i in np.arange(num_files2.size):
    order_index2[i] = mb.find(sorted_keys2 == selected_keys2[i])      
        
sorted_values = np.zeros((len(selected_keys), arraylen))
sorted_values1 = np.zeros((len(selected_keys1), arraylen))
sorted_values2 = np.zeros((len(selected_keys2), arraylen))
    
for i in np.arange(num_files.size):
    sorted_values[order_index[i],:] = selected_values[i,:]    
    
for i in np.arange(num_files1.size):
    sorted_values1[order_index1[i],:] = selected_values1[i,:]  
    
for i in np.arange(num_files2.size):
    sorted_values2[order_index2[i],:] = selected_values2[i,:]  
    
masked_values = ma.masked_equal(sorted_values, value_threshold)   
masked_values1 = ma.masked_equal(sorted_values1, value_threshold) 
masked_values2 = ma.masked_equal(sorted_values2, value_threshold) 


## CREATING A STABLE TIMESTAMP (i.e. one in which we can specify the day and month)   
 
#==============================================================================
timestamp_lis = list(timestamp) # makes timestamp into a list so we can manipulate it
timestamp_sep = list()  # creates an open list into which we can input values
 
for d in np.arange(timestamp.size): # puts each time point into an ndarray of datetime.datetime objects whereupon each component of the timepoint is separated out
    timestamp_sep = np.append(timestamp_sep, dt.datetime.strptime(timestamp_lis[d], "%m/%d/%Y %H:%M:%S"))
     
new_timestamp = timestamp_sep   #creates a new object that is the same size and type as timestamp_sep
time_zero = dt.datetime.date(timestamp_sep[0]) # gives the date only of the 1st timepoint of timestamp_sep
 
for d in np.arange(timestamp.size): # returns an ndarray of datetime objects which have had their dates changed to the 1st or 2nd day of the month reflecting 1st or 2nd day of recording
    if dt.datetime.date(timestamp_sep[d]) == time_zero:
       new_timestamp[d] = new_timestamp[d].replace(day = 1, month = 1)
    else:
        new_timestamp[d] = new_timestamp[d].replace(day = 2, month = 1)
 
t_diff = md.date2num(timestamp_sep[1]) - md.date2num(timestamp_sep[0])  # gives the time difference of the first 2 timepoints as a float
new_time = md.num2date(md.date2num(timestamp_sep) + t_diff) # adds one time interval to each time, keeps as a datetime object
 
 
 # PLOTTING THE DATA
#time = dt.datestr2num(timestamp)
#t = dt.num2date(time)
hours  = md.HourLocator(interval = 1)
hoursFmt = md.DateFormatter('%H')
 
#new_time = [-1,0,1,2,3,4,5,6,7,8,9,10] 
    
mean_y1 = np.mean(masked_values, axis = 0)
mean_y2 = np.mean(masked_values1, axis = 0)
mean_y3 = np.mean(masked_values2, axis = 0)
 
cum_y1 = np.cumsum(masked_values, axis = 1)
cumy_y2 = np.cumsum(masked_values1, axis = 1)
cumy_y3 = np.cumsum(masked_values2, axis = 1)
   
plt.hold
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
wake, = plt.plot(new_time, mean_y1, 'b-')
sws, = plt.plot(new_time, mean_y2, 'g-')
rem, = plt.plot(new_time, mean_y3, 'r-')
plt.errorbar(new_time, mean_y1, yerr = st.sem(masked_values, axis = 0), fmt = 'b-')    
plt.errorbar(new_time, mean_y2, yerr = st.sem(masked_values1, axis =0), fmt = 'g') 
plt.errorbar(new_time, mean_y3, yerr = st.sem(masked_values2, axis =0), fmt = 'r')

#ax.xaxis.set_major_locator(hours)
#ax.xaxis.set_major_formatter(hoursFmt)
plt.legend((wake,sws,rem),(condition1, condition2, condition3))
plt.xlabel('Time (mins)')
plt.ylabel('% time spent in stage')
plt.title(fig_title)   
  
plt.hold

np.savetxt((str(export_folder) + str(mouse) +'_wakeAVG.txt'), mean_y1)
np.savetxt((str(export_folder) + str(mouse) +'_swsAVG.txt'), mean_y2)
np.savetxt((str(export_folder) + str(mouse) +'_remAVG.txt'), mean_y3)
    