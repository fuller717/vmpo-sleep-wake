# -*- coding: utf-8 -*-
"""
Created on Mon Mar 04 14:06:34 2013

@author: avenner
"""
#timestamp = np.genfromtxt('timestamp_' + str(filename), dtype = [('date','|S10'),('time','|S9')])
#timestamp = np.loadtxt('timestamp_hdc104_cno10.txt', dtype = '|S19', delimiter = ',') 

# Programme to plot percent time spent in various sleep stages against time

import os
import numpy as np
import numpy.ma as ma
import matplotlib.mlab as mb
import datetime as dt
import matplotlib.dates as md
import matplotlib.pyplot as plt
import scipy.stats as st


### VARIABLES WE CAN CHANGE
condition1 = 'remAVG'
condition2 = 'sal'
condition3 = 'cno'
timestamp = np.loadtxt('timestamp_vip477_cno10a.txt', dtype = '|S19', delimiter = ',') 
fig_title = '% ' +  condition1 + ' in VMPO(VIP)-M3 mice after ' + condition2 + ' or ' + condition3 + ' injection'
path = 'E:/VMPO Data/vip vmpo m3_sept2019/sleep_wake/results/averages/'  # insert the path to the directory of interest
value_threshold = -1


### MANIPULATING DATA FOR PLOTTING

dirList= os.listdir(path)
filename = []
filename_data = []
file_dict = {}

for fname in dirList:
    if fname.startswith('vip'):
        filename = np.append(filename, fname)

fdata = list(filename)
        
for i in np.arange(filename.size):        
    fdata[i] = np.loadtxt(str(path)+str(filename[i]))
    

for i in np.arange(filename.size):
        file_dict[filename[i]] = fdata[i]

index_keys = np.arange(len(file_dict.keys()))
num_files = []
num_files1 = []
    
for i in np.arange(index_keys.size):
    if condition1 in file_dict.keys()[i] and condition2 in file_dict.keys()[i]:
        num_files = np.append(num_files, 1)
    else:
        if condition1 in file_dict.keys()[i] and condition3 in file_dict.keys()[i]:
            num_files1 = np.append(num_files1, 1)
            
arraylen = np.size(file_dict.values()[0])        

for i in np.arange(index_keys.size):
    if np.size(file_dict.values()[i]) > arraylen:
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
         
q = -1
p = -1
       
for i in np.arange(index_keys.size):
    if condition1 in file_dict.keys()[i] and condition2 in file_dict.keys()[i]:
        q = q + 1
        selected_keys[q] = file_dict.keys()[i] 
        selected_values[q,:] = file_dict.values()[i]
    else:
        if condition1 in file_dict.keys()[i] and condition3 in file_dict.keys()[i]:
            p = p + 1
            selected_keys1[p] = file_dict.keys()[i] 
            selected_values1[p,:] = file_dict.values()[i]
            
sorted_keys = np.sort(selected_keys)
order_index = np.arange(len(num_files))

sorted_keys1 = np.sort(selected_keys1)
order_index1 = np.arange(len(num_files1))
    
for i in np.arange(num_files.size):
    order_index[i] = mb.find(sorted_keys == selected_keys[i])
    
for i in np.arange(num_files1.size):
    order_index1[i] = mb.find(sorted_keys1 == selected_keys1[i])        
        
sorted_values = np.zeros((len(selected_keys), arraylen))
sorted_values1 = np.zeros((len(selected_keys1), arraylen))
    
for i in np.arange(num_files.size):
    sorted_values[order_index[i],:] = selected_values[i,:]    
    
for i in np.arange(num_files1.size):
    sorted_values1[order_index1[i],:] = selected_values1[i,:]  
    
masked_values = ma.masked_equal(sorted_values, value_threshold)   
masked_values1 = ma.masked_equal(sorted_values1, value_threshold) 


### CREATING A STABLE TIMESTAMP (i.e. one in which we can specify the day and month)   
 
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


### PLOTTING THE DATA
#time = dt.datestr2num(timestamp)
#t = dt.num2date(time)
hours  = md.HourLocator(interval = 1)
hoursFmt = md.DateFormatter('%H')
   
mean_y1 = np.mean(masked_values, axis = 0) 
mean_y2 = np.mean(masked_values1, axis = 0)
   
plt.hold
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
control, = plt.plot(new_time, mean_y1, 'b-')
drug, = plt.plot(new_time, mean_y2, 'r')
plt.errorbar(new_time, mean_y1, yerr = st.sem(masked_values, axis = 0), fmt = 'b-')    
plt.errorbar(new_time, mean_y2, yerr = st.sem(masked_values1, axis =0), fmt = 'r') 

ax.xaxis.set_major_locator(hours)
ax.xaxis.set_major_formatter(hoursFmt)
plt.legend((control, drug),(condition2, condition3))
plt.xlabel('Time of day (hours)')
plt.ylabel('% time spent in stage')
plt.ylim(0,110)
plt.title(fig_title)   
  
plt.hold
    
cum_y1 = np.cumsum(masked_values, axis = 1)
cum_y2 = np.cumsum(masked_values1, axis = 1)