#! /usr/bin/python

import os
import sys
import glob
import string

##global variables
PREF_DIR = '/Users/dardenne/Desktop/RE_fMRI'
scripts = 'scripts/ians_scripts'
template_file = os.path.join(PREF_DIR, scripts,'templates/average_runs.fsf')
runs = ['run1a','run1b','run2a', 'run2b']

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
	for i in range(0,2):
		test_path = os.path.join(PREF_DIR,'data',subj,'fsl','func','day' + str(i+1) + '_v2.gfeat','cope6.feat','thresh_zstat1.nii.gz')
		if os.path.exists(test_path)==False:
	
			if i==0:
				output_directory = os.path.join(PREF_DIR,'data',subj,'fsl','func','day1_v2')
				temp_file = os.path.join(PREF_DIR, scripts,'fsfs/' + subj + '_day1.fsf')
				input_1 = os.path.join(PREF_DIR,'data',subj,'fsl','func', 'run1a_glm_v2.feat')
				input_2 = os.path.join(PREF_DIR,'data',subj,'fsl','func', 'run2a_glm_v2.feat')			
			else:
				output_directory = os.path.join(PREF_DIR,'data',subj,'fsl','func','day2_v2')
				temp_file = os.path.join(PREF_DIR, scripts,'fsfs/' + subj + '_day2.fsf')
				input_1 = os.path.join(PREF_DIR,'data',subj,'fsl','func', 'run1b_glm_v2.feat')
				input_2 = os.path.join(PREF_DIR,'data',subj,'fsl','func', 'run2b_glm_v2.feat')
			
			##make changes to template file
			fin = open(template_file, 'r')
			fout = open(temp_file, 'w')
			for line in fin:
				line = string.replace(line, 'INPUT1', input_1)
				line = string.replace(line, 'INPUT2', input_2)
				line = string.replace(line, 'OUTPUT_DIR', output_directory)
				fout.write(line)
			fin.close()
			fout.close()

			##run preprocessing
			cmd_str = 'feat ' + temp_file
			os.system(cmd_str)
			print subj  + ' complete!'

