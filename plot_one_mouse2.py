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
import matplotlib
import matplotlib.mlab as mb
import datetime as dt
import matplotlib.dates as md
import matplotlib.pyplot as plt
import scipy.stats as st

mouse = 'vip492'
fig_title = mouse + ': 10am CNO injection'
path = 'F:/vip_vmpo cohort2_Dec2018/analysis/results/'  

stage1 = 'wake'
stage2 = 'sws'
stage3 = 'rem'

condition1 = 'sal10c'
condition2 = 'cno10c'
#condition3 = 'day27tele'

stamp1 = np.loadtxt('timestamp_' + mouse + '_' + condition1 + '.txt', dtype = '|S19', delimiter = ',') 
stamp2 = np.loadtxt('timestamp_' + mouse + '_' + condition2 + '.txt', dtype = '|S19', delimiter = ',')
#stamp3 = np.loadtxt('timestamp_' + mouse + '_' + condition3 + '.txt', dtype = '|S19', delimiter = ',') 

stamp_lis1 = list(stamp1)
stamp_lis2 = list(stamp2)
#stamp_lis3 = list(stamp3)

timestamp1 = list()
timestamp2 = list()
#timestamp3 = list()

for d in np.arange(stamp1.size):
    timestamp1 = np.append(timestamp1, dt.datetime.strptime(stamp_lis1[d], "%m/%d/%Y %H:%M:%S"))
    
for d in np.arange(stamp2.size):    
    timestamp2 = np.append(timestamp2, dt.datetime.strptime(stamp_lis2[d], "%m/%d/%Y %H:%M:%S"))
 #   timestamp3 = np.append(timestamp3, dt.datetime.strptime(stamp_lis3[d], "%d/%m/%Y %H:%M:%S"))
    
new_time1 = timestamp1
new_time2 = timestamp2
#new_time3 = timestamp3

time_zero1 = dt.datetime.date(timestamp1[0])
time_zero2 = dt.datetime.date(timestamp2[0])
#time_zero3 = dt.datetime.date(timestamp3[0])

for d in np.arange(stamp1.size):
    if dt.datetime.date(timestamp1[d]) == time_zero1:
        new_time1[d] = new_time1[d].replace(day = 1, month =1)
    else:
        new_time1[d] = new_time1[d].replace(day = 2, month = 1)
    
for d in np.arange(stamp2.size):
    if dt.datetime.date(timestamp2[d]) == time_zero2:
        new_time2[d] = new_time2[d].replace(day = 1, month = 1)
    else:
        new_time2[d] = new_time2[d].replace(day = 2, month = 1)
        
#for d in np.arange(stamp3.size):
 #   if dt.datetime.date(timestamp3[d]) == time_zero3:
  #      new_time3[d] = new_time3[d].replace(day = 1, month = 1)
   # else:
    #    new_time3[d] = new_time3[d].replace(day = 2, month = 1)
        
t_diff = md.date2num(timestamp1[1]) - md.date2num(timestamp1[0])

new_time1 = md.date2num(new_time1)
new_time1 = new_time1 + t_diff
new_time1 = md.num2date(new_time1)

new_time2 = md.date2num(new_time2)
new_time2 = new_time2 + t_diff
new_time2 = md.num2date(new_time2)

#new_time3 = md.date2num(new_time3)
#new_time3 = new_time3 + t_diff
#new_time3 = md.num2date(new_time3)


dirList= os.listdir(path)    # insert the path to the directory of interest

for fname in dirList:
    if mouse in fname and stage1 in fname and condition1 in fname:
        wake_sal = np.loadtxt(str(path)+str(fname))
    else:
        if mouse in fname and stage1 in fname and condition2 in fname:
            wake_ivm = np.loadtxt(str(path)+str(fname))
        #else:
 #           if mouse in fname and stage1 in fname and condition3 in fname:
  #              wake_day2 = np.loadtxt(str(path)+str(fname))   
        else:
            if mouse in fname and stage2 in fname and condition1 in fname:
                sws_sal = np.loadtxt(str(path)+str(fname))
            else:
                if mouse in fname and stage2 in fname and condition2 in fname:
                    sws_ivm = np.loadtxt(str(path)+str(fname))
         #           else:
   #                    if mouse in fname and stage2 in fname and condition3 in fname:
    #                        sws_day2 = np.loadtxt(str(path)+str(fname))
                else:
                    if mouse in fname and stage3 in fname and condition1 in fname:
                         rem_sal = np.loadtxt(str(path)+str(fname))
                    else:
                        if mouse in fname and stage3 in fname and condition2 in fname:
                            rem_ivm = np.loadtxt(str(path)+str(fname))
          #                      else:
     #                               if mouse in fname and stage3 in fname and condition3 in fname:
      #                               rem_day2 = np.loadtxt(str(path)+str(fname))
    
#time1 = md.datestr2num(timestamp1)
#t1 = md.num2date(time1)
#time2 = md.datestr2num(timestamp2)
#t2 = md.num2date(time2)
#time3 = md.datestr2num(timestamp3)
#t3 = md.num2date(time3)
    
hours  = md.HourLocator(interval = 2)
hoursFmt = md.DateFormatter('%H')
   
fig = plt.figure(facecolor = 'w')
ax = fig.add_subplot(111)

ax1 = fig.add_subplot(311)
wakesal_fig, = plt.plot(new_time1, wake_sal)
wakeivm_fig, = plt.plot(new_time2, wake_ivm)
#wakeday2_fig, = plt.plot(new_time3, wake_day2)
ax1.xaxis.set_major_locator(hours)
ax1.xaxis.set_major_formatter(hoursFmt)
ax1.spines['top'].set_color('none')
ax1.spines['right'].set_color('none')
ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')
plt.title((stage1), fontsize = 12, x = 0.1, fontweight = 'demi')

ax2 = fig.add_subplot(312)
sws = plt.plot(new_time1, sws_sal, new_time2, sws_ivm)
ax2.xaxis.set_major_locator(hours)
ax2.xaxis.set_major_formatter(hoursFmt)
ax2.spines['top'].set_color('none')
ax2.spines['right'].set_color('none')
ax2.xaxis.set_ticks_position('bottom')
ax2.yaxis.set_ticks_position('left')
plt.title(stage2, fontsize = 12, x = 0.1, fontweight = 'demi')

ax3 = fig.add_subplot(313)
rem = plt.plot(new_time1, rem_sal, new_time2, rem_ivm)
ax3.xaxis.set_major_locator(hours)
ax3.xaxis.set_major_formatter(hoursFmt)
ax3.spines['top'].set_color('none')
ax3.spines['right'].set_color('none')
ax3.xaxis.set_ticks_position('bottom')
ax3.yaxis.set_ticks_position('left')
plt.title(stage3, fontsize = 12, x = 0.1, fontweight = 'demi')

# Turn off axis lines and ticks of the big subplot
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_color('none')
ax.spines['left'].set_color('none')
ax.spines['right'].set_color('none')
ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')

plt.suptitle(fig_title, fontsize = 15, color = 'b')
plt.figlegend((wakesal_fig, wakeivm_fig),(condition1, condition2), loc = 'upper right', fontsize = 10, frameon = False) 
ax.set_xlabel('time (hours)', fontsize = 14)
ax.set_ylabel('% time spent in stage', fontsize = 14)
plt.figtext(0.1, 0.02, str(condition1) + ' at ' + str(stamp1[0]) + ', ' + str(condition2) + ' at ' + str(stamp2[0]))
plt.tight_layout()


#plt.errorbar(t, mean_y1, yerr = st.plt.xlabel('Time of day (hours)')sem(sorted_values, axis = 0), fmt = 'b-')    
#plt.errorbar(t, mean_y2, yerr = st.sem(sorted_values1, axis =0), fmt = 'r') 

  
  
plt.hold
    