#! /usr/bin/python

import os
import sys
import glob
import string

PREF_DIR = '/Users/dardenne/Desktop/RE_fMRI'
scripts = 'scripts/ians_scripts'
runs = ['run1a', 'run1b', 'run2a','run2b']
subject_list = os.path.join(PREF_DIR, scripts, 'subject_list.txt')

subjects = []
subj_file = open(subject_list,'r')
for subj in subj_file.readlines():
	subj = subj.strip('\n')
	subj = subj.strip('/')
	subjects.append(subj)
subj_file.close()

for subj in subjects:
	if subj == 're07':
		
		anat = os.path.join(PREF_DIR,'data',subj,'fsl','anat','anat')
		cmd_str = 'fslreorient2std ' + anat + ' ' + anat
		os.system(cmd_str)
		
		for run in runs:
			func = os.path.join(PREF_DIR,'data',subj,'fsl','func',run)
			cmd_str = 'fslreorient2std ' + func + ' ' + func
			os.system(cmd_str)
			
		print subj + ' done!'