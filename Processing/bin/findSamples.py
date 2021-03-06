#!/usr/bin/env python
#---------------------------------------------------------------------------------------------------
# Script to identify all samples which are kept in our database.
#
# Author: C.Paus                                                                (September 23, 2008)
#---------------------------------------------------------------------------------------------------
import os,sys,getopt,re,string
from subprocess import call
import task

def findStartedDatasets(path):
    if debug == 1:
        print " Collecting information over started samples"
    datasetList = []

    cmd = 'list ' + path
    for line in os.popen(cmd).readlines():   # run command
        line = line[:-1]                     # strip '\n'
        f    = line.split(" ")
        size = f[0]
        file = f[1]

        #if debug == 1:
        #    print ' Debug:: adding: ' + file + ' with size ' + size
        datasetList.append(file)

    return datasetList

def findOngoingDatasets(path):
    if debug == 1:
        print " Collecting information over ongoing samples"
    datasetList = []

    cmd = 'cat crab_[0-9]_[0-9]*_[0-9]*/share/crab.cfg |grep ^user_remote_dir'
    for line in os.popen(cmd).readlines():   # run command
        line    = line[:-1]                  # strip '\n'
        f       = line.split("/")
        dataset = f[-1]
        if re.search('crab_0',dataset):
            dataset = f[-2]
        
        #if debug == 1:
        #    print ' Debug:: adding: ' + dataset '
        datasetList.append(dataset)

    return datasetList

def findCompletedDatasets(path):
    if debug == 1:
        print " Collecting information over completed samples"
    datasetList = []

    cmd = 'cat ' + os.environ['MIT_PROD_DIR'] + '/' + mitCfg + '/' + version + \
          '/Completed  2> /dev/null'
    for line in os.popen(cmd).readlines():   # run command
        line    = line[:-1]                  # strip '\n'
        dataset = line

        #if debug == 1:
        #    print ' Debug:: adding: ' + dataset '
        datasetList.append(dataset)

    return datasetList

def inList(file,list):
    for entry in list:
        if entry == file:
            return True
    return False

def cleanupCompletedList(ongoingDsetList,completedDsetList):
    if debug == 1:
        print " Update completed list with ongoing list"

    for dataset in ongoingDsetList:
        if inList(dataset,completedDsetList):
            print ' -> removing fropm completed: ' + dataset
            cmd  = 'cat ' + mitCfg + '/' + version + '/Completed|grep -v ^' + dataset + '$ > C.bak'
            cmd += '; mv C.bak ' + mitCfg + '/' + version + '/Completed'
            os.system(cmd)

#===================================================================================================
# Main starts here
#===================================================================================================
# Define string to explain usage of the script
usage  = "\nUsage: findSamples.py --mitCfg=<name>\n"
usage += "                      --version=<version> [ default: MIT_VERS ]\n"
usage += "                      --cmssw=<name>\n"
usage += "                      --pattern=<name>\n"
usage += "                      --download=<int: -1,0,1>\n"
usage += "                      --status=<int: -1,0,1>\n"
usage += "                      --remakeLfns=<int: -1,0,1>\n"
usage += "                      --show=<int: 0,1>\n"
usage += "                      --useCachedDb\n"
usage += "                      --useExistingLfns\n"
usage += "                      --useExistingSites\n"
usage += "                      --exe\n"
usage += "                      --noInfo\n"
usage += "                      --forceCopy\n"
usage += "                      --debug\n"
usage += "                      --help\n\n"

# Define the valid options which can be specified and check out the command line
valid = ['mitCfg=','version=','cmssw=','pattern=','download=','status=','remakeLfns=','show=', \
         'help','exe','useCachedDb','useExistingLfns','useExistingSites','complete','noInfo',
         'forceCopy','debug']
try:
    opts, args = getopt.getopt(sys.argv[1:], "", valid)
except getopt.GetoptError, ex:
    print usage
    print str(ex)
    sys.exit(1)

# --------------------------------------------------------------------------------------------------
# Get all parameters for the production
# --------------------------------------------------------------------------------------------------
# Set defaults for each option
mitCfg           = 'filefi'
version          = os.environ['MIT_VERS']
cmssw            = ''
pattern          = ''
cmsswCfg         = 'cmssw.cfg'
exe              = 0
useCachedDb      = False
useExistingLfns  = False
useExistingSites = False
complete         = 0
noInfo           = False
download         = -1
status           = -1
remakeLfns       = -1
show             = 0
forceCopy        = False
debug            = False

webServer        = 'http://t3serv001.mit.edu/~cmsprod'

# Read new values from the command line
for opt, arg in opts:
    if opt == "--help":
        print usage
        sys.exit(0)
    if opt == "--mitCfg":
        mitCfg          = arg
    if opt == "--version":
        version         = arg
    if opt == "--cmssw":
        cmssw           = arg
    if opt == "--pattern":
        pattern         = arg
    if opt == "--exe":
        exe             = 1
    if opt == "--useCachedDb":
        useCachedDb     = True
    if opt == "--useExistingLfns":
        useExistingLfns = True
    if opt == "--useExistingSites":
        useExistingSites = True
    if opt == "--download":
        download        = int(arg)
    if opt == "--status":
        status          = int(arg)
    if opt == "--remakeLfns":
        remakeLfns      = int(arg)
    if opt == "--show":
        show            = int(arg)
    if opt == "--complete":
        complete        = 1
    if opt == "--noInfo":
        noInfo          = True
    if opt == "--forceCopy":
        forceCopy       = True
    if opt == "--debug":
        debug           = True

# Read parameters needed
crabFile = os.environ['MIT_PROD_DIR'] + '/' + mitCfg + '/' + version + '/' + 'crab.cfg'
if not os.path.exists(crabFile):
    cmd = "Crab file not found: %s" % crabFile
    raise RuntimeError, cmd

# Does the local environment exist?
dir = mitCfg + '/' + version
if not os.path.exists(dir):
    cmd = "\n Local work directory does not exist: %s\n" % dir
    raise RuntimeError, cmd

if not useCachedDb:
    # Download up to date database file for productions
    cmd  = 'wget ' + webServer + '/' + mitCfg + '/' + version + '/Productions.' + cmssw \
           + ' -O /tmp/Productions.' + cmssw
    rc = call(cmd.split(' '))
    if rc == 0:
        print " Download of central database file worked (rc=%d)."%(rc)
    else:
        print " Download of central database file failed."
    
    # Check whether something has changed
    cmd  = 'diff /tmp/Productions.' + cmssw + ' ' \
           + './' + mitCfg + '/' + version + '/Productions.' + cmssw
    rc = call(cmd.split(' '))
    if rc == 0:
        print " No difference in the local and central database files (rc=%d)."%(rc)
    else:
        print " Differences in central and local file found (rc=%d)."%(rc)
        print " Moving one!."%(rc)
        #answer = raw_input(" Overwrite the local database with these changes and continue? [y/N] ")
        ## Check whether something has changed
        #if answer == 'y' or answer == 'Y':
        #    cmd  = 'mv /tmp/Productions.' + cmssw + ' ./' + mitCfg \
        #           + '/' + version + '/Productions.' + cmssw
        #    rc = call(cmd.split(' '))
        #    print ' Local database was overwritten.'
        #else:
        #    print ' Local database *not* overwritten. Exit here.'
        #    sys.exit(0)
else:
    print " Using cached version: "
    cmd = 'ls -lhrt ./' + mitCfg + '/' + version + '/Productions.' \
          + cmssw
    rc = call(cmd.split(' '))

cmsswFile = os.environ['MIT_PROD_DIR'] + '/' + mitCfg + '/' + version + '/' + cmsswCfg
if not os.path.exists(cmsswFile):
    cmd = "Cmssw file not found: %s" % cmsswFile
    cmsswCfg = 'cmssw.py'
    cmsswFile = os.environ['MIT_PROD_DIR'] + '/' + mitCfg + '/' + version + '/' + cmsswCfg
    if not os.path.exists(cmsswFile):
        cmd  = " Cmssw file not found: %s\n" % cmsswFile
        cmd += " XXXX ERROR no valid configuration found XXXX"
        raise RuntimeError, cmd

# Where is our storage?
storageTag = 'T2_US_MIT'
domain = task.Domain()
if   re.search('mit.edu',domain):
    storageTag = 'T2_US_MIT'
elif re.search('cern.ch',domain):
    storageTag = 'T0_CH_CERN'
seTable = os.environ['MIT_PROD_DIR'] + '/' + mitCfg + '/' + version + '/' + 'seTable'
if not os.path.exists(crabFile):
    cmd = "seTable file not found: %s" % seTable
    raise RuntimeError, cmd
cmd = 'grep ^' + storageTag + ' ' + seTable + ' | cut -d = -f2 | sed \'s# : ##\''
for line in os.popen(cmd).readlines():
    path = line[:-1] +  '/' + mitCfg + '/' + version

# Find all started samples
startedDsetList   = findStartedDatasets(path)
ongoingDsetList   = findOngoingDatasets(path)
completedDsetList = findCompletedDatasets(path)
cleanupCompletedList(ongoingDsetList,completedDsetList)
completedDsetList = findCompletedDatasets(path)

# Resolve the other mitCfg parameters from the configuration file
cmd = 'cat ' + './' + mitCfg + '/' + version + '/' + 'Productions'
#cmd = 'cat '+ os.environ['MIT_PROD_DIR'] + '/' + mitCfg + '/' + version + '/' + 'Productions'
if cmssw != '':
    cmd = cmd + '.' + cmssw

print ''

join       = 0
mitDataset = ""
fullLine   = ""
bSlash     = "\\";
printOpt   = "-header"
samples    = {}
dbs        = ""
for line in os.popen(cmd).readlines():  # run command
    line = line[:-1]
    #print 'Line: "' + line + '"'
    # get ride of empty lines
    if line == '':
        continue
    # get ride of commented lines and read steering parameters
    if line[0] == '#':
        names = line.split()       # splitting every blank
        if len(names)> 2 and names[1] == 'crontab' and int(names[3]) != 1:
            print 'No crontab has been set.... (LINE: ' + line + ')'
            sys.exit(0)
        continue

    # join lines
    if join == 1:
        fullLine += line
    else:
        fullLine  = line

    # determine if finished or more is coming
    if fullLine[-1] == bSlash:
        join = 1
        fullLine = fullLine[:-1]
    else:
        join = 0
        fullLine = " ".join(str(fullLine).split()).strip()
        # test whether there is a directory   
        names      = fullLine.split()       # splitting every blank
        if debug == True:
            print "FullLine: " + fullLine
        cmsDataset = names[0]
        # OLD CP # mitDataset = names[1]      # the equivalent MIT name of the dataset
        mitDataset = cmsDataset[1:].replace("/","+")
        nevents    = int(names[2])          # number of events to be used in the production
        procStatus = names[3]
        local      = names[4]
        # check whether dbs is given
        dbs=""
        if len(names) > 5:
            dbs = names[5]
        fixSites=""
        if len(names) > 6:
            fixSites = names[6]
        
        if pattern != '' and not re.search(pattern,mitDataset):
            continue
#	else:
#	    print ' SET: ' + mitDataset 
#	    print ' PTR:    ' + pattern

        # this is a dataset (equivalent to a line) that we will consider
        sample = task.Sample(cmsDataset,mitDataset,str(nevents),procStatus,local)
        # is it already in our list or is it new?
        if sample.cmsDataset in samples:
            if mitDataset != samples[sample.cmsDataset].mitDataset:
                print " renameSample.sh ",
                print " " + mitDataset + " " + samples[sample.cmsDataset].mitDataset
                samples[sample.cmsDataset].mitDataset += " " + mitDataset
        else:
            samples[sample.cmsDataset] = sample

        # make sure we want to consider submission
        if download != 1 and status != 1  and show != 1 and remakeLfns != 1:
            cmd = 'submit.py --mitCfg=' + mitCfg + ' --version=' + version + ' --noTestJob'
            if cmssw != '':
                cmd = cmd + " --cmssw=" + cmssw
            if useExistingLfns:
                cmd = cmd + " --useExistingLfns"
            if useExistingSites:
                cmd = cmd + " --useExistingSites"
            if dbs == "none":
                if fixSites == '':
                    cmd = cmd + " --fixSites=T1_US_FNAL"
                else:
                    cmd = cmd + " --fixSites=" + fixSites

            # last thing to add is the dataset itself (nicer printing)
            cmd = cmd + ' --mitDataset=' + mitDataset

            # check for errors (to be done)
    
            # check for the logical combinations
            if   not inList(mitDataset,startedDsetList):
                print ' submitting: ' + cmd
                if exe == 1:
                    os.system(cmd)
    
            elif     inList(mitDataset,ongoingDsetList):
                if download != 1 and status != 1:
                    print ' handled by jobSitter -- ' + mitDataset
    
            elif     inList(mitDataset,completedDsetList):
                if not noInfo:
                    print ' don: ' + mitDataset
            else:
                if complete == 1:
                    cmd = cmd + ' --complete'
                    print ' completing: ' + cmd
                    if exe == 1:
                        os.system(cmd)

        # test status request
        if status != -1:
            cmd = 'status.sh ' + mitCfg + '/' + version + ' ' + mitDataset + ' ' + printOpt
            if exe == 1:
                rc = os.system(cmd)
            else:
                print " " + cmd
            printOpt = ""

        # test remake lfns request
        if remakeLfns != -1:
            lfnFile = 'lfns/' + mitDataset + '.lfns'
            cmd = 'input.py --dbs=' + dbs + ' --option=lfn --dataset=' + cmsDataset + ' > ' \
                  + lfnFile
            print ' input: ' + cmd + '\n'
            if exe == 1:
                rc = os.system(cmd)

        # test download request
        if local != "-" and download != -1:
            localPath  = local
            cmd = 'downloadSample.py --cmsDataset=' + cmsDataset + ' --mitCfg=' + mitCfg + \
                  " --version=" + version
            if cmssw != '':
                cmd = cmd + " --cmssw=" + cmssw
            if forceCopy:
                cmd += ' --forceCopy'
            print " " + cmd
            if exe == 1:
                rc = os.system(cmd)
            

if show != 0:
    lCmsDataset = 0
    lMitDataset = 0
    lNEvents    = 0
    lStatus     = 0
    lLocalPath  = 0
    lDbs        = 0

    for dataset in sorted(samples.iterkeys()):
        sample = samples[dataset]
        lCmsDataset = max(lCmsDataset,len(sample.cmsDataset))
        lMitDataset = max(lMitDataset,len(sample.mitDataset))
        lNEvents    = max(lNEvents   ,len(sample.nEvents   ))
        lStatus     = max(lStatus    ,len(sample.status    ))
        lLocalPath  = max(lLocalPath ,len(sample.localPath ))
        lDbs        = max(lDbs       ,len(sample.dbs       ))

    for dataset in sorted(samples.iterkeys()):
        sample = samples[dataset]
        sample.showFormat(lCmsDataset+2,lMitDataset+2,lNEvents+1,lStatus+1,lLocalPath+1,lDbs)

if mitDataset == "":
    print "ERROR - dataset not defined."
    sys.exit(0)

sys.exit(0)
