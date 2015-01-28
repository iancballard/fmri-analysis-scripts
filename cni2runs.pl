#! /usr/bin/perl
use strict;

opendir(DIR, ".");
my @tarfs = grep(/\.tar/, readdir(DIR));
@tarfs = sort(@tarfs);
closedir(DIR);

if ($#tarfs < 0) {
    print "No tar files found... exiting.\n";
    exit;
}

my $day = 1;

foreach my $tar (@tarfs) {
    print "working on $tar...\n";
    if ($tar =~ /(.*_.*)_nii.tar/) {
        my $pfx = $1;
        print "\tunpacking to $pfx...\n";
        system("tar -xf $tar");

        opendir(DIR, $pfx);
        my @all_f = readdir(DIR);
        my @epis = grep(/.*EPI.*\.nii\.gz/, @all_f);
        @epis = sort(@epis);
        print "\tfound " . ($#epis+1) . " EPIs:\n";
        my @t1 = grep(/FSPGR/, @all_f);
        closedir(DIR);

        if ($#epis > 2) {
            # more than two runs, must be second expt in mix
            # drop last two EPI runs
            print "\tdropping last two EPIs\n";
            pop(@epis);
            pop(@epis);
        }

        if ($#epis % 2 == 0) { # odd number of EPI runs
            #my @s = ();
            #foreach my $e (@epis) {
            #    push(@s, -s "${pfx}/$e");
            #}

            #print "\tEPI sizes: " . join("\t", @s) . "\n";
            #my @s_sort = sort(@s);
            #print "\tkeeping: $s[0]\t$s[1]\n";

            #my @new_epis = ();
            #for (my $i=0; $i<=$#s; $i++) {
            #    if ($s[$i] == $s_sort[0] or $s[$i] == $s_sort[1]) {
            #        push(@new_epis, $epis[$i]);
            #        print "\t\trun " . ($i+1) . "\n";
            #    }
            #}
            #@epis = @new_epis;

            @epis = ($epis[1], $epis[2]);
        }

        print "\t\t".join("\n\t\t", @epis) . "\n";
        print "\tfound t1: $t1[0]\n" if ($t1[0]);

        system("cp $pfx/" . join(" $pfx/", @epis) . " .");
        if ($#t1 >= 0) {
            system("cp $pfx/$t1[0] .");
        }

        print "\tconverting to BRIK\n";
        system("nii2afni.pl $day");

        system("rm -rf $pfx");
        system("rm *.nii.gz");

        if ($day == 1) {
            system("mkdir raw");
            system("mkdir brik");
        }
        system("mv $tar raw/");
        system("mv *.BRIK *.HEAD brik/");
        
        $day++;
    }
}

