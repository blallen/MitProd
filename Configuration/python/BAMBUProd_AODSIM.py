# $Id: BAMBUProd_AODSIM.py,v 1.36 2012/04/11 20:18:27 paus Exp $

import FWCore.ParameterSet.Config as cms

process = cms.Process('FILEFI')

# import of standard configurations
process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.load('Configuration/EventContent/EventContent_cff')
process.load('RecoVertex/PrimaryVertexProducer/OfflinePrimaryVertices_cfi')
 
process.configurationMetadata = cms.untracked.PSet(
  version    = cms.untracked.string('Mit_026'),
  annotation = cms.untracked.string('AODSIM'),
  name       = cms.untracked.string('BambuProduction')
)

process.maxEvents = cms.untracked.PSet(
  input = cms.untracked.int32(-1)
)

process.options = cms.untracked.PSet(
  Rethrow = cms.untracked.vstring('ProductNotFound'),
  fileMode = cms.untracked.string('NOMERGE'),
)

# input source
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring('/store/relval/CMSSW_5_2_2/RelValProdTTbar/GEN-SIM-RECO/START52_V4-v1/0004/DCA3A2E4-C973-E111-9839-003048F1183E.root')
)

process.source.inputCommands = cms.untracked.vstring("keep *",
                                                     "drop *_MEtoEDMConverter_*_*",
                                                     "drop L1GlobalTriggerObjectMapRecord_hltL1GtObjectMap__HLT")

# other statements
process.GlobalTag.globaltag = 'START52_V9::All'

process.add_(cms.Service("ObjectService"))

process.load("MitProd.BAMBUSequences.BambuFillAODSIM_cfi")

process.MitTreeFiller.TreeWriter.fileName = 'XX-MITDATASET-XX'

#process.output = cms.OutputModule("PoolOutputModule",
#                                  outputCommands = cms.untracked.vstring('keep *'),
#                                  fileName       = cms.untracked.string ("test.root")
#)


process.bambu_step  = cms.Path(process.BambuFillAODSIM)
# schedule definition
process.schedule = cms.Schedule(process.bambu_step)
#process.outpath  = cms.EndPath(process.output)
