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
conditions = ['rep1','rep2','ctrl1','ctrl2','dayxrep']
#read subject file (list of all subids) and put them in subjects
subjects = []
subj_file = open(subject_list,'r')
for subj in subj_file.readlines():
	subj = subj.strip('\n')
	subj = subj.strip('/')
	subjects.append(subj)
subj_file.close()

roi = os.path.join(PREF_DIR, 'data','vs_roi','vs+tlrc')
#loop through subjects
for subj in subjects:
	
	contrast = [os.path.join(PREF_DIR, 'data',subj,'brik',subj+'.results/', 'dayxrep_iter_v_bucket+tlrc[1]') ,#rep`
		os.path.join(PREF_DIR, 'data',subj,'brik',subj+'.results/', 'dayxrep_iter_v_bucket+tlrc[16]') , #rep2
			os.path.join(PREF_DIR, 'data',subj,'brik',subj+'.results/', 'dayxrep_iter_v_bucket+tlrc[22]') , #ctrl1
				os.path.join(PREF_DIR, 'data',subj,'brik',subj+'.results/', 'dayxrep_iter_v_bucket+tlrc[7]') ,#ctrl2
					os.path.join(PREF_DIR, 'data',subj,'brik',subj+'.results/', 'dayxrep_iter_v_bucket+tlrc[37]') ] #dayxrep
	##Note: this technique is only accurate to a scale factor. Not bothering to figure it out since Betas are in a.u.
	##create a new image that is the product of the probabilistic vta atlas and the contrast
	for n, cond in enumerate(conditions):
		print cond
		print contrast[n]
		out_f = os.path.join(PREF_DIR,scripts,'roi_analyses','vs_' + cond + '.txt')  #output file for all the smoothness data
	
		#afni command
	 	cmd_str = '3dmaskave -mask ' + roi + ' ' + contrast[n] + '+tlrc' #left dlpfc

		print cmd_str
		#nasty subprocess stuff to assign the output of a shell script to a variable
		proc=subprocess.Popen(cmd_str,shell=True,stdout=subprocess.PIPE, )
		output = proc.communicate()[0]
		output = output.strip('\n')
		output = output.split('  ')
		output = output[0].split(' ')
		print output
		output = output[0]
	
		#compile data to a text file
		f = open(out_f,'a')
		f.write(str(output))
		f.write('\n')
		f.close()

		print "finished " + subj + "!!"


