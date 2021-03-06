import FWCore.ParameterSet.Config as cms

process = cms.Process('FILEFI')

# import of standard configurations
process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load('Configuration/StandardSequences/MixingNoPileUp_cff')
process.load('Configuration/StandardSequences/GeometryIdeal_cff')
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration/StandardSequences/Digi_cff')
process.load('Configuration/StandardSequences/SimL1Emulator_cff')
process.load('Configuration/StandardSequences/DigiToRaw_cff')
process.load('Configuration/StandardSequences/RawToDigi_cff')
process.load('Configuration/StandardSequences/L1Reco_cff')
process.load('Configuration/StandardSequences/Reconstruction_cff')
process.load('Configuration/StandardSequences/EndOfProcess_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.load('Configuration/EventContent/EventContent_cff')

process.configurationMetadata = cms.untracked.PSet(
  version    = cms.untracked.string('Mit_029'),
  annotation = cms.untracked.string('redigiReRecoNoPixels'),
  name       = cms.untracked.string('BambuProduction')
)
process.options = cms.untracked.PSet(
  Rethrow  = cms.untracked.vstring('ProductNotFound'),
  fileMode =  cms.untracked.string('NOMERGE'),
)

# Input source
process.source = cms.Source("PoolSource",
  fileNames = cms.untracked.vstring('file:/build/bendavid/RAW/MinBias900GeV334Startup/FA1C6DA5-0FD7-DE11-A2BC-00304867901A.root')
)
process.source.inputCommands = cms.untracked.vstring("keep *",
                                                     "drop *_MEtoEDMConverter_*_*",
                                                     "drop L1GlobalTriggerObjectMapRecord_hltL1GtObjectMap__HLT")

# Other statements
process.GlobalTag.globaltag = 'GR_P_V40::All'

#remove pixel detector at digi level
process.DigiToRaw.remove(process.siPixelRawData)
        
process.add_(cms.Service("ObjectService"))

process.load("MitProd.BAMBUSequences.BambuFillRECOSIM_cfi")

process.MitTreeFiller.TreeWriter.fileName = 'XX-MITDATASET-XX'

#loosen conversion producer pre-selection
process.mvfTrackerConversions.rhoMin = 0.1

#hack pixelLess tracking back (present in special startup MC samples)
process.MitTreeFiller.PixelLessTracks.active          = True

# Path and EndPath definitions
process.digitisation_step   = cms.Path(process.pdigi)
process.L1simulation_step   = cms.Path(process.SimL1Emulator)
process.digi2raw_step       = cms.Path(process.DigiToRaw)
process.raw2digi_step       = cms.Path(process.RawToDigi)
process.L1Reco_step         = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction_withPixellessTk)
process.bambu_step          = cms.Path(process.BambuFillRECOSIM)

# Schedule definition
process.schedule = cms.Schedule(process.digitisation_step,
                                process.L1simulation_step,
                                process.digi2raw_step,
                                process.raw2digi_step,
                                process.L1Reco_step,
                                process.reconstruction_step,
                                process.bambu_step)
