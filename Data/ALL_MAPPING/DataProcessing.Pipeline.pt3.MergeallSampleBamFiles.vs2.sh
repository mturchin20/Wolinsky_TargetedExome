#!/bin/sh

#######
#
#       Description
#
#
#######

beginTime1=`perl -e 'print time;'`
date1=`date`
PBSnodeFile=`cat $PBS_NODEFILE`
echo ""
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "~~ ${PBS_JOBID} ~ ${date1} ~ ${PBS_O_HOST} ~ ${PBS_O_WORKDIR} ~ ${PBSnodeFile} ~~"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "Working variables:" $fileDirList1
echo ""

#Variables: $fileDirList1 -- directoryoffile,sffFile;directoryoffile,sffFile;etc..

mkdir /tmp/$PBS_JOBID
cd /tmp/$PBS_JOBID

mainDir2=`echo $fileDirList1 | perl -F/\;/ -ane 'chomp(@F); my @vals1 = split(/\|/, $F[0]); print $vals1[0];' | perl -F/ -ane '$F[7] = "PostMerge"; if ($F[9] =~ m/(POOL\w+).*(\d\dRL)/) { $F[9] = $1 . "_" . $2;  print "/", join("/", @F[1..9]);}'`
baseFileN=`echo $mainDir2 | perl -F/ -ane 'print $F[9];'`

echo $mainDir2 $baseFileN

#/home/pg/michaelt/Data/ALL_MAPPING/Pools/PreMerge/mapping_pool_106-124/POOL106-01RL,H9Y2FG202.RL1.sff

mergeBamCommand1=`echo $fileDirList1 | perl -F/\;/ -sane 'chomp(@F); foreach my $file1 (@F) { if ($file1) { my @vals1 = split(/\|/, $file1); my $baseFile1; if ($vals1[1] =~ m/(.*)\.sff/) { $baseFile1 = $1; } my $preGATKbam1 = $baseFile1 . ".QCed.preGATK.QCed.bam"; my $totalFile1 = $vals1[0] . "/" . $preGATKbam1; system("cp -p $totalFile1 /tmp/$pbs_jobid1"); print "I=$preGATKbam1\t"; } }' -- -pbs_jobid1=$PBS_JOBID`

#echo $mergeBamCommand1

/home/shared/software/java/jre1.7.0_09/bin/java -Xmx4g -jar /home/shared/software/picard/picard-tools-1.91/MergeSamFiles.jar $mergeBamCommand1 O=${baseFileN}.QCed.preGATK.QCed.samplesMerged.bam SORT_ORDER=coordinate

mv /tmp/$PBS_JOBID/$baseFileN* $mainDir2/.

rm -r /tmp/$PBS_JOBID

endTime1=`perl -e 'print time;'`
#timeDiff1=$((($endTime1-$beginTime1)/60/60))
timeDiff1=$(($endTime1-$beginTime1))
echo ""
echo "Script run time: $timeDiff1 ($endTime1 - $beginTime1)"
echo ""

