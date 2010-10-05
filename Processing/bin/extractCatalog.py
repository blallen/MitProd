#!/usr/bin/env python
#---------------------------------------------------------------------------------------------------
# Script to extract catalog information from condor outputs.
#
# Catalog extraction principle:
#
# 1) create a raw file with the bare bones information in the cataloging directory
#    happens in this script extractCatalog.py: order files by the job numbers
#    - this raw file has to have various versions to ensure existing data does
#      not get overwritten or mixed in
#
# 2) from the raw file we will then in a separate step generate the catalog
#    - need to be able to deal with files being added on in the end
#
# 3) dealing with files added later on?!
#    - need to move output from batch job into done directory
#    - need to find a way to add on this information to the existing catalog
# 
# Author: C.Paus                                                                  (November 08 2008)
#---------------------------------------------------------------------------------------------------
import os,sys,getopt,re,string

def move(srcFile,source,target):
    # make an entry to be executed
    if not re.search('castor/cern.ch',source):
        mvCmd = "echo mv " + "/".join(source.split('/')[3:]) + ' ' \
                +            "/".join(target.split('/')[3:]) + " >> " + srcFile
        os.system(mvCmd)

    cmd = 'move ' + source + '  ' + target
    print cmd
    if test == 0 and re.search('castor/cern.ch',source):
        status = os.system(cmd)

    return status

  
#===================================================================================================
# Main starts here
#===================================================================================================
# Define string to explain usage of the script
usage  = "\n"
usage += " Usage: extractCatalog.py --dataset=<name>\n"
usage += "                          --mitCfg=<name>\n"
usage += "                          --version=<name>\n"
usage += "                          --catalogDir=<name>\n"
usage += "                          --retry\n"
usage += "                          --remove\n"
usage += "                          --compact\n"
usage += "                          --test\n"
usage += "                          --retest\n"
usage += "                          --debug\n"
usage += "                          --help\n\n"

# Define the valid options which can be specified and check out the command line
valid = ['dataset=','mitCfg=','version=','catalogDir=','retry','remove','compact','test',
         'retest','debug','help']
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
server     = "srm://se01.cmsaf.mit.edu:8443/srm/managerv2?SFN="
catalogDir = "/home/cmsprod/catalog/t2mit"
dataset    = None
mitCfg     = "filefi"
version    = "014"
lRetry     = 0
lRemove    = 0
compact    = 0
test       = 0
debug      = 0
retest     = 0
official   = 0

# Read new values from the command line
for opt, arg in opts:
    if opt == "--help":
        print usage
        sys.exit(0)
    if opt == "--catalogDir":
        catalogDir = arg
    if opt == "--dataset":
        dataset    = arg
    if opt == "--mitCfg":
        mitCfg     = arg
    if opt == "--version":
        version    = arg
    if opt == "--retry":
        lRetry     = 1
    if opt == "--remove":
        lRemove    = 1
    if opt == "--compact":
        compact    = 1
    if opt == "--test":
        test       = 1
    if opt == "--debug":
        debug      = 1
    if opt == "--retest":
        retest     = 1

# Deal with obvious problems
if dataset == None:
    cmd = "--dataset option not provided. This is required."
    raise RuntimeError, cmd

# Are we dealing with a dataset residing at MIT
atMit = 0
if re.search('catalog/t2mit',catalogDir):
    atMit = 1

# See whether we are dealing with an official production request
if re.search('crab_0',dataset):
    official   = 1
    f = dataset.split('/')
    offDataset = f[0]
    crabId     = f[1]
##    if os.path.exists(os.environ['HOME']+ \
##                      '/cms/jobs/'+mitCfg+'/'+version+'/'+offDataset+'.lfns'+'_'+crabId):
    fileInput = open(os.environ['HOME']+ \
                     '/cms/jobs/'+mitCfg+'/'+version+'/'+offDataset+'.lfns'+'_'+crabId,'r')
##    else:
##        print ' WARNING WARNING ---- LFN FILE << OLD PRODUCTION OR DANGER FOR DATA MATCHING >>'
##        fileInput = open(os.environ['HOME']+ \
##                         '/cms/jobs/'+mitCfg+'/'+version+'/'+offDataset+'.lfns','r')
    index = 1
    files = {}
    nevts = {}
    for line in fileInput:
        f = line.split(" ")
        g = f[1].split("/")
##        if len(f) == 2:
##            print '\n\nOLD SCHEME\n\n'
##            g = f[0].split("/")
        originalFile = offDataset + '_000_%d_1.root'%index
        if debug == 1:
            print ' Key: %s  Name: %s  NEvts: %d'%(originalFile,g[-1],int(f[1]))
        files[originalFile] = g[-1] 
##        if len(f) == 2:
##            print '\n\nOLD SCHEME\n\n'
##            nevts[originalFile] = int(f[1])
##        else:
        nevts[originalFile] = int(f[2])
        index += 1
    fileInput.close()
    

# No specific task means just testing
if lRetry == 0 and lRemove == 0:
    test = 1

# Debug mode is always in test
if debug == 1:
    test = 1

# Create directories necessary to work
logDir  = catalogDir + '/condor/' + mitCfg + '/' + version + '/' + dataset
procDir = ' '
doneDir = ' '
rawDir  = ' '
if os.path.exists(logDir):
    procDir =  catalogDir + '/condor/' + mitCfg + '/' + version + '/' + dataset + '/proc'
    doneDir =  catalogDir + '/condor/' + mitCfg + '/' + version + '/' + dataset + '/done'
    rawDir  =  catalogDir + '/' + mitCfg + '/' + version + '/' + dataset
    if re.search('crab_0',rawDir):
        rawDir =  catalogDir + '/' + mitCfg + '/' + version + '/' + offDataset
    cmd     = "mkdir -p " + procDir + ' ' + doneDir + ' ' + rawDir
    status = os.system(cmd)
    if status != 0:
        print " Directory for the requested datasets could not be created. -> EXIT"
        sys.exit(1)        
else:
    print " Directory request: " + logDir
    print " Directory for the requested dataset does not exist. -> EXIT"
    sys.exit(1)

# Reset the extraction for the entire dataset and exit
if retest == 1:
    print '\n Move all logs back to unprocessed area. \n'
    cmd = 'cd ' + logDir + '/done/; mv *.err ../'
    status1 = os.system(cmd)
    cmd = 'cd ' + logDir + '/done/; mv *.out ../'
    status2 = os.system(cmd)
    if status1 != 0 or status2 != 0:
        print " Could not move files to unproc status (comand line, too long maybe?). -> EXIT"
        print '   logDir : ' + logDir
        print '   procDir: ' + procDir
        sys.exit(1)
    sys.exit(0)

# Compactify the RawFile.?? into one sorted file
if compact == 1:
    # Consolidate the existing RawFiles.?? into just one
    print '\n Consolidating the raw files into one. \n'
    cmd = 'cat ' + rawDir + '/RawFiles.?? | sort -u > /tmp/RawFiles.00; cat /tmp/RawFiles.00;'
    status = os.system(cmd)
    if os.path.exists(rawDir + '/old'):
        cmd = 'rm -rf ' + rawDir + '/old'
        #print 'CMD: ' + cmd
        status = os.system(cmd)
    cmd = 'mkdir ' + rawDir + '/old; mv ' + rawDir + '/RawFiles.?? ' + rawDir + '/old'
    status = os.system(cmd)
    cmd = 'mv /tmp/RawFiles.00 ' + rawDir
    status = os.system(cmd)
    sys.exit(0)

# Are there any files or maybe too many?
cmd = 'cd ' + logDir + '; ls *.out *.err >& /dev/null'
status = os.system(cmd)
if status != 0:
    print " Could not find files or comand line is too long maybe. -> EXIT"
    print '   logDir : ' + logDir
    print '   procDir: ' + procDir
    sys.exit(1)
    
# Safe the status (we are going from proc and later to done to have a save environment)
cmd = 'cd ' + logDir + '; mv *.err proc/'
status1 = os.system(cmd)
cmd = 'cd ' + logDir + '; mv *.out proc/'
status2 = os.system(cmd)
if status1 != 0 or status2 != 0:
    print " Could not move files to proc status (comand line, too long maybe?). -> EXIT"
    print '   logDir : ' + logDir
    print '   procDir: ' + procDir
    sys.exit(1)
    
cmd = 'cd ' + procDir + '; cat *.out | grep \'  File \' | grep corrupted'
print 'Execute:  ' + cmd
lBroken = False
for line in os.popen(cmd).readlines():  # run command
    line = line[:-1]
    if not lBroken:
        lBroken = True
        print 'XXXX Broken files XXXX Broken files XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    # compactify line
    line = " ".join(str(line).split()).strip()
    f = line.split(" ");
    rm0 = "rm           " + f[1]
    rm1 = "stager_rm -M " + f[1]
    rm2 = "nsrm         " + f[1]
    #rm3 = "srmrm        " + server + f[1]
    rm3 = "ssh paus@cgate.mit.edu rm " + f[1]
    g = f[1].split("/")
    file = g[-1]
    rm4 = "rm           " + procDir + '/' + file + '.{err,out}'

    machine = "fgrep cern.ch " + procDir + '/' + file + '.out | head -1 | sed "s/^/Machine: /"' 
    os.system(machine)

    if   re.search("/castor/cern.ch",f[1]):
        cmd = rm1 + '; ' + rm2 + '; ' + rm4
        print '  ' + rm1 + '\n  ' + rm2 + '\n  ' + rm4
    elif re.search("cmsaf.mit.edu",f[1]):
        cmd = rm3 + '; ' + rm4
        print '  ' + rm3 + '\n  ' + rm4
    else:
        cmd = rm0 + '; ' + rm4
        print '  ' + rm0 + '\n  ' + rm4

    if   lRetry == 1 and test == 0:
        print ' Deleting only log files'
        status = os.system(rm4)
    elif lRemove == 1 and test == 0:
        print ' Deleting entire job output'
        status = os.system(cmd)

    if debug ==1:
        print ' == DUMPING .err and .out =='
        dump = "cat " + procDir + '/' + file + '.out' 
        os.system(dump)
        dump = "cat " + procDir + '/' + file + '.err' 
        os.system(dump)
        

# Find out what the name of the raw file will be
cmd = 'ls -1 ' + rawDir + ' | grep RawFiles | tail -1'
rawFile = 'RawFiles.00'
#testFile = catalogDir + '/' + mitCfg + '/' + version + '/' + dataset + '/RawFiles.00'
testFile = rawDir + '/RawFiles.00'
if os.path.exists(testFile):
    for line in os.popen(cmd).readlines():  # run command
        rawFile = line[:-1]
        #print '  ' + rawFile
        f = line.split('.');
        number = int(f[1])
        number = number + 1
        rawFile = '%s.%02d'%(f[0],number)
print 'Raw file identified (in %s): \n     %s'%(rawDir,rawFile)

# --------------------------------------------------------------------------------------------------
#                           START -- THE KEY ACTION
# 
# Find new catalog entries and add them to the new raw file (or not for test run)
# --------------------------------------------------------------------------------------------------

# Create the moving file from this extract task
srcFile = "EMPTY.bak"
if official == 1 and atMit == 1:
    cmd = "date +Extracting_%y%m%d_%H%M%S.src"
    for line in os.popen(cmd).readlines():  # run command
        line = line[:-1]
        srcFile = line
    cmd = "rm -f " + srcFile + "; touch " + srcFile
    os.system(cmd)


# Process all relevant files
cmd = 'cd ' + procDir + '; cat *.out | grep XX-CATALOG-XX'
print 'Execute:  ' + cmd
print '  For the catalog:'
if test == 0:
    fileOutput = open(rawDir + '/' + rawFile,'w')
for line in os.popen(cmd).readlines():  # run command
    #print 'LINE: ' + line
    line = line[:-1]
    # compactify line
    line = " ".join(str(line).split()).strip()
    f = line.split(" ");
    f = f[2:];

    # are we dealing with an official production dataset?
    valid = 1
    if official == 1:
        if len(f) < 2:
            continue
        fullFile = f[0]
        nProc    = int(f[1])
        g        = fullFile.split("/");
        file     = g[-1]
        g        = g[:-2]
        dir      = "/".join(g)
        if nProc == nevts[file]:
            ##print ' complete: ' + file + '  -->  ' + files[file] + '  %d /%d' %(nProc,nevts[file])
            move(srcFile,fullFile,dir + '/' + files[file])
            # modify the catalog entry accordingly
            f[0] = dir + '/' + files[file]
        else:
            valid = 0
            print ' ERROR   : ' + file + '  -->  ' + files[file] + '  %d /%d' %(nProc,nevts[file])
            
    if valid == 1:
        line = " ".join(f)
        print '  ' + line
        if test == 0:
            fileOutput.write(line + '\n')

if test == 0:
    fileOutput.close()

if atMit == 1:
    # Moving all files
    cmd = "scp " + srcFile + ' paus@cgate.mit.edu:'
    print ' CMD: ' + cmd
    status = os.system(cmd)
    cmd = "ssh paus@cgate.mit.edu source " + srcFile
    print ' CMD: ' + cmd
    status = os.system(cmd)
    
    # Removing the source file once we are done
    cmd = "rm " + srcFile + "; ssh paus@cgate rm " + srcFile
    print ' CMD: ' + cmd
    status = os.system(cmd)

# --------------------------------------------------------------------------------------------------
#                           END ---- THE KEY ACTION
# --------------------------------------------------------------------------------------------------

# Safe the status (from proc to done, or back to the original directory for test)
cmd = 'cd ' + procDir + '; mv *.err ../done/'
if test != 0:
    cmd = 'cd ' + procDir + '; mv *.err ../'
status1 = os.system(cmd)

cmd = 'cd ' + procDir + '; mv *.out ../done/'
if test != 0:
    cmd = 'cd ' + procDir + '; mv *.out ../'
status2 = os.system(cmd)

if status1 != 0 or status2 != 0:
    print " Could not move files from proc to done status (comand line, too long maybe?). -> EXIT"
    print '   procDir: ' + procDir
    print '   doneDir: ' + doneDir
    sys.exit(1)

sys.exit(0)
