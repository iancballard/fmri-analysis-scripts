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
final_smooth = os.path.join(PREF_DIR,scripts,'smoothness.txt')  #output file for all the smoothness data

#read subject file (list of all subids) and put them in subjects
subjects = []
subj_file = open(subject_list,'r')
for subj in subj_file.readlines():
	subj = subj.strip('\n')
	subj = subj.strip('/')
	subjects.append(subj)
subj_file.close()

#loop through subjects
for subj in subjects:
	
	if subj=='re04':
		data_path = os.path.join(PREF_DIR, 'data',subj,'brik',subj+'.results/') #AFNI data dir

		#local smoothness file for each subject
		smoothness_file = data_path + 'smoothness.txt'
		if os.path.exists(smoothness_file): #remove old if it exists already
			os.system('rm ' + smoothness_file)
		
		#afni command
		cmd_str = '3dFWHMx -arith -mask ' + data_path + 'mask_anat.' + subj + '+tlrc -dset ' + data_path + 'GLM_residuals+tlrc -out ' + smoothness_file
		print cmd_str
		#nasty subprocess stuff to assign the output of a shell script to a variable
		proc=subprocess.Popen(cmd_str,shell=True,stdout=subprocess.PIPE, )
		output = proc.communicate()[0]
		output = output.strip('\n')
		output = output.split('  ')
	
		# compile smoothness data to a text file
		s_file = open(final_smooth,'a')
		s_file.write(str(float(output[0])))
		s_file.write('\t')
		s_file.write(str(float(output[1])))
		s_file.write('\t')
		s_file.write(str(float(output[2])))
		s_file.write('\n')
		s_file.close()

		print "finished " + subj + "!!"


# 3dClustSim --fwhmxyz 3.2647 3.0611 2.9082 -dxyz 2 2 2 -pthr .05 .02 .01 .005 .001
# Grid: 64x64x32 2.00x2.00x2.00 mm^3 (131072 voxels)
#
# CLUSTER SIZE THRESHOLD(pthr,alpha) in Voxels
# -NN 1  | alpha = Prob(Cluster >= given size)
#  pthr  |  0.100  0.050  0.020  0.010
# ------ | ------ ------ ------ ------
 # 0.050000    82.4   90.3  101.6  109.5
 # 0.020000    34.6   38.0   42.2   46.4
 # 0.010000    22.3   24.4   27.3   29.2
 # 0.005000    15.7   17.4   19.4   21.0
 # 0.001000     8.3    9.2   10.4   11.4

# 3dClustSim -mask master_funcres+tlrc -fwhmxyz 3.2647 3.0611 2.9082 -pthr .05 .02 .01 .005 .001
# Grid: 80x95x75 2.00x2.00x2.00 mm^3 (217604 voxels in mask)
# CLUSTER SIZE THRESHOLD(pthr,alpha) in Voxels
# -NN 1  | alpha = Prob(Cluster >= given size)
#  pthr  |  0.100  0.050  0.020  0.010
# # ------ | ------ ------ ------ ------
#  0.050000    89.8   98.6  111.6  122.8
#  0.020000    36.1   39.8   45.0   48.7
#  0.010000    22.9   25.1   27.8   30.0
#  0.005000    15.8   17.4   19.4   20.9
#  0.001000     8.2    9.1   10.4   11.3