# -*- coding: utf-8 -*-
"""
Created on Fri Mar 01 11:07:54 2013

@author: avenner
"""

# A script to analyse hourly sleep-wake amounts from exported SleepSign files

# Make sure Python is looking in the correct directory for the file
import os
os.chdir('E:/VMPO Data/vip vmpo m3_sept2019/sleep_wake')

# Open SleepSign exported file and extract data in a sensible fashion
import sys
import numpy as np
import matplotlib.pyplot as plt

# Make sure Python is looking in the correct directory for the file

path = 'E:/VMPO Data/vip vmpo m3_sept2019/sleep_wake'
dirList= os.listdir(path)    # insert the path to the directory of interest
filename = []

for filename in dirList:
    if filename.startswith('vip'):

        #filename = 'vip461_sal10a.txt'
        file_output = filename.replace('.txt','')
        export_folder = 'E:/VMPO Data/vip vmpo m3_sept2019/sleep_wake/results/'
        
        input_file = open(filename)
        meta_fh = open('meta_%s' % filename,'w')
        ts_fh   = open('timestamp_%s' % filename,'w')
        stage_fh   = open('frequency_%s' % filename,'w')
        data_fh   = open('data_%s' % filename,'w')
        
        data = False
        
        for line in input_file:
            if data:    
                parts = line.split('\t')
                ts_fh.write("\t".join(parts[0:1]))
                ts_fh.write("\n")
                data_fh.write("\t".join(parts[1:]))
            else:
                meta_fh.write(line)
                if line.startswith('Time'):
                    stage_fh.write("\t".join(line.split('\t')[1:]))
                    stage_fh.close()
                    meta_fh.close()
                    data = True
        
        
        ts_fh.close()
        data_fh.close()
        input_file.close()
        
        # Load sensible data
        data = np.loadtxt('data_'+ str(filename))
        # timestamp = np.genfromtxt('timestamp_' + str(filename), dtype = [('date','|S10'),('time','|S9')])
        # timestamp = np.loadtxt('timestamp_hdc104_cno10.txt', dtype = '|S19', delimiter = ',') 
        # time = matplotlib.dates.datestr2num(timestamp)
        # t = matplotlib.dates.num2date(time)
        
        wake = data[:,0]
        sws = data[:,2]
        rem = data[:,1]
        
        # Save wake, SWS and REM values
        np.savetxt((str(export_folder) + str(file_output) +'_wake'), wake)
        np.savetxt((str(export_folder) + str(file_output) +'_sws'), sws)
        np.savetxt((str(export_folder) + str(file_output) +'_rem'), rem)