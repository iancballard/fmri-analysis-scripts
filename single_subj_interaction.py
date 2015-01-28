#! /usr/bin/python

import os
import sys
import glob
import string

##global variables
PREF_DIR = '/Users/dardenne/Desktop/RE_fMRI'
scripts = 'scripts/ians_scripts'
template_file = os.path.join(PREF_DIR, scripts,'templates/interaction_contrast.fsf')

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
	if n>=16:
		
		output_directory = os.path.join(PREF_DIR,'data',subj,'fsl','func','interaction_fixed')
		temp_file = os.path.join(PREF_DIR, scripts,'fsfs/' + subj + '_interaction.fsf')
		input_1 = os.path.join(PREF_DIR,'data',subj,'fsl','func', 'day1_v2.gfeat/cope1.feat/stats/cope1.nii.gz')
		input_2 = os.path.join(PREF_DIR,'data',subj,'fsl','func', 'day1_v2.gfeat/cope3.feat/stats/cope1.nii.gz')
		input_3 = os.path.join(PREF_DIR,'data',subj,'fsl','func', 'day2_v2.gfeat/cope1.feat/stats/cope1.nii.gz')
		input_4 = os.path.join(PREF_DIR,'data',subj,'fsl','func', 'day2_v2.gfeat/cope3.feat/stats/cope1.nii.gz')
		
		##make changes to template file
		fin = open(template_file, 'r')
		fout = open(temp_file, 'w')
		for line in fin:
			line = string.replace(line, 'INPUT1', input_1)
			line = string.replace(line, 'INPUT2', input_2)
			line = string.replace(line, 'INPUT3', input_3)
			line = string.replace(line, 'INPUT4', input_4)
			line = string.replace(line, 'OUTPUT_DIR', output_directory)
			fout.write(line)
		fin.close()
		fout.close()

		##run preprocessing
		cmd_str = 'feat ' + temp_file
		os.system(cmd_str)
		print subj  + ' complete!'
	
