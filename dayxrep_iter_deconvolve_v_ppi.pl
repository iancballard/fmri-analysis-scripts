#! /usr/bin/perl

use Switch;

$testonly = 0;
$outname = "dayxrep_iter_v_caudate_ppi";

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
# Define variables of interest and populate with event info
###############################################################################

# the variables defined here (as strings) will automatically
# be used to create the 3dDeconvolve command with regressors
# given the same labels. so, be careful with names here.
foreach $day (1,2) {
	foreach $stim qw(rep ctrl) {
		# juice delivery
		push(@vars, "${stim}${day}");

		# juice x iter
		push(@vars, "${stim}${day}_iter");
	}
}

# create links to anonymous array references for each variable.
# these arrays will be populated with times that are subsequently
# passed to 3dDeconvolve to construct the regressors.
$vh{$_} = [] foreach(@vars);

@all_day1 = @vh{ grep(/1/,keys(%vh)) };
@all_day2 = @vh{ grep(/2/,keys(%vh)) };
@all = values(%vh);

# this stuff below will be idiosyncratic to the experiment based
# on how events are stored and how you would like regressors formed.
for ($day=1; $day<=2; $day++) { 
    $nr = -1.15; #iteration repeat Since there are 12 trials, this increments up from -1.15??
    $nc = -1.15; #iteration control

	for ($run=1; $run<=2; $run++) {
		open(FIN, "<../../stimTimes/day".$day."_run".$run."_stimTimes.txt") or die "cannot open file $day $run";		
		while ($line = <FIN>) {
			@vals = split(/\s/, $line);
			$t = $vals[1]; #variable hold the timing
            $r = -1 * ($run * 2 - 3); #I don't thhink this line does anything run1=1 run2=-1

			switch ($vals[0]) { #look through the first line to determine the correct condition 
				case 2 {
                    ;
					# delivery: do nothing
									}

				case 1 {
					push(@{ $vh{"rep".$day} }, $t);
					push(@{ $vh{"rep".$day."_iter"} }, $t."*".$nr);
                    $nr += .1;
				}

				case 4 {
                    ;
					# delivery: do nothing
                }

				case 3 {
					push(@{ $vh{"ctrl".$day} }, $t);
					push(@{ $vh{"ctrl".$day."_iter"} },$t."*".$nc);
                    $nc += .1;
				}
			}
		}
		close(FIN);
	
		if ($day == 1) {
			push(@{ $_ }, "*") for (@all_day2);
		} else {
			push(@{ $_ }, "*") for (@all_day1);
		}

		# adding a \n to the arrays signals 3dDeconvolve
		# that the end of the run has been reached.
		push(@{ $_ }, "\n") for (@all);
	}
}

# dump event times to text files that will be passed to 3dDeconvolve
foreach $k (keys(%vh)) {
	open(fp, ">".$k."_input.txt");
	print fp join(" ", @{ $vh{$k} });
	close(fp);
	system("sed -i 's/^ //g' ".$k."_input.txt");
}

###############################################################################
# Generate and run the 3dDeconvolve command(s)
###############################################################################

# index for number of regressors
$ir=1;
# boxcar duration to use for hrf model
$boxcar = 6;

$cmd = "3dDeconvolve -jobs 3 -input all_runs.${subj}+tlrc.HEAD";
$cmd .= " -concat concat.txt"; #text fule containing the lengths of each run
$cmd .= " -mask mask_anat.${subj}+tlrc"; #speedup processing by not running for voxels outside of brain
$cmd .= " -censor censor_${subj}_combined_2.1D"; #remove bad time points
$cmd .= " -polort 'A' -local_times";  ## choose baseline polynomial order based on length of run
$cmd .= " -num_stimts NUMSTIMTS"; # NUMSTIMTS: placeholder, switched below
# $cmd .= " -errts GLM_residuals"; # residuals output for estimating smoothness
$cmd .= " -xjpeg glm_matrix_v_caudate_ppi.jpg"; #display design

# add regressor for each of the variables created and populated above
for $v (keys(%vh)) {
	$cmd .= " -stim_label ".$ir." ".$v;
	$cmd .= " -stim_times";
	## TODO: make this smarter. perhaps look for \d+\*\d+ in the values?
	## hard to do because "*" used to signal no events in run, would have
	## to loop?
	$cmd .= "_AM1" if ($v =~ /_iter$/); #modulate by AMplitude if iter
	$cmd .= " ".$ir." ".$v."_input.txt SPMG1'(".$boxcar.")'"; #incrememnt regressor number, textfile with timing, convolve with boxcor
	$ir++;
}

##add ppi regressors
$cmd .= " -stim_file " .$ir. " caudate_inter0.txt -stim_label " .$ir. " ppi_rep1 -stim_base " .$ir;
$ir++;
$cmd .= " -stim_file " .$ir. " caudate_inter1.txt -stim_label " .$ir. " ppi_ctrl1 -stim_base " .$ir;
$ir++;
$cmd .= " -stim_file " .$ir. " caudate_inter2.txt -stim_label " .$ir. " ppi_rep2 -stim_base " .$ir;
$ir++;
$cmd .= " -stim_file " .$ir. " caudate_inter3.txt -stim_label " .$ir. " ppi_ctrl2 -stim_base " .$ir;
$ir++;
$cmd .= " -stim_file " .$ir. " raw_caudate_ts.txt -stim_label " .$ir. " ppi_ts -stim_base " .$ir;
$ir++;

# standard: add motion regressors as events of no interest (i.e. stim_base)
@m_str = qw(roll pitch yaw dS dL dP);
for ($im=0; $im<=$#m_str; $im++) {
	$cmd .= " -stim_file " .$ir. " motion_demean.1D'[" .$im. "]'";
	$cmd .= " -stim_label " .$ir. " " .$m_str[$im]; 
	$cmd .= " -stim_base " .$ir;
	$ir++ #unless ($im==5);
}

$cmd .= " -stim_file " .$ir. " ventricle_ts.txt -stim_label " .$ir. " ventricle -stim_base " .$ir;


# index for number of general linear tests
$ig=1;
$cmd .= " -num_glt NUMGLT"; #  NUMGLT: placeholder, switched below

$cmd .= " -glt_label " .$ig. " diff_day1";
$cmd .= " -gltsym 'SYM: +rep1 -ctrl1'";
$ig++;

$cmd .= " -glt_label " .$ig. " main_day1";
$cmd .= " -gltsym 'SYM: .5*rep1 .5*ctrl1'";
$ig++;

$cmd .= " -glt_label " .$ig. " rep_day1";
$cmd .= " -gltsym 'SYM: +rep1'";
$ig++;

$cmd .= " -glt_label " .$ig. " diff_day2";
$cmd .= " -gltsym 'SYM: +rep2 -ctrl2'";
$ig++;

$cmd .= " -glt_label " .$ig. " dayxrep";  ##main contrast of interest
$cmd .= " -gltsym 'SYM: +rep2 -rep1 -ctrl2 +ctrl1'";
$ig++;

$cmd .= " -glt_label " .$ig. " dayxrep_iter";  ##main contrast of interest
$cmd .= " -gltsym 'SYM: +rep2_iter -rep1_iter -ctrl2_iter +ctrl1_iter'";
$ig++;

$cmd .= " -glt_label " .$ig. " dayxrep_ppi";  ##main contrast of interest
$cmd .= " -gltsym 'SYM: +ppi_rep2 -ppi_rep1 -ppi_ctrl2 +ppi_ctrl1'";
$ig++;

$cmd .= " -glt_label " .$ig. " rep2_1";
$cmd .= " -gltsym 'SYM: +rep2 -rep1'";
$ig++;

$cmd .= " -glt_label " .$ig. " main_iter";
$cmd .= " -gltsym 'SYM: .25*rep1_iter .25*rep2_iter .25*ctrl1_iter .25*ctrl2_iter'";
$ig++;

$cmd .= " -glt_label " .$ig. " main_juice";
$cmd .= " -gltsym 'SYM: .25*rep1 .25*rep2 .25*ctrl1 .25*ctrl2'";
$ig++;

$cmd .= " -glt_label " .$ig. " main_ppi";
$cmd .= " -gltsym 'SYM: .25*ppi_rep1 .25*ppi_rep2 .25*ppi_ctrl1 .25*ppi_ctrl2'";

$cmd .= " -fout -tout -bucket ${outname}_bucket";

# swap values for placeholders
$cmd =~ s/NUMSTIMTS/$ir/;
$cmd =~ s/NUMGLT/$ig/;
print $cmd . "\n";
system($cmd) unless $testonly;

# this substitutes events modeled with an hrf to TENT so that irfs are
# estimated. outputs irfs using variable names followed by _irf
# $cmd =~ s/\-stim_times (\d+) (ctrl\d|rep\d)_input\.txt SPMG1'\($boxcar\)'/-stim_times $1 $2_input.txt TENT'\(-2,12,8\)' -iresp $1 $2_irf/g;
# deletes all glts (only care about the ones generated above)
# $cmd =~ s/-num_glt.*/-nobucket/; #-bucket ${outname}_irf_bucket/;
# print "\n\n$cmd\n";
# system($cmd) unless $testonly;

# this tells Sam's cell phone that the script is done
# system("growl $outname \"Done with $subj\"") unless $testonly;
