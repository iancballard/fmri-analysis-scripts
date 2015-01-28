#! /usr/bin/perl

##Runs single trial beta series analysis. Over-writes the bucket each time, but pulls the brik corresponding to
## the single trial to a 4d file.

use Switch;

$testonly = 0;
$outname = "dayxrep_iter_bseries_v";

# get to the right directory
$subj = $ARGV[0];
if ($subj =~ /(.*)\/$/) {
	$subj = $1;
}
print "WORKING ON $subj...\n";
chdir("../data/$subj/brik/$subj.results");
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
    $nr = -1.15; #iteration repeat Since there are 12 trials, this increments up from -1.15?? -- so mean(nr) = 0
    $nc = -1.15; #iteration control

	for ($run=1; $run<=2; $run++) {
		open(FIN, "<../../stimTimes/day".$day."_run".$run."_stimTimes.txt") or die "cannot open file $day $run";		
		while ($line = <FIN>) {
			@vals = split(/\s/, $line);
			$t = $vals[1]; #variable hold the timing
            #$r = -1 * ($run * 2 - 3); #I don't thhink this line does anything run1=1 run2=-1

			switch ($vals[0]) { #look through the first line to determine the correct condition 
				case 2 {
                    ;
					# delivery: do nothing
				}

				case 1 {
					push(@{ $vh{"rep".$day} }, $t);
					$nr += .1;
				}

				case 4 {
                    ;
					# delivery: do nothing
                }

				case 3 {
					push(@{ $vh{"ctrl".$day} }, $t);
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
foreach $k (keys(%vh)) { #loop through conditions
	my @ev_ar = @{ $vh{$k} }; 
	
	#write the regular event files
	open(fp, ">".$k."_input.txt");
	print fp join(" ", @ev_ar);
	close(fp);
	#system("sed -i 's/^ //g' ".$k."_input.txt");
	
	#write text files for single events and spliced event files
	my $ev_run = 0; #index for run number
	for (my $xi=0; $xi <= $#ev_ar; $xi++) { #loop through the events in each 
		my $x = $ev_ar[$xi]; #assign the event time to x
		$ev_run++ if ($x eq "\n"); #increment the run counter if there is a new line
		next if not ($x =~ /\d/); #skip the loop if not a number
		
		open(fp, ">event_".$k."_".$xi."_input.txt"); #single event file
		my $str = "";
		for (my $i=0; $i<$ev_run; $i++) { $str .= " *\n"; } #add in * for each previous run
		$str .= $x . "\n"; #write the time
		for (my $i=0; $i<=2-$ev_run; $i++) { $str .= " *\n"; } #fill in * for subsequent runs
		print fp $str;
		close(fp);
		
		open(fp, ">".$k."_".$xi."_input.txt"); #spliced file
		my @temp_ar = @ev_ar;
		splice(@temp_ar, $xi, 1); #splice removes an entry at a specified index xi
		print fp join(" ", @temp_ar);
		close(fp);
		#system("sed -i 's/^ //g' ${k}_${xi}_input.txt");
	}
}

###############################################################################
# Generate and run the 3dDeconvolve command(s)
###############################################################################


#loop through all the conditions and events and run 3ddeconvolve
for my $event_type (keys(%vh)) {
	system("rm ${event_type}_bseries*"); #remove the bseries 4d file in case you want to re-run script
	my @event_array = @{ $vh{$event_type} }; #same as k above, each conditions timing files
	for (my $event_num=0; $event_num <= $#event_array; $event_num++) { #same as xi above
		# skip \n and * in event_arrays
		next if not ($event_array[$event_num] =~ /\d/);
	
		# index for number of regressors
		$ir=1;
		# boxcar duration to use for hrf model
		$boxcar = 6;
		
		$cmd = "3dDeconvolve -jobs 3 -input all_runs.${subj}+tlrc.HEAD"; #-jobs 3 runs3 jobs in parallel
		$cmd .= " -concat concat.txt"; #text fule containing the lengths of each run
		$cmd .= " -mask mask_anat.${subj}+tlrc"; #speedup processing by not running for voxels outside of brain
		$cmd .= " -censor censor_${subj}_combined_2.1D"; #remove bad time points
		$cmd .= " -polort 'A' -local_times";  ## choose baseline polynomial order based on length of run
		$cmd .= " -num_stimts NUMSTIMTS"; # NUMSTIMTS: placeholder, switched below
		$cmd .= " -xjpeg glm_matrix_bseries_v.jpg"; #display design

		#add the single event to the command so that it is always run first
		$cmd .= " -stim_label ${ir} event_${event_type}_${event_num}";
		$cmd .= " -stim_times ${ir} event_${event_type}_${event_num}_input.txt";
		$cmd .= " SPMG1'(".$boxcar.")'";
		$ir++;

		# add regressor for each of the variables created and populated above
		for $v (keys(%vh)) {
			$cmd .= " -stim_label ".$ir." ".$v;
			$cmd .= " -stim_times";
			## TODO: make this smarter. perhaps look for \d+\*\d+ in the values?
			## hard to do because "*" used to signal no events in run, would have
			## to loop?
			$cmd .= "_AM1" if ($v =~ /_iter$/); #modulate by AMplitude if iter
			$cmd .= ($v eq $event_type) ? #if we are in the single event condition, use the spliced event file
				" ${ir} ${v}_${event_num}_input.txt" :
				" ${ir} ${v}_input.txt"; #otherwise use the standard event file
				
			$cmd .= " SPMG1'(".$boxcar.")'"; #incrememnt regressor number, textfile with timing, convolve with boxcor
			$ir++;
		}

		# standard: add motion regressors as events of no interest (i.e. stim_base)
		@m_str = qw(roll pitch yaw dS dL dP);
		for ($im=0; $im<=$#m_str; $im++) {
			$cmd .= " -stim_file " .$ir. " motion_demean.1D'[" .$im. "]'";
			$cmd .= " -stim_label " .$ir. " " .$m_str[$im]; 
			$cmd .= " -stim_base " .$ir;
			$ir++; #unless ($im==5);
		}
		
		$cmd .= " -stim_file " .$ir. " ventricle_ts.txt -stim_label " .$ir. " ventricle -stim_base " .$ir;

		$cmd .= " -bucket ${outname}_bucket";

		# swap values for placeholders
		$cmd =~ s/NUMSTIMTS/$ir/;
		$cmd =~ s/NUMGLT/$ig/;
		print $cmd . "\n";
		system($cmd) unless $testonly;
		
		#append the first brik to to a 4d file event_type_bseries. Then remove the bucket to save disk space
		system("3dbucket -aglueto ${event_type}_bseries+tlrc ${outname}_bucket+tlrc'[1]'");
		system("rm -f ${outname}_bucket*+tlrc.*");
	}
}
system("rm *_input.txt"); #delete all the text files we created
