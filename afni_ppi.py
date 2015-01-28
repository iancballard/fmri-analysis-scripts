#! /usr/bin/python

import os
import sys
import glob
import string
import subprocess
import numpy as np

PREF_DIR = '/Users/dardenne/Desktop/RE_fMRI/'
scripts = 'scripts'
subject_list = os.path.join(PREF_DIR, scripts, 'subject_list.txt')
subjects = []
subj_file = open(subject_list,'r')
for subj in subj_file.readlines():
	subj = subj.strip('\n')
	subj = subj.strip('/')
	subjects.append(subj)
subj_file.close()

conditions = ['rep1', 'ctrl1','rep2','ctrl2']
runs = ['run1a','run2a','run1b','run2b'] ##order very important!

##create ideal HRF
hrf_file = os.path.join(PREF_DIR,'data','GammaHR.1D')
cmd_str = 'waver -dt 1 -GAM -inline 1@1 > ' + hrf_file
os.system(cmd_str)


##function gets the average within a mask given a range value index. 
def get_region_by_index(data_path,mask,output,index):
	index = str(index)
	cmd_str = '3dmaskave -q -mrange ' + index + ' ' + index + ' -mask ' + mask + ' ' + data_path + ' > ' + output
	os.system(cmd_str)
	ts = read_file(output)
	return ts

def get_region_simple_mask(data_path,mask,output):
	cmd_str = '3dmaskave -q -mask ' + mask + ' ' + data_path + ' > ' + output
	os.system(cmd_str)
	ts = read_file(output)
	return ts
	
##gets contents of simple text file into an array
def read_file(file_name):
	f=open(file_name,'r')
	ts = []
	for line in f:
		ts.append(float(line))
	f.close()
	ts = np.array(ts)
	return ts
	
	
##dictionary mapping run to file handle	
def make_dict_handle(prefix,mode,loop_list):
	run_dict = dict({})
	for i,run in enumerate(loop_list):
		out_path = os.path.join(PREF_DIR,'data',prefix + str(i) + '.1D')
		f = open(out_path,mode)
		run_dict[run] = f
	return run_dict
	
#dictionary mapping run to filename
def make_dict(prefix,loop_list):
	run_dict = dict({})
	for i,run in enumerate(loop_list):
		run_dict[run] = os.path.join(PREF_DIR,'data',prefix + str(i) + '.1D')
	return run_dict
	
	
#delete files
def delete_dict(run_dict,loop_list):
	for i,run in enumerate(loop_list):
		cmd_str = 'rm ' + run_dict[run]
		os.system(cmd_str)
	
#close the files
def close_dict_handle(run_dict,loop_list):
	for i,run in enumerate(loop_list):
		f = run_dict[run]
		f.close()

##takes an ROI TS and a pointer to AFNI's concat file and splits up the TS into runs
def split_roi_by_run(roi,concat):

	##get concat indices into an array	
	f=open(concat,'r')
	for i in f:
		out=i.split(' ')
		indices = map(float,out)
		indices = np.array(indices)
	indices = np.append(indices,len(roi)) ##useful for indexing below	
	
	run_dict = make_dict_handle('Seed','w',runs)
	
	##write runs into separate files
	for i,val in enumerate(roi):
		if i<indices[1] and i>=indices[0]: #run1
			r_index = 0
		elif i<indices[2] and i>=indices[1]: #run2
			r_index = 1
		elif i<indices[3] and i>=indices[2]: #run3
			r_index = 2
		elif i>=indices[3]: #run4
			r_index = 3
		
		f=run_dict[runs[r_index]]
		f.write(str(val))
		f.write(' ')

	close_dict_handle(run_dict,runs)
	
	return indices ##useful for later on in the script	

for n,subj in enumerate(subjects):
	
	if subj!='re04':	
	
		print '\n \n \n \n \n ' + subj + '  ' + str(n) + '\n \n \n \n \n '
	
		##main vars
		concat = os.path.join(PREF_DIR, 'data',subj,'brik',subj+'.results','concat.txt') 
		data_path = os.path.join(PREF_DIR, 'data',subj,'brik',subj+'.results','all_runs.' + subj + '+tlrc.HEAD')		
		
		#holds the average ts, will be deleted
		temp_out = os.path.join(PREF_DIR, 'data',subj,'brik','Seed.1D')

		##this is for the hand edited VTA cluster
		# mask = os.path.join(PREF_DIR, 'data','res','vta_draw_v_2787_2_208+tlrc')
		# ts = get_region_simple_mask(data_path,mask,temp_out)
		
		#this is for the caudate
		index = 3 
		mask = os.path.join(PREF_DIR, 'data','res','mask_inter_v_2787_2_208+tlrc')
		ts = get_region_by_index(data_path,mask,temp_out,index)
		
		##split TS into runs for appropriate detrending
		indices = split_roi_by_run(ts,concat)
		
		##convert indices (beginning of each run) into run lengths in seconds for use later on
		run_len = []
		for i in range(0,len(indices)-1):
			run_len.append( (indices[i+1] - indices[i] ) * 2)
		
		##set up intermediate files because AFNI always wants to write to txt
		run_dict = make_dict('Seed',runs)
		detrended_run_dict = make_dict('detrend',runs)
		transposed_run_dict = make_dict('transposed',runs)
		upsampled_run_dict = make_dict('upsampled',runs)
		fit_run_dict = make_dict('fit',runs)
		t_fit_run_dict = make_dict('t_fit',runs)
		timing_cond_dict = make_dict('timing',conditions)
 		inter_cond_dict = make_dict('inter',conditions)
		conv_cond_dict = make_dict('conv',conditions)
		final_cond_dict = make_dict('final_inter_caudate',conditions)
		
		##get ts info for each run
		raw_ts_cmd = 'cat '
		dec_ts_cmd = 'cat '
		for i,run in enumerate(runs):
		
			##detrend TS for each run
			cmd_str = '3dDetrend -polort 3 -prefix ' + detrended_run_dict[run] + ' ' + run_dict[run]
			os.system(cmd_str)
								
			cmd_str = '1dTranspose ' +  detrended_run_dict[run] + ' ' +  transposed_run_dict[run];
			os.system(cmd_str)
			
			raw_ts_cmd += transposed_run_dict[run] + ' '  #for the whole experiment raw ts
			
			#upsample to 1s
			cmd_str = '1dUpsample 2 ' + transposed_run_dict[run] + ' > '  + upsampled_run_dict[run]
			os.system(cmd_str)
			
			#deconvolve
			cmd_str = '3dTfitter -RHS ' + upsampled_run_dict[run] + ' -FALTUNG ' + hrf_file + ' ' + fit_run_dict[run] + ' 012 0'
 			os.system(cmd_str)
 			
 			##transpose so cat works later on (transpose gets rid of the obnoxious header info)
 			cmd_str = '1dTranspose ' +  fit_run_dict[run] + ' ' +  t_fit_run_dict[run];
			os.system(cmd_str)
			
			dec_ts_cmd += t_fit_run_dict[run] + ' '  #for the whole experiment raw ts


		##concatenate raw ts
		raw_ts_cmd += '> ' + os.path.join(PREF_DIR, 'data',subj,'brik',subj+'.results','raw_caudate_ts.txt')
		os.system(raw_ts_cmd)
		
		##concatenate deconvolved ts
		deconvolved_ts = os.path.join(PREF_DIR, 'data',subj,'brik',subj+'.results','detrended_caudate_ts.txt')
		dec_ts_cmd += '> ' + deconvolved_ts
		os.system(dec_ts_cmd)


		##get interaction regressors
		timing = dict({})
		for cond in conditions:
			
			#get timing vector for each run in appropriate format using timing_tool.py
			cond_file = os.path.join(PREF_DIR, 'data',subj,'brik',subj+'.results', cond + '_input.txt') 
			cmd_str = 'python /usr/local/afni/timing_tool.py -timing ' + cond_file +  ' -timing_to_1D ' + timing_cond_dict[cond] + ' -tr 1 -min_frac .3 -stim_dur 6 -run_len ' + ' '.join(map(str,run_len))
			os.system(cmd_str)
			
			##fix timing vector because AFNI sucks. timing_tool.py gives 1 0 for task/baseline and you need 1 -1
			x = np.loadtxt(timing_cond_dict[cond], delimiter='\n')
			x = ( x * 2 ) - 1 #converts 1 0 into 1 -1

			##save new timing vector
			os.system('rm ' + timing_cond_dict[cond]) #delete old file
			np.savetxt(timing_cond_dict[cond],x,delimiter = '\n',fmt='%i')
				
		##get interaction regressors for each condition
		for i,cond in enumerate(conditions):

			##multiply the stimulus and the ts
			cmd_str = '1deval -a ' + deconvolved_ts + ' -b ' + timing_cond_dict[cond] + ' -expr \'a*b\' > ' + inter_cond_dict[cond]
			os.system(cmd_str)
			
			##convolve
			cmd_str = 'waver -GAM -peak 1 -TR 1 -input ' + inter_cond_dict[cond] + ' -numout ' + str(indices[-1]*2) + ' > ' + conv_cond_dict[cond]
			os.system(cmd_str)
			
			##downsample
			cmd_str = '1dcat ' + conv_cond_dict[cond] + '\'{0..$(2)}\' > ' + final_cond_dict[cond]
			os.system(cmd_str)
			
			##separate regressors for separate days, wants 0s for the alternate day	
			x = np.loadtxt(final_cond_dict[cond], delimiter='\n')
			if cond == 'rep1' or cond == 'ctrl1': ##day 1 					
				x[indices[2]:]=0
			else:
				x[:indices[2]]=0
			np.savetxt(os.path.join(PREF_DIR, 'data',subj,'brik',subj+'.results','caudate_inter' + str(i) + '.txt'),x,delimiter = '\n',fmt='%.8f')
		
		
		#delete intermediate files
		delete_dict(run_dict,runs)
		delete_dict(detrended_run_dict,runs)
		delete_dict(transposed_run_dict,runs)
		delete_dict(upsampled_run_dict,runs)
		delete_dict(fit_run_dict,runs)
 		delete_dict(t_fit_run_dict,runs)
 		delete_dict(timing_cond_dict,conditions)					
 		delete_dict(inter_cond_dict,conditions)		
 		delete_dict(conv_cond_dict,conditions)	
 		delete_dict(final_cond_dict,conditions)	
 		cmd_str = 'rm ' + deconvolved_ts
		os.system(cmd_str)
 		cmd_str = 'rm ' + temp_out
		os.system(cmd_str)
 			
		
		
		
	
				
		
		
		


