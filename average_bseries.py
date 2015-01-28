#! /usr/bin/python

import os
import sys
import glob
import string
import subprocess
import numpy as np

PREF_DIR = '/Users/dardenne/Desktop/RE_fMRI'
scripts = 'scripts'
subject_list = os.path.join(PREF_DIR, scripts, 'subject_list.txt')
subjects = []
subj_file = open(subject_list,'r')
for subj in subj_file.readlines():
	subj = subj.strip('\n')
	subj = subj.strip('/')
	subjects.append(subj)
subj_file.close()

conditions = ['ctrl1_bseries+tlrc', 'ctrl2_bseries+tlrc','rep1_bseries+tlrc','rep2_bseries+tlrc']
region_corr = np.zeros((len(subjects),len(conditions)))
mean_vta = np.zeros((len(subjects),len(conditions)))
mean_str = np.zeros((len(subjects),len(conditions)))
slope_vta = np.zeros((len(subjects),len(conditions)))
slope_str = np.zeros((len(subjects),len(conditions)))

outfile = os.path.join(PREF_DIR,'data','vta_striatum_corr.txt')
vta_out = os.path.join(PREF_DIR,'data','vta_mean.txt')
str_out = os.path.join(PREF_DIR,'data','str_mean.txt')
vta_s_out = os.path.join(PREF_DIR,'data','vta_slope.txt')
str_s_out = os.path.join(PREF_DIR,'data','str_slope.txt')

##function gets the average within a mask given a range value index
def get_region(index,data_path):
	index = str(index)
	mask = os.path.join(PREF_DIR, 'data','res','mask_inter_v_2787_2_208+tlrc')
	cmd_str = '3dmaskave -q -mrange ' + index + ' ' + index + ' -mask ' + mask + ' ' + data_path
	proc=subprocess.Popen(cmd_str,shell=True,stdout=subprocess.PIPE, )
	output = proc.communicate()[0]
	output = output.strip(' ')
	output = output.strip('\n')
	output = output.split('\n')
	output = map(float,output)
	return output

#function gets the slope assuming measurements are equally spaced
def linear_slope(beta_series):
	x = np.arange(0,len(beta_series))
	coefficients = np.polyfit(x,beta_series,1)

	print coefficients
	return coefficients[1]
	

for n,subj in enumerate(subjects):
	
	for p,cond in enumerate(conditions):

		data_path = os.path.join(PREF_DIR, 'data',subj,'brik',subj+'.results',cond)
		
		##averaging together bseires for each subject
		# if n==0: #first subjet
		# 			out_file = os.path.join(PREF_DIR, 'data','res')
		# 
		# 			cmd_str = 'cp ' + data_path + '*' + ' ' + out_file + '/'
		# 			print cmd_str
		# 			os.system(cmd_str)

		# if subj=='re04':
		# 	out_file =  os.path.join(PREF_DIR, 'data','res',cond) #output file that gets added to each time
		# 	tmp_out = os.path.join(PREF_DIR, 'data','res',cond) + 'temp' #temp file to be removed because afni doesnt overwrite
		# 	cmd_str = '3dcalc -a ' + data_path + ' -b ' + out_file + ' -expr \'a+b\' -prefix ' + tmp_out
		# 	os.system(cmd_str)
		# 
		# 	#move temporary file to out_file
		# 	cmd_str = 'mv ' + tmp_out + '+tlrc.BRIK ' + out_file + '.BRIK'
		# 	os.system(cmd_str)
		# 
		# 	cmd_str = 'mv ' + tmp_out + '+tlrc.HEAD ' + out_file + '.HEAD'
		# 	os.system(cmd_str)
		
		##get the time series in each mask
		# vta = get_region(6,data_path)
		striatum = get_region(3,data_path)
		
		
		##this is for the hand drawn VTA
		mask = os.path.join(PREF_DIR, 'data','res','vta_draw_v_2787_2_208+tlrc')
		cmd_str = '3dmaskave -q -mask ' + mask + ' ' + data_path
		proc=subprocess.Popen(cmd_str,shell=True,stdout=subprocess.PIPE, )
		output = proc.communicate()[0]
		output = output.strip(' ')
		output = output.strip('\n')
		output = output.split('\n')
		
		vta=map(float,output)
		
		##means
		mean_vta[n,p] = np.mean(vta)
		mean_str[n,p] = np.mean(striatum)
		
		#compile into a single array and correlated
		regions = np.array((vta, striatum))
		corr_coef = np.corrcoef(regions)
		region_corr[n,p] = corr_coef[0,1]
		
		
		##get slopes across task
		slope_vta[n,p] = linear_slope(vta)		
		slope_str[n,p] = linear_slope(striatum)

np.savetxt(outfile,region_corr,delimiter=' ', newline='\n')
np.savetxt(vta_out,mean_vta,delimiter=' ', newline='\n')
np.savetxt(str_out,mean_str,delimiter=' ', newline='\n')
np.savetxt(vta_s_out,slope_vta,delimiter=' ', newline='\n')
np.savetxt(str_s_out,slope_str,delimiter=' ', newline='\n')
			
			
			
print slope_vta
print slope_str
		
	
				
		
		
		


