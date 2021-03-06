#!/bin/bash
#---------------------------------------------------------------------------------------------------
# Download a list of files
#---------------------------------------------------------------------------------------------------

# Read the arguments
echo ""
echo " downloadSample.sh  $*"
echo ""
dataDir=$1;      shift
book=$1;         shift
dataset=$1;      shift
target=$1;       shift
nCopyProcs=$1;   shift
condorOutput=$1; shift
onlyMissing=$1;  shift

DN=`grid-proxy-info -subject`

# Prepare environment
echo " "
echo " Process dataset: $dataset  of book: $book"
echo "   in directory : $dataDir"
echo "   to target    : $target"
echo "   n copy procs : $nCopyProcs"
echo "   condor output: $condorOutput"
echo "   only missing : $onlyMissing"

mkdir -p $condorOutput/$book/$dataset
makedir --exe  $target
makedir --exe  $target/$book
makedir --exe  $target/$book/$dataset
script=`which downloadFiles.sh`

# cleanup our lists and remake a clean one
#echo "rm -f $condorOutput/$book/$dataset/fileList*.$$.txt*"
rm -f $condorOutput/$book/$dataset/fileList*.$$.txt*

# make list of all local files
if [ "`echo $HOSTNAME | grep mit.edu`" != "" ] && \
 ( [ "`echo $dataDir  | grep /castor/cern.ch`" != "" ] || \
   [ "`echo $target   | grep /castor/cern.ch`" != "" ] )
then
  opt="--simple"
else
  opt=""
fi

list $opt $dataDir/$book/$dataset | sort > $condorOutput/$book/$dataset/fileList-all.$$.txt-bak

# make list of all remote files
rm -f $condorOutput/$book/$dataset/fileList-all.$$.txt
touch $condorOutput/$book/$dataset/fileList-all.$$.txt

cat   $condorOutput/$book/$dataset/fileList-all.$$.txt-bak | grep root | sort | \
while read line
do
  size=`echo $line | tr -s ' ' | cut -d ' ' -f 1`
  file=`echo $line | tr -s ' ' | cut -d ' ' -f 2`
  file=`basename $file`
  echo "$size $file" >> $condorOutput/$book/$dataset/fileList-all.$$.txt
done

# make list of all local files
if [ "`echo $HOSTNAME | grep mit.edu`" != "" ] && \
    ( [ "`echo $dataDir | grep /castor/cern.ch`" != "" ] || \
      [ "`echo $target | grep /castor/cern.ch`" != "" ] )
then
  opt="--simple"
else
  opt=""
fi

list $opt $target/$book/$dataset | grep root | sort \
     > $condorOutput/$book/$dataset/fileList-done.$$.txt

diff -y $condorOutput/$book/$dataset/fileList-all.$$.txt  \
        $condorOutput/$book/$dataset/fileList-done.$$.txt > diff.$$
echo ""
echo " Files different in size: "
grep \| diff.$$
echo ""
echo " Files available in all and not done: "
grep \< diff.$$
echo ""
echo " Files done but not listed in all available: "
grep \> diff.$$
echo ""
rm      diff.$$

# make list of missing files
rm -f $condorOutput/$book/$dataset/fileList.$$.txt
touch $condorOutput/$book/$dataset/fileList.$$.txt

cat   $condorOutput/$book/$dataset/fileList-all.$$.txt | grep root | \
while read line
do
  size=`echo $line | tr -s ' ' | cut -d ' ' -f 1`
  file=`echo $line | tr -s ' ' | cut -d ' ' -f 2`
  exists=`grep "$file" $condorOutput/$book/$dataset/fileList-done.$$.txt`
  if [ "$exists" == "" ]
  then
    echo "   -missing-- $file with $size bytes"
    echo "$size $file" >> $condorOutput/$book/$dataset/fileList.$$.txt
  # else
  #   echo "   -exists--- $file with $size bytes - exists"
  else
    # now check that size matches
    test=`grep "$size $file" $condorOutput/$book/$dataset/fileList-done.$$.txt`
    if [ "$test" == "" ]
    then
      if [ "$onlyMissing" == "" ]
      then
        echo "   -fileSize- $exists (remote: $size)"
        echo "$size $file" >> $condorOutput/$book/$dataset/fileList.$$.txt
      fi
    fi
  fi
done

nAll=`wc -l $condorOutput/$book/$dataset/fileList-all.$$.txt | cut -d ' ' -f1`
nMissing=`wc -l $condorOutput/$book/$dataset/fileList.$$.txt | cut -d ' ' -f1`
nDone=`wc -l $condorOutput/$book/$dataset/fileList-done.$$.txt | cut -d ' ' -f1`
echo ""
echo " Download Summary "
echo "   All       $nAll"
echo "   Done      $nDone"
echo "   Missing   $nMissing"
echo ""

# construct our job
nFiles=`wc -l $condorOutput/$book/$dataset/fileList.$$.txt | cut -d ' ' -f1`
if   [ "$nFiles" == "" ] || [ "$nFiles" == "0" ]
then
  echo " "
  echo " No more files to download. EXIT."
  exit 0
elif [ $nFiles -lt $nCopyProcs ]
then
  nCopyProcs=$nFiles
fi
# how many files per job?
nFilesPerJob=$(( $nFiles/$nCopyProcs ))
nFilesTmp=$(( $nFilesPerJob*$nCopyProcs ))
if [ $nFilesPerJob == 1 ] && [ $nFiles -gt $nCopyProcs ]
then
  nFilesPerJob=2
elif [ $nFilesTmp -lt $nFiles ]
then
  nFilesPerJob=$(( $nFilesPerJob+1 ))
fi

echo "   n files to copy: $nFiles"
echo "   n files/proc   : $nFilesPerJob"

i=1
next=1
last=$nFilesPerJob

# make sure condor is properly setup for us
if ! [ -z $CONDOR_LOCATION ]
then
  unset  CONDOR_LOCATION
  export CONDOR_CONFIG=/usr/local/condor/etc/condor_config
fi

# stage in the missing files if it is at CERN
if [ "`echo $dataDir | grep /castor/cern.ch`" != "" ]
then
  echo "  scp $condorOutput/$book/$dataset/fileList.$$.txt  $TICKET_HOLDER@lxplus.cern.ch:"
  scp $condorOutput/$book/$dataset/fileList.$$.txt  $TICKET_HOLDER@lxplus.cern.ch:
  echo "  ssh $TICKET_HOLDER@lxplus.cern.ch ./stageSample.py --dataDir=$dataDir/$book/$dataset --fileList=fileList.$$.txt"
  ssh $TICKET_HOLDER@lxplus.cern.ch ./stageSample.py --dataDir=$dataDir/$book/$dataset --fileList=fileList.$$.txt
  echo "  ssh $TICKET_HOLDER@lxplus.cern.ch rm fileList.$$.txt"
  ssh $TICKET_HOLDER@lxplus.cern.ch rm fileList.$$.txt
fi

# make sure authentication will work
x509File=/tmp/x509up_u`id -u`

# loop over the condor jobs and submit them
while [ $i -le $nCopyProcs ] && [ $last -le $nFiles ]
do
  if [ $i == $nCopyProcs ]
  then
    last=$nFiles
  fi

  # say what we are going to submit
  echo "   downloadFiles.sh $dataDir $book $dataset $target $condorOutput $$ $next $last"

  # prepare the condor_submit files
  cat > submit_$$.cmd <<EOF
Universe                = vanilla
Environment             = "MIT_PROD_DIR=$MIT_PROD_DIR"
Requirements            = Arch == "INTEL" && Disk >= DiskUsage && (Memory * 1024) >= ImageSize && HasFileTransfer
Notify_user             = $TICKET_HOLDER@mit.edu
Notification            = Error
Executable              = $script
Arguments               = $dataDir $book $dataset $target $condorOutput $$ $next $last
Rank                    = Mips
GetEnv                  = False
Input                   = /dev/null
Output                  = $condorOutput/$book/$dataset/${next}-${last}.out
Error                   = $condorOutput/$book/$dataset/${next}-${last}.err
Log                     = $condorOutput/$book/$dataset/${next}-${last}.log
transfer_input_files    = $x509File
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
+AccountingGroup        = "group_cmsuser.cmsu0284"
Queue
EOF

  # submit the jobs
  condor_submit submit_$$.cmd >& /dev/null #>& lastSub
  rm  submit_$$.cmd

  # update counters
  next=$(( $next + $nFilesPerJob ))
  last=$(( $last + $nFilesPerJob ))
  i=$(( $i + 1 ))

done

exit 0
