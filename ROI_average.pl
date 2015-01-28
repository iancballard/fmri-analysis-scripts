#! /usr/bin/perl

use Switch;

$testonly = 0;


# get to the right directory
$subj = $ARGV[0];
if ($subj =~ /(.*)\/$/) {
	$subj = $1;
}
print "WORKING ON $subj...\n";
# chdir("../data/$subj/brik/$subj.results");
# system("~/Desktop/RE_fMRI/scripts/make_concat.pl > concat.txt");
# system("rm -f ${outname}_bucket+tlrc*") unless $testonly;
# system("rm -f *irf*.HEAD *irf*.BRIK") unless $testonly;


##get ventricle average of preprocessed data
# $cmd = "3dmaskave -q -mask /Users/dardenne/Desktop/RE_fMRI/data/vta_atlas/ventricle+tlrc all_runs.${subj}+tlrc > ventricle_ts.txt";
# system($cmd) unless $testonly;

#get vta average from probabilistic atlas
#sum of VTA is 222.834 (normalizing constant). Got from 3dmaskave -q -sum -mask VTA_prob+tlrc.HEAD VTA_prob+tlrc.HEAD
# $cmd = "3dcalc -a /Users/dardenne/Desktop/RE_fMRI/data/vta_atlas/vta_prob+tlrc -b dayxrep_iter_v_bucket+tlrc[46] -expr 'a*b' -prefix vta_mask_iter";
# system($cmd) unless $testonly;
# 
# $cmd = "3dmaskave -q -mrange .01 1 -mask /Users/dardenne/Desktop/RE_fMRI/data/vta_atlas/vta_prob+tlrc vta_mask_iter+tlrc >> /Users/dardenne/Desktop/RE_fMRI/data/vta_mask_iter.txt";
# system($cmd) unless $testonly;


#get the average from the striatal subregions
# $cmd = "3dmaskave -q -mrange .9 1.1 -mask /Users/dardenne/Desktop/RE_fMRI/data/striatum/striatum+tlrc dayxrep_iter_v_bucket+tlrc[37] >> /Users/dardenne/Desktop/RE_fMRI/data/striatum/vs.txt";
# system($cmd) unless $testonly;
# $cmd = "3dmaskave -q -mrange 1.9 2.1 -mask /Users/dardenne/Desktop/RE_fMRI/data/striatum/striatum+tlrc dayxrep_iter_v_bucket+tlrc[37] >> /Users/dardenne/Desktop/RE_fMRI/data/striatum/putamen.txt";
# system($cmd) unless $testonly;
# $cmd = "3dmaskave -q -mrange 2.1 3.1 -mask /Users/dardenne/Desktop/RE_fMRI/data/striatum/striatum+tlrc dayxrep_iter_v_bucket+tlrc[37] >> /Users/dardenne/Desktop/RE_fMRI/data/striatum/caudate.txt";
# system($cmd) unless $testonly;

##get average betas from each of the main ROIs
#insula=1, caudate=3, vta=6 but using the edited vta mask: vta_draw_v_2787_2_208+tlrc

## vta
# $cmd = "3dmaskave -q -mask /Users/dardenne/Desktop/RE_fMRI/data/res/vta_draw_v_2787_2_208+tlrc dayxrep_iter_v_bucket+tlrc[37] >> /Users/dardenne/Desktop/RE_fMRI/data/regression_analysis/vta.txt";
# system($cmd) unless $testonly;
# 
# #caudate
# $cmd = "3dmaskave -q -mrange 2.9 3.1 -mask /Users/dardenne/Desktop/RE_fMRI/data/res/mask_inter_v_2787_2_208+tlrc dayxrep_iter_v_bucket+tlrc[37] >> /Users/dardenne/Desktop/RE_fMRI/data/regression_analysis/caudate.txt";
# system($cmd) unless $testonly;
# 
# #insula
# $cmd = "3dmaskave -q -mrange .9 1.1 -mask /Users/dardenne/Desktop/RE_fMRI/data/res/mask_inter_v_2787_2_208+tlrc dayxrep_iter_v_bucket+tlrc[37] >> /Users/dardenne/Desktop/RE_fMRI/data/regression_analysis/insula.txt";
# system($cmd) unless $testonly;

#thalamus(5), HPC(3)
$cmd = "3dmaskave -q -mrange 4.9 5.1 -mask /Users/dardenne/Desktop/RE_fMRI/data/res/mask_inter_v_decline_2787_2_208+tlrc dayxrep_iter_v_bucket+tlrc[40] >> /Users/dardenne/Desktop/RE_fMRI/data/regression_analysis/thalamus.txt";
system($cmd) unless $testonly;
$cmd = "3dmaskave -q -mrange 2.9 3.1 -mask /Users/dardenne/Desktop/RE_fMRI/data/res/mask_inter_v_decline_2787_2_208+tlrc dayxrep_iter_v_bucket+tlrc[40] >> /Users/dardenne/Desktop/RE_fMRI/data/regression_analysis/hpc.txt";
system($cmd) unless $testonly;









