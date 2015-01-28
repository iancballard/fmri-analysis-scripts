#! /usr/bin/python

##gets the smoothness of each subject to average and use for 3dClustSim for thresholding
import os
import sys
import glob
import string
import subprocess

PREF_DIR = '/Users/dardenne/Desktop/RE_fMRI' #data directory
scripts = 'scripts' #scripts directory (where subject list is)
subject_list = os.path.join(PREF_DIR, scripts, 'subject_list.txt')
out_f = os.path.join(PREF_DIR,scripts,'vta_roi_habituation.txt')  #output file for all the smoothness data

#read subject file (list of all subids) and put them in subjects
subjects = []
subj_file = open(subject_list,'r')
for subj in subj_file.readlines():
	subj = subj.strip('\n')
	subj = subj.strip('/')
	subjects.append(subj)
subj_file.close()

# vta = os.path.join(PREF_DIR, 'data', 'vta_atlas','VTA_prob+tlrc')
vta = os.path.join(PREF_DIR, 'data','res','vta_draw_v_2787_2_208+tlrc')
#loop through subjects
for subj in subjects:
	
	contrast = os.path.join(PREF_DIR, 'data',subj,'brik',subj+'.results/', 'dayxrep_iter_v_bucket+tlrc[46]') #AFNI data dir for habituation regressor
	
	##Note: this technique is only accurate to a scale factor. Not bothering to figure it out since Betas are in a.u.
	##create a new image that is the product of the probabilistic vta atlas and the contrast
	mask_ave = os.path.join(PREF_DIR, 'data',subj,'brik',subj+'.results/', 'vta_iter_mask')		
	cmd_str = '3dcalc -a ' +  contrast + ' -b ' + vta + ' -expr \'a*b\' -prefix ' + mask_ave
# 		os.system(cmd_str)
	
	
	#afni command
# 	cmd_str = '3dmaskave -mask ' + vta + ' -mrange .975 1 ' + mask_ave + '+tlrc'
 	cmd_str = '3dmaskave -mask ' + vta + ' ' + contrast + '+tlrc'

	print cmd_str
	#nasty subprocess stuff to assign the output of a shell script to a variable
	proc=subprocess.Popen(cmd_str,shell=True,stdout=subprocess.PIPE, )
	output = proc.communicate()[0]
	output = output.strip('\n')
	output = output.split('  ')
	output = output[0].split(' ')
	print output
	output = output[0]
	
# 		compile smoothness data to a text file
	f = open(out_f,'a')
	f.write(str(output))
	f.write('\n')
	f.close()

	print "finished " + subj + "!!"


