#! /usr/bin/python

import os
import sys
import glob
import string

##global variables
PREF_DIR = '/Users/dardenne/Desktop/RE_fMRI'
scripts = 'scripts/ians_scripts'
template_file = os.path.join(PREF_DIR, scripts,'templates/preproc.fsf')
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
	if subj=='re07':#n%2!=0:
		print n
		#skull strip
		if os.path.exists(PREF_DIR + '/data/' + subj + '/fsl/anat/anat_brain.nii.gz')==False:
			cmd_str = 'bet ' + PREF_DIR + '/data/' + subj + '/fsl/anat/anat ' + PREF_DIR + '/data/' + subj + '/fsl/anat/anat_brain -R -f 0.5 -g 0'
			os.system(cmd_str)
	
		##setup preprocessing, run independant stuff
		anatomical = os.path.join(PREF_DIR,'data',subj,'fsl','anat/anat_brain')
		
		#loop through runs
		for run in runs:			
			if run=='run1a':
				output_directory = os.path.join(PREF_DIR,'data',subj,'fsl','func', run)
				temp_file = os.path.join(PREF_DIR, scripts,'fsfs/' + subj + '_' + run + '_preproc.fsf')
				func = os.path.join(PREF_DIR,'data',subj,'fsl','func',run)
				
				##get number of timepoints
				temp_file_ntp = PREF_DIR + '/tmp.txt'
				cmd_str = 'fslinfo ' + func + ' > ' + temp_file_ntp #read fslinfo to a text file
				os.system(cmd_str)
				fin = open(temp_file_ntp,'r')
				for line in fin:
					line = line.strip('\n')
					line = line.split(' ')
					if line[0]=='dim4':
						ntp = line[-1:]
				ntp = str(ntp[0])
				ntp = 'fmri(npts) ' + ntp
				cmd_str = 'rm ' + temp_file_ntp #remove text file
				os.system(cmd_str)
	
				##make changes to template file
				fin = open(template_file, 'r')
				fout = open(temp_file, 'w')
				for line in fin:
					line = string.replace(line, 'OUTPUT_DIR', output_directory)
					line = string.replace(line, 'FULL_ANAT', anatomical)
					line = string.replace(line, 'fmri(npts) 0', ntp)  #hack because FSL wont let me input strings into this box
					line = string.replace(line, 'INPUT_DATA', func)
					fout.write(line)
				fin.close()
				fout.close()

				##run preprocessing
				cmd_str = 'feat ' + temp_file
				os.system(cmd_str)
				print subj + ' ' + run + ' complete!'