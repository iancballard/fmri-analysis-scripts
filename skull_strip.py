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
	#skull strip
	if os.path.exists(PREF_DIR + '/data/' + subj + '/fsl/anat/anat_brain.nii.gz')==False:
		cmd_str = 'bet ' + PREF_DIR + '/data/' + subj + '/fsl/anat/anat ' + PREF_DIR + '/data/' + subj + '/fsl/anat/anat_brain -R -f 0.5 -g 0'
		os.system(cmd_str)
