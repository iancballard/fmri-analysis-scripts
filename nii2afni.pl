#! /usr/bin/perl

#system("rm run* t1*");

$day = $ARGV[0];

opendir(DIR, ".");
@fs = grep(/.*EPI.*\.nii\.gz/, readdir(DIR));
@fs = sort(@fs);
closedir(DIR);

@names = ($day . "a", $day . "b");

$i = 0;
foreach $f (@fs) {
	$info = `3dinfo $f 2> /dev/null`;
	if ($info =~ /Number of time steps = (\d+) /)  {
		$nt = $1;
	}
	
	$cmd = "to3d -fim -prefix run$names[$i] -orient RAI -geomparent $f -time:zt 44 $nt 2000 alt+z $f";
	print $cmd . "\n";
	system($cmd);

#	$cmd = "3drefit -xdel 3 -ydel 3 -zdel 3 -keepcen run$names[$i]+orig";
#	print $cmd . "\n";
#	system($cmd);

	
	$i++;
}

if ($day == 1) {
	$t1 = glob("*FSPGR*.nii.gz");
	$cmd = "to3d -orient RAI -geomparent $t1 -anat -prefix t1 $t1";
	print $cmd . "\n";
	system($cmd);
}
