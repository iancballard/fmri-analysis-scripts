#! /usr/bin/perl

###############################################################################
# Directions to results from 3dDeconvolve.
# This will probably have to be modified when the script is used on a new 
# analysis.
###############################################################################
# $base = "re??/brik/re??.results";
$base = "re??/brik/re??.results/";

if (not (@f = glob($base."/*_bucket*.HEAD")) ) {
    print "Unable to find any results buckets.\nRunning from wrong directory?\n";
    exit;
}

@unique = ();
for ($i=0; $i<=$#f; $i++) {
    $f[$i] =~ s/.*\/([^\/]+)_bucket.*HEAD$/$1/;
    if (not grep(/$f[$i]/, @unique)) {
        push(@unique, $f[$i]);
        print "$i:\t$f[$i]\n";
    }
}
print"\n Which bucket?  >";

$a = <STDIN>;
$a =~ s/\s$//;
$a = $f[$a];

@f = glob(${base} . "/" . $a . "_bucket*.HEAD");
for ($i=0; $i<=$#f; $i++) {
    if ($f[$i] =~ m/re(07|64)/) {
        splice(@f, $i, 1);
    }
}

$info = `3dinfo -verb $f[0] | grep 'brick.*Coef'`;
%brick_names = {};
while ($info =~ m/brick \#(\d+) \'(\w+)\#0_Coef/g) {
	$brick_names{$1} = $2;

	print "Brick " .$1. ": " .$2. "\n";
}
print "\n Which brick?  >";

$b = <STDIN>;
$b =~ s/\s$//;

s/\+tlrc/\+tlrc'[$b]'/ for(@f);
s/.HEAD$// for(@f);

$prefix = "./res/${a}_$brick_names{$b}_v";

if ( glob(${prefix} . "*") ) {
    print "Output files exist.\n Overwrite?  >";
    $r = <STDIN>;
    if ($r =~ m/[yY]/) {
        system("rm " . $prefix . "*");
    } else {
        print "Exiting...\n";
        exit;
    }
}

# $cmd = "3dttest++ -prefix ./res/${a}_$brick_names{$b} -setA " . join(" ", @f);
$cmd = "3dttest++ -prefix $prefix -setA " . join(" ", @f);

print $cmd . "\n";
`$cmd`;
