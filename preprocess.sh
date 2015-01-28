#! /bin/sh

s=`basename $1`
echo "*******************************"
echo "WORKING ON"
echo "\t$s"
echo "*******************************"
echo

cd $s/brik

# rm proc.*
# rm -rf *.results
# rm tshft*.HEAD tshft*.BRIK
# rm warp*.HEAD warp*.BRIK
# rm frun*.HEAD frun*.BRIK

i=1
for dset in `ls run??+orig.HEAD`; do
	pfx=`echo $dset | sed -e 's/\+orig\.HEAD//'`;
	
	echo "TShifting $dset"
	3dTshift -tpattern alt+z -prefix tshft_$pfx $dset

	echo "Warping $dset"
	3dWarp -prefix warp_tshft_$pfx -deoblique tshft_$dset

	# done with tshft data so delete it
	rm tshft_$pfx*.HEAD tshft_$pfx*.BRIK

	if [ $i -eq 1 ]; then
		master=warp_tshft_$dset
		3dcopy $master frun1	
		i=`expr $i + 1`
	else
		3dresample -master $master -inset warp_tshft_$dset -prefix frun$i
		i=`expr $i + 1`
	fi
done

# done with warped data so delete it
# rm warp_tshft*.HEAD warp_tshft*.BRIK
if [ -f t1_nudge+orig.HEAD ]; then
	t1="t1_nudge+orig"
else
t1="t1+orig"
fi

afni_proc.py -subj_id ${s} \
	-dsets frun?+orig.HEAD \
       	-blocks align volreg blur mask regress \
       	-copy_anat $t1 \
	-align_opts_aea -edge -giant_move \
	-tlrc_anat \
	-volreg_tlrc_warp \
	-volreg_warp_dxyz 2 \
	-blur_in_automask \
	-regress_censor_motion 1.0 \
	-regress_censor_outliers 0.1 \
    -regress_compute_fitts \
	-out_dir results_noscale

if [-f t1_nudge+orig.HEAD ]; then
sed -i bkp 's/-edge -giant_move.*/-edge \\/g' proc.${s}
fi

./proc.${s} >> '/Users/dardenne/Desktop/RE_fMRI/output.txt'

#  with warped / tshifted data, so delete it
# rm frun*.HEAD frun*.BRIK

~/bin/growl Preprocessing "Done with $s"

cd ../..
