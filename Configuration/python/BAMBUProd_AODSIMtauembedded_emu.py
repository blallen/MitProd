# $Id: BAMBUProd_AODSIMtauembedded_emu.py,v 1.2 2013/05/07 11:31:20 pharris Exp $

import FWCore.ParameterSet.Config as cms

process = cms.Process('FILLER')

# import of standard configurations
process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.load('Configuration/EventContent/EventContent_cff')

process.configurationMetadata = cms.untracked.PSet(
  version    = cms.untracked.string('Mit_029'),
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
  fileNames = cms.untracked.vstring('/store/cmst3/group/cmgtools/CMG/DoubleMu/StoreResults-Run2012A_22Jan2013_v1_RHembedded_trans1_tau115_ptelec1_20had1_18_v1-f456bdbb960236e5c696adfe9b04eaae/USER/V5_B/PFAOD_81.root')
)
#process.source.inputCommands = cms.untracked.vstring("keep *",
#                                                     "drop *_MEtoEDMConverter_*_*",
#                                                     "drop L1GlobalTriggerObjectMapRecord_hltL1GtObjectMap__HLT")

# other statements
process.GlobalTag.globaltag = 'START53_V15::All'

process.add_(cms.Service("ObjectService"))

process.load("MitProd.BAMBUSequences.BambuFillAODSIM_cfi")

process.MitTreeFiller.TreeWriter.fileName = 'XX-MITDATASET-XX'

process.load('TauAnalysis/MCEmbeddingTools/embeddingKineReweight_cff')
#process.embeddingKineReweightRECembedding.inputFileName = cms.FileInPath('TauAnalysis/MCEmbeddingTools/data/embeddingKineReweight_recEmbedding_mutau.root')
# process.embeddingKineReweightRECembedding.inputFileName = cms.FileInPath('TauAnalysis/MCEmbeddingTools/data/embeddingKineReweight_recEmbedding_etau.root')
process.embeddingKineReweightRECembedding.inputFileName = cms.FileInPath('TauAnalysis/MCEmbeddingTools/data/embeddingKineReweight_recEmbedding_emu.root')

from MitProd.TreeFiller.filltauembedded_cff import *
filltauembedded(process.MitTreeFiller)    
process.MitTreeFiller.MergedConversions.checkTrackRef           = cms.untracked.bool(False)
process.MitTreeFiller.EmbedWeight.useGenInfo                    = True

process.bambu_step  = cms.Path(process.BambuFillAODSIM)
# schedule definition
process.schedule = cms.Schedule(process.bambu_step)
