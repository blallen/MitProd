# $Id: mc.py,v 1.1 2013/07/10 02:25:44 paus Exp $

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
  version    = cms.untracked.string('Mit_031'),
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
  fileNames = cms.untracked.vstring('/store/relval/CMSSW_5_3_2-START53_V6/RelValProdTTbar/AODSIM/v2/0000/9A630BD7-C3B9-E111-BAB3-00304867918E.root')
)

process.source.inputCommands = cms.untracked.vstring("keep *",
                                                     "drop *_MEtoEDMConverter_*_*",
                                                     "drop L1GlobalTriggerObjectMapRecord_hltL1GtObjectMap__HLT")

# other statements
process.GlobalTag.globaltag = 'START53_LV3::All'

process.add_(cms.Service("ObjectService"))

process.load("MitProd.BAMBUSequences.BambuFillAODSIM_cfi")

#process.MitTreeFiller.TreeWriter.fileName = 'XX-MITDATASET-XX'
process.MitTreeFiller.TreeWriter.fileName = 'bambu-output-file-tmp'

process.bambu_step  = cms.Path(process.BambuFillAODSIM)
# schedule definition
process.schedule = cms.Schedule(process.bambu_step)
