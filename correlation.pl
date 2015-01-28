#! /usr/bin/perl

###############################################################################
# $base must be set to locate results from 3dDeconvolve.
#
# Result files are assumed to be located in the $base director with the suffix
# _bucket*.HEAD.
#
# $base will probably have to be modified when the script is used on a new 
# analysis.
###############################################################################
$base = "re??/brik/re??.results";
# $base = "re??/brik/results_noscale";
$testonly = 0; # for debugging

@f = glob($base."/*_bucket*.HEAD"); #put all buckets from all subjects into an array f
@unique = ();

# get unique buckets
for ($i=0; $i<=$#f; $i++) { # to get an arrays length use $#
    $f[$i] =~ s/.*\/([^\/]+)_bucket.*HEAD$/$1/;
    if (not grep(/^$f[$i]$/, @unique)) {
        push(@unique, $f[$i]);
        print "$i:\t$f[$i]\n"; #print in form i:	bucket
    }
}

print"\n Which bucket?  >";

#take input and get corresponding bucket and assign it to a
$a = <STDIN>;
$a =~ s/\s$//;
$a = $f[$a]; 

@f = glob(${base} . "/" . $a . "_bucket*.HEAD"); #reassign f to include that bucket from all subjects

#get in bricks in the bucket
$info = `3dinfo -verb $f[0] | grep 'brick.*Coef'`;
%brick_names = {};
while ($info =~ m/brick \#(\d+) \'(\w+)\#0_Coef/g) {
	$brick_names{$1} = $2;
	print "Brick " .$1. ": " .$2. "\n";
}
print "\n Which brick?  >";

#take input and assign brik index to b
$b = <STDIN>;
$b =~ s/\s$//;

s/\+tlrc/\+tlrc'[$b]'/ for(@f);
s/.HEAD$// for(@f);
s/([^\/]+)\/.*/$1 $_/ for (@f);

$prefix = "./res/${a}_$brick_names{$b}_v_inter_dayxrepcov";

print $prefix;

#check if output files exist
if ( glob(${prefix} . "*") and not $testonly ) {
    print "Output files exist.\n Overwrite?  >";
    $r = <STDIN>;
    if ($r =~ m/[yY]/) {
        system("rm " . $prefix . "*");
    } else {
        print "Exiting...\n";
        exit;
    }
}

#run ttest with appropriate files
$cmd = "3dttest++ -prefix $prefix -setA $brick_names{$b} " . join(" ", @f); #join concatenates the strings in @f with the specified delimiter
$cmd .= " -covariates cov_interaction_dayxrep.txt";
print $cmd . "\n";
system($cmd) unless $testonly;
