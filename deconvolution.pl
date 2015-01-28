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
system("~/Desktop/RE_fMRI/scripts/make_concat.pl > concat.txt");
system("rm -f ${outname}_bucket+tlrc*") unless $testonly;
system("rm -f *irf*.HEAD *irf*.BRIK") unless $testonly;


###############################################################################
#GET deconvolved ROI timeseries
###############################################################################

##average preprocessed data in mask
# $cmd = "3dmaskave -q -mask ~/Desktop/RE_fMRI/data/res/mask_inter_3077_2_136+tlrc -mrange 6 6  all_runs.${subj}+tlrc.HEAD > vta_ts.1D";
# $cmd = "3dmaskave -q -mask ~/Desktop/RE_fMRI/data/res/mask_inter_3077_2_136+tlrc -mrange 6 6  residuals_denuisanced+tlrc.HEAD > vta_ts.1D";

$cmd = "3dmaskave -q -mask ~/Desktop/RE_fMRI/data/res/mask_inter_3077_2_136+tlrc -mrange 6 6  residuals_denuisanced+tlrc.HEAD > /Users/dardenne/Desktop/RE_fMRI/data/vta_deconvolve/${subj}_vta_raw.txt";
system($cmd) unless $testonly;

##transpose
# $cmd = "1dTranspose vta_ts.1D vta_ts_t.1D";
# system($cmd) unless $testonly;
# $cmd = "rm vta_ts.1D";
# system($cmd) unless $testonly;

##detrend data
# $cmd = "3dDetrend -polort 3 -prefix detrended_vta vta_ts_t.1D";
# system($cmd) unless $testonly;
# 
# ##transpose
# $cmd = "1dTranspose detrended_vta.1D detrended_vta_t.1D";
# system($cmd) unless $testonly;
# $cmd = "rm detrended_vta.1D";
# system($cmd) unless $testonly;

# ##upsample data
# $cmd = "1dUpsample 20 detrended_vta_t.1D > detrended_vta_ts.1D";
# system($cmd) unless $testonly;

# ##create HRF
# $cmd = "waver -dt 2 -GAM -inline 1X1 > GammaHR.1D";
# system($cmd) unless $testonly;
# 
# #deconvolve TS
# $cmd = "3dTfitter -RHS vta_ts.1D -FALTUNG GammaHR.1D seed_vta 012 0";
# system($cmd) unless $testonly;

##transpose to remove header
# $cmd = "1dTranspose seed_vta.1D /Users/dardenne/Desktop/RE_fMRI/data/vta_deconvolve/${subj}_vta.txt";
# system($cmd) unless $testonly;

