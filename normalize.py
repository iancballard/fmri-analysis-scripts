#! /usr/bin/python

import os
import sys
import glob
import string

##global variables
PREF_DIR = '/Users/dardenne/Desktop/RE_fMRI'
scripts = 'scripts/ians_scripts'
template_file = os.path.join(PREF_DIR, scripts,'templates/normalize.fsf')
runs = ['run1a', 'run1b', 'run2a','run2b']

##get list of subjects
subject_list = os.path.join(PREF_DIR, scripts, 'subject_list.txt')
subjects = []
subj_file = open(subject_list,'r')
for subj in subj_file.readlines():
	subj = subj.strip('\n')
	subj = subj.strip('/')
	subjects.append(subj)
subj_file.close()

for n,subj in enumerate(subjects):
	if n>16:#n%2!=0:
		#skull strip
		if os.path.exists(PREF_DIR + '/data/' + subj + '/fsl/anat/anat_brain.nii.gz')==False:
			cmd_str = 'bet ' + PREF_DIR + '/data/' + subj + '/fsl/anat/anat ' + PREF_DIR + '/data/' + subj + '/fsl/anat/anat_brain -R -f 0.5 -g 0'
			os.system(cmd_str)
	
		##setup preprocessing, run independant stuff
		anatomical = os.path.join(PREF_DIR,'data',subj,'fsl','anat/anat_brain')
		
		#loop through runs
		for run in runs:			
				output_directory = os.path.join(PREF_DIR,'data',subj,'fsl','func', run)
				temp_file = os.path.join(PREF_DIR, scripts,'fsfs/' + subj + '_' + run + '_norm.fsf')
				func = os.path.join(PREF_DIR,'data',subj,'fsl','func',run + '.feat')
		
	
				##make changes to template file
				fin = open(template_file, 'r')
				fout = open(temp_file, 'w')
				for line in fin:
					line = string.replace(line, 'FULL_ANAT', anatomical)
					line = string.replace(line, 'INPUT_DATA', func)
					fout.write(line)
				fin.close()
				fout.close()

				##run preprocessing
				cmd_str = 'feat ' + temp_file
				os.system(cmd_str)
				print subj + ' ' + run + ' complete!'