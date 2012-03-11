# $Id: BAMBUProd_AOD.py,v 1.31 2011/10/09 14:15:05 bendavid Exp $

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
    version = cms.untracked.string('Mit_017'),
    annotation = cms.untracked.string('AOD'),
    name = cms.untracked.string('BambuProduction')
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
                            #fileNames = cms.untracked.vstring('/store/relval/CMSSW_4_4_2/RelValZMM/GEN-SIM-RECO/START44_V9_special_111130-v1/0067/2E329508-DE1D-E111-8EAC-0018F3D09658.root')
                            #/store/mc/Fall11/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_Chamonix12_START44_V10-v2/0000/FED1A710-ED33-E111-B889-003048FFCC1E.root')
                            #fileNames = cms.untracked.vstring('/store/data/Run2011A/Interfill/AOD/PromptReco-v3/000/164/393/EA56AD49-A07C-E011-B1A5-003048F1C836.root')
                            #fileNames = cms.untracked.vstring('/store/relval/CMSSW_4_4_0/Electron/RECO/GR_R_44_V5_RelVal_wzEG2010B-v2/0045/1652C5A5-0EE6-E011-94F2-0018F3D0963C.root'),
                            fileNames = cms.untracked.vstring('/store/relval/CMSSW_4_4_2/DoubleMu/RECO/GR_R_44_V7_RelVal_zMu2011A-v1/0059/FE6E5B28-0C02-E111-AE7E-0018F3D0961A.root')
                            
    #skipEvents=cms.untracked.uint32(30888),
)
process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*", "drop L1GlobalTriggerObjectMapRecord_hltL1GtObjectMap__HLT")

# other statements
process.GlobalTag.globaltag = 'GR_R_44_V6A::All'

process.add_(cms.Service("ObjectService"))

process.load("MitProd.BAMBUSequences.BambuFillAOD_cfi")

process.MitTreeFiller.TreeWriter.fileName = 'XX-MITDATASET-XX'

process.bambu_step  = cms.Path(process.BambuFillAOD)

# schedule definition
process.schedule = cms.Schedule(process.bambu_step)
