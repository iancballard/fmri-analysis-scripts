#! /usr/bin/python
#new version with makes GLMs with motion parameters, temporal derivatives, and a 4s HRF
import os
import sys
import glob
import string

##global variables
PREF_DIR = '/Users/dardenne/Desktop/RE_fMRI'
scripts = 'scripts/ians_scripts'
template_file = os.path.join(PREF_DIR, scripts,'templates/glm_take2.fsf')
runs = ['run1a','run1b', 'run2a','run2b']


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
	if n>12:
		#loop through runs
		for run in runs:
			output_directory = os.path.join(PREF_DIR,'data',subj,'fsl','func', run + '_glm_v2')
			temp_file = os.path.join(PREF_DIR, scripts,'fsfs/' + subj + '_' + run + '_glm_v2.fsf')
			func = os.path.join(PREF_DIR,'data',subj,'fsl','func',run)
			input_func_feat = os.path.join(PREF_DIR,'data',subj,'fsl','func', run + '.feat/filtered_func_data')
			motion = os.path.join(PREF_DIR,'data',subj,'fsl','func', run + '.feat/mc/prefiltered_func_data_mcf.par')
		
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
			ntp = str(int(ntp[0])-3)  ##subtract the 3 volumes which were removed
			ntp = 'fmri(npts) ' + ntp
			cmd_str = 'rm ' + temp_file_ntp #remove text file
			os.system(cmd_str)
	
	
			##timing files
			repeated = os.path.join(PREF_DIR, scripts, 'onsets_fsl', subj + '_' + run + '_' + 'repeated_4.txt')
			repeated_pmod = os.path.join(PREF_DIR, scripts, 'onsets_fsl', subj + '_' + run + '_' + 'repeated_pmod_4.txt')
			control = os.path.join(PREF_DIR, scripts, 'onsets_fsl', subj + '_' + run + '_' + 'control_4.txt')
			control_pmod = os.path.join(PREF_DIR, scripts, 'onsets_fsl', subj + '_' + run + '_' + 'control_pmod_4.txt')

			##make changes to template file
			fin = open(template_file, 'r')
			fout = open(temp_file, 'w')
			for line in fin:
				line = string.replace(line, 'INPUT_DATA', input_func_feat)
				line = string.replace(line, 'OUTPUT_DIR', output_directory)
				line = string.replace(line, 'fmri(npts) 0', ntp)  #hack because FSL wont let me input strings into this box
				line = string.replace(line, 'SUB_MOTION_SUB', motion)  #hack because FSL wont let me input strings into this box
				
				##timing files
				line = string.replace(line, 'SUB_REPEATED_SUB', repeated)
				line = string.replace(line, 'SUB_REPEATED_PMOD_SUB', repeated_pmod)
				line = string.replace(line, 'SUB_CONTROL_SUB', control)
				line = string.replace(line, 'SUB_CONTROL_PMOD_SUB', control_pmod)
				fout.write(line)
			fin.close()
			fout.close()

			##run preprocessing
			cmd_str = 'feat ' + temp_file
			os.system(cmd_str)
			print subj + ' ' + run + ' complete!'
	