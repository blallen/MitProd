#!/bin/bash
#---------------------------------------------------------------------------------------------------
# Catalog exactly one file, either interactively or submitting to condor batch system.
#
#                                                                             Ch.Paus (Dec 09, 2008)
#---------------------------------------------------------------------------------------------------
# some basic printing
h=`basename $0`
echo " ${h}: Show who and where we are!"
echo " Script:    $h"
echo " Arguments: ($*)"
echo " "
echo " start time    : "`date`
echo " user executing: "`whoami`" --> "`id`
echo " running on    : "`/bin/hostname`
echo " executing in  : "`pwd`
echo " ";

export CATALOG_MACRO="runFileCataloger.C+"

dataDir=$1
dataFile=$2
if [ ".$2" == "." ]
then
  dataFile=`basename $dataDir`
  dataDir=`dirname $dataDir`
fi

if ! [ -z "`echo $dataDir | grep delphes`" ] || ! [ -z "`echo $dataDir | grep user/paus/mc`" ]
then
  CATALOG_MACRO="runSimpleFileCataloger.C"
fi

procId=$$
logFile=`echo $dataDir/$dataFile | tr '/' '+'`
logFile=/tmp/$logFile

echo " "; echo "Initialize CMSSW"; echo " "

# this seems to fail -- local release broken?
#export SCRAM_ARCH='slc5_ia32_gcc434'
#export  VO_CMS_SW_DIR=~cmsprod/cmssoft
#source $VO_CMS_SW_DIR/cmsset_default.sh
#cd     ~cmsprod/cms/cmssw/018/CMSSW_3_9_7/src

source /cvmfs/cms.cern.ch/cmsset_default.sh
#cd     ~cmsprod/cms/cmssw/018/CMSSW_3_11_3/src
#cd     ~cmsprod/cms/cmssw/032/CMSSW_5_3_11/src
cd     ~cmsprod/cms/cmssw/040/CMSSW_7_4_0/src
eval   `scram runtime -sh`
source $CMSSW_BASE/src/MitProd/Processing/bin/processing.sh

cd - >& /dev/null

# show the certificate
# take care of the certificate
if [ -e "./x509up_u`id -u`" ]
then
  export X509_USER_PROXY="./x509up_u`id -u`"
fi
echo " INFO -- using the x509 ticket: $X509_USER_PROXY"
voms-proxy-info -all

# Get ready to run
rm -f $logFile

which root
echo "PWD: $CMSSW_BASE/src/MitAna/macros/"
ls -lhrt   $CMSSW_BASE/src/MitAna/macros/

echo " "; echo "Starting root now"; echo " "
echo " root -l -b -q $CMSSW_BASE/src/MitProd/Processing/root/rootlogon.C \ "
echo "               $CMSSW_BASE/src/MitProd/Processing/root/${CATALOG_MACRO} \ "
echo "               ($dataDir,$dataFile) \ "
echo "               >& $logFile "

root -l -b -q \
     $CMSSW_BASE/src/MitProd/Processing/root/rootlogon.C \
     $CMSSW_BASE/src/MitProd/Processing/root/${CATALOG_MACRO}\(\"$dataDir\",\"$dataFile\"\) \
     >& $logFile
  
status=`echo $?`
error=`cat $logFile |grep -v mithep::Selector::UpdateRunInfo | grep -v 'no dictionary for class' | grep 'Error' | wc -l`
zip=`grep R__unzip: $logFile | wc -l`
  
echo " "
echo "Status: $status  Errors: $error  R__Unzip: $zip"
if [ $status == 0 ] && [ $error == 0 ] && [ $zip == 0 ]
then
  cat $logFile
  echo "DECISION"
  echo "  File  $dataDir/$dataFile  looks healthy, make entry into cataloging database."
  echo " "
  echo -n " XX-CATALOG-XX "
  tail -1 $logFile 
else
  echo " ==== DUMPING LOGFILE NOW ===="
  cat $logFile
  echo "DECISION"
  echo "  File  $dataDir/$dataFile  looks corrupted, remove it."
fi

rm -f $logFile

exit 0
